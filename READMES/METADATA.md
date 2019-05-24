# METADATA #

## FORMAT ##

Metadata is stored as a JSON file which allows C-likecomments.

Metadata is loaded from the top down, so each parent from the root can impart metadata on children. Children can explitily nullify parent metadata by
assigning it to undefined.

## STORAGE ##

On-disk meatdata is stored as a file along side the non-metadata file with the extension '.meta', for example the file 'foo.thtml' would have a metadata file as 'foo.thtml.meta'. Metadata for directories (which gets applied to all contents of that directory) is stored in .meta in the directory.

## DEFAULT KEYS AND VALUES ##

All files define the following keys by default:

relpath
:  The relative path to the root of the site, useful for prepending to image `src=` and other resource paths such as CSS files and fonts in order to maintain locally viewable output.
file_name
:  The local path of the file
file_path
:  The full path to the file from the root
dir
:  The directory to the path from root for this file
os-path
:  The native OS path to this file
guessed-type
:  The guessed mime-type of the file
stat
:  A tree of stat() values in a dictionary, without the ST_ prefix, and with lowercase keys.
templates
:  The path to the template files.
uuid
:  A UUID for this file based on its path and a specified `uuid-oid-root` metadata
build-time
:  The time stamp for the build time

Files can also explicitly override these which are set to empty defaults:

mime-type
:  Either the specified mime-type or guessed type if undefined.
template
:  The full path to the template file
dir-template
:  The full path to the filesystem template
title
:  A title for this object derived from the template, metadata or other sources.
summary
:  A summary of the file contents.
description
:  A description of file contents.

Trees have some metadata that projects should probably override (generally in their top-level .meta):

uuid-oid-root
:  A string added to the beginning of the path that identifies this site, used for deriving OID UUIDs.
author
:  The full name of the author of this site (should also be overridden per-file if necessary).
author_email
:  The email of the author of this site (see above)
site_root
:  The full URL for the root of this web site used for links and whatnot, with ending slash.

Special Keys that can be defined, these change the processing in predictable ways:

type
: Define that the file that this metadata is applied to as a specific type from the type mapping table. Useful values are `passthrough` and `templatable` with obvious outcomes.
wildcard_metadata
: Define a dictionary of file globs (patterns which match files such as `*.txt`), with the value being a dictionary of additional metadata to apply to the matched files. This is generally
defined at the top level of the project to make certain file patterns treated as special without having to give them their own metadata.


## CACHING STRATEGY ##

The tree is traversed from the top down, each node in the tree is stat(). The mtime walue is compared to the mtime stored in the cache dict for that node. If it is newer, the metadata
is loaded again, and the tree continues to traverse.
