# iterate source tree
#   create directors in target tree
#   for each item:
#    run processor(s) on item, each processor could be in a chain or a branch
#    Processors also provide filename munging
#    output target based on processor output

import argparse
import logging
import os
import shutil
import sys
import time

from typing import Dict, List, cast

from .processchain import ProcessorChains
from .processors.processors import PassthroughException
from .metadata import MetaTree
from .template_tools import file_list, file_name, file_content, file_metadata, time_iso8601


logger = logging.getLogger()


def setup_logging(verbose: bool = False) -> None:
    pass


def get_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser("Compile a Pixywerk directory into an output directory.")

    parser.add_argument("root", help="The root of the pixywerk directory to process.")
    parser.add_argument("output", help="The output directory to export post-compiled files to.")

    parser.add_argument(
        "-c", "--clean", help="Remove the target tree before proceeding (by renaming to .bak).", action="store_true"
    )
    parser.add_argument("-s", "--safe", help="Abort if the target directory already exists.", action="store_true")
    parser.add_argument("-t", "--template", help="The template directory (default: root/templates)", default=None)
    parser.add_argument("-d", "--dry-run", help="Perform a dry-run.", action="store_true")
    parser.add_argument("-v", "--verbose", help="Output verbosely.", action="store_true")
    parser.add_argument("--processors", help="Specify a path to a processor configuration file.", default=None)

    result = parser.parse_args(args)

    # validate arguments
    if not os.path.isdir(result.root):
        raise FileNotFoundError("can't find root folder {}".format(result.root))

    if not result.template:
        result.template = os.path.join(result.root, "templates")
        result.excludes = [result.template]

    return result


def main() -> int:
    try:
        args = get_args(sys.argv[1:])
    except FileNotFoundError as ex:
        print("error finding arguments: {}".format(ex))
        return 1
    setup_logging(args.verbose)
    if os.path.exists(args.output) and args.clean:
        bak = "{}.bak-{}".format(args.output, int(time.time()))
        print("cleaning target {} -> {}".format(args.output, bak))
        os.rename(args.output, bak)

    process_chains = ProcessorChains(args.processors)

    default_metadata = {
        "templates": args.template,
        "template": "default.jinja2",
        "dir-template": "default-dir.jinja2",
        "filters": {},
        "build-time": time.time(),
        "uuid-oid-root": "pixywerk",
        "summary": "",
        "description": "",
        "author": "",
        "author_email": ""
    }
    meta_tree = MetaTree(args.root, default_metadata)
    file_list_cache = cast(Dict, {})
    file_cont_cache = cast(Dict, {})
    file_name_cache = cast(Dict, {})
    default_metadata["globals"] = {
        "get_file_list": file_list(args.root, file_list_cache),
        "get_file_name": file_name(args.root, meta_tree, process_chains, file_name_cache),
        "get_file_content": file_content(args.root, meta_tree, process_chains, file_cont_cache),
        "get_file_metadata": file_metadata(meta_tree),
        "get_time_iso8601": time_iso8601("UTC"),
    }

    for root, _, files in os.walk(args.root):
        workroot = os.path.relpath(root, args.root)
        if workroot == ".":
            workroot = ""
        target_dir = os.path.join(args.output, workroot)
        print("mkdir -> {}".format(target_dir))
        if not args.dry_run:
            try:
                os.mkdir(target_dir)
            except FileExistsError:
                if args.safe:
                    print("error, target directory exists, aborting")
                    return 1
        for f in files:
            # fixme global generic filters
            if f.endswith(".meta") or f.endswith("~"):
                continue
            metadata = meta_tree.get_metadata(os.path.join(workroot, f))
            chain = process_chains.get_chain_for_filename(os.path.join(root, f), ctx=metadata)
            print("process {} -> {}".format(os.path.join(root, f), os.path.join(target_dir, chain.output_filename)))
            if not args.dry_run:
                try:
                    with open(os.path.join(target_dir, chain.output_filename), "w") as outfile:
                        for line in chain.output:
                            outfile.write(line)
                except PassthroughException:
                    shutil.copyfile(os.path.join(root, f), os.path.join(target_dir, chain.output_filename))

    return 0


if __name__ == "__main__":
    sys.exit(main())
