# METADATA #

## FORMAT ##

Metadata shall be stored in json files. It shall take the form of a top-level dictionary, with each key being an item of metadata. Heirarchical metadata
and types are preserved and explitily allowed.

Metadata is loaded from the top down, so each parent from the root can impart metadata on children. Children can explitily nullify parent metadata by
assigning it to undefined.

## STORAGE ##

On-disk meatdata is stored as a file along side the non-metadata file with the extension '.meta', for example the file 'foo.thtml' would have a metadata file as 'foo.thtml.meta'. Metadata for directories (which gets applied to all contents of that directory) is stored in .meta in the directory.

## DEFAULT KEYS AND VALUES ##

All files define the following keys by default:

filename
:  The local path of the file
path
:  The full path to the file from the root
type
:  The guessed mime-type of the file
stat
:  A tree of stat() values in a dictionary, without the ST_ prefix, and with lowercase keys.

Most files will want to define these keys:

template
:  The full path to the template file
template-fs
:  The full path to the filesystem template
title
:  A title for this object derived from the template, metadata or other sources.
description
:  A description of this file.

## METAMETADATA ##

Some keys support metadata replacement, such as title, description, template and type. The metadata becomes a micro template which allows some template functions to occur at load time based on existing / default metadata.

## CACHING STRATEGY ##

The tree is traversed from the top down, each node in the tree is stat(). The mtime walue is compared to the mtime stored in the cache dict for that node. If it is newer, the metadata
is loaded again, and the tree continues to traverse.
