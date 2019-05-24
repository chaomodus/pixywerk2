"""Convert a Wordpress XML dump into to a (mostly working) pixywerk2 tree."""

import argparse
import datetime
import json
import os
import sys
from urllib.parse import urlparse
from xml.etree.ElementTree import ElementTree

import requests

FILE_PATTERN = "{postdate}-{postname}.thtml"


def parse_args(args):
    parser = argparse.ArgumentParser("importwp.py")

    parser.add_argument("input", help="The input file.")
    parser.add_argument("out_dir", help="Output root directory.", default='.')
    parser.add_argument("--fetch-attachments", help="Fetch all attachments referred to in file.", action="store_true", dest='fetch_attachments')
    parser.add_argument("--attachment-dir", help="Subdirectory to place attachments in.", default="attachments", dest='attachment_dir')
    parser.add_argument("--post-dir", help="Subdirectory to place posts in.", default="posts", dest='post_dir')
    parser.add_argument("--page-dir", help="Subdirectory to place pages in.", default="", dest='page_dir')

    result = parser.parse_args(args)
    result.post_dir = os.path.join(result.out_dir, result.post_dir)
    result.page_dir = os.path.join(result.out_dir, result.page_dir)
    result.attachment_dir = os.path.join(result.out_dir, result.attachment_dir)

    return result


def parse_input(xmlpath):
    tree = ElementTree()

    tree_root = tree.parse(source=xmlpath)
    posts = {}
    attachments = {}
    pages = {}

    for node in tree_root.find("channel"):
        if node.tag == "item":
            post_type = node.find("{http://wordpress.org/export/1.2/}post_type")
            if post_type is not None:
                status = node.find("{http://wordpress.org/export/1.2/}status")
                if status is not None and status.text == "draft":
                    continue
                content = node.find("{http://purl.org/rss/1.0/modules/content/}encoded")
                title = node.find("title")
                pubdate = node.find("pubDate")
                description = node.find("description")
                post_name = node.find("{http://wordpress.org/export/1.2/}post_name")
                categories = node.findall("category")
                post_id = node.find("{http://wordpress.org/export/1.2/}post_id")
                post_parent = node.find("{http://wordpress.org/export/1.2/}post_parent")
                if post_type.text == "post":
                    # found a post!
                    posts[post_id.text] = {'content':content,
                                           'title':title,
                                           'pubdate':pubdate,
                                           'description':description,
                                           'post_name':post_name,
                                           'categories':categories,
                                           'post_parent':post_parent}
                elif post_type.text == "attachment":
                    # attachment
                    att_url = node.find("{http://wordpress.org/export/1.2/}attachment_url")

                    attachments[post_id.text] = {'content':content,
                                                 'title':title,
                                                 'pubdate':pubdate,
                                                 'description':description,
                                                 'post_name':post_name,
                                                 'categories':categories,
                                                 'post_parent':post_parent,
                                                 'att_url':att_url,}
                elif post_type.text == "page":
                    pages[post_id.text] = {'content':content,
                                           'title':title,
                                           'pubdate':pubdate,
                                           'description':description,
                                           'post_name':post_name,
                                           'categories':categories,
                                           'post_parent':post_parent}

    return posts, attachments, pages

def fetch_attachment(attch, outdir):
    url = attch['att_url'].text
    p = urlparse(url)
    filename = os.path.join(outdir, os.path.split(p.path)[-1])
    print("fetching attachment",url,"->",filename)
    r = requests.get(url)
    with open(filename, 'wb') as outf:
        outf.write(r.content)

def save_cont(post, outdir):
    dt = datetime.datetime.strptime(post['pubdate'].text, "%a,  %d %b %Y %H:%M:%S %z")
    postdate = dt.strftime("%Y-%m-%d-%H%M%S")
    filename = FILE_PATTERN.format(postdate=postdate, postname=post['post_name'].text)
    print(post['title'].text, "->", filename)
    with open(os.path.join(outdir, filename), "w") as outf:
        outf.write(post['content'].text)
        # handle attachments

        tags = []
        category = ""
        for tg in post['categories']:
            if "domain" in tg.attrib and tg.attrib["domain"] == "category":
                category = tg.text
            else:
                tags.append(tg.text)

    with open(os.path.join(outdir, filename + ".meta"), "w") as outf:
        metadata = {
            "title": post['title'].text,
            "description": post['description'].text,
            "post_time": dt.timestamp(),
            "featured": "",
            "tags": tags,
            "category": category,
        }
        json.dump(metadata, outf)


def main():
    args = parse_args(sys.argv[1:])
    try:
        os.mkdir(args.out_dir)
    except FileExistsError:
        pass

    try:
        os.mkdir(args.page_dir)
    except FileExistsError:
        pass

    try:
        os.mkdir(args.post_dir)
    except FileExistsError:
        pass

    if args.fetch_attachments:
        try:
            os.mkdir(args.attachment_dir)
        except FileExistsError:
            pass

    posts, attachments, pages = parse_input(args.input)

    if args.fetch_attachments:
        [fetch_attachment(post, args.attachment_dir) for post in attachments.values()]

    [save_cont(post, args.post_dir) for post in posts.values()]
    [save_cont(page, args.page_dir) for page in pages.values()]

    return 0


if __name__ == "__main__":
    sys.exit(main())
