# Template Functions #

These are functions exposed to the templates which perform various useful actions for the site designer.

## get_file_list ##

Return a list of file names based on a wildcard glob, matched against the root of the project.

Prototype: `get_file_list(file_glob, sort_order, reverse, limit) -> [files]`

Arguments:
* file_glob: A standard file glob, for example `*.txt` matches all files that end in `.txt` in the root of the project. (default: `*`)
* sort_order: A string of either `file_path`, `file_name`, `ctime`, `mtime`, `size` and `ext` (default: `ctime`)
* reverse: whether the sort is reversed (default: False)
* limit: The number of entries to return from the top of the list, 0 for unlimited (default: `0`)

Returns:
* A list of file names.

## get_file_name ##

Return the filename that will result from processing the specified file based on the processors that it will be passed through.

Prototype: `get_file_name(file) -> outfile`

Arguments:
* file: The name of a file, with path, from root.

Returns:
* outfile: The name of the file, with path, that will result from processing.

## get_file_content ##

Return the rendered content of specified file. Caution: Can result in infinite loops if two templates include each other.

Prototype: `get_file_content(file) -> content`

Arguments:
* file: The name of the input file, with path, from root.

Returns:
* content: the contents that result from passing the specified file through its processors.

## get_raw ##

Return the raw contents of a source file. It is specifically not passed through any processing.

Prototype: `get_raw(file) -> content`

Arguments:
* file: The name of the input file, with path, from root.

Returns:
* content: the raw contents of the input file

## get_file_metadata ##

Return the metadata tree associated with a particular file.

Prototype: `get_file_metadata(file) -> metadata`

Arguments:
* file: the name of an input file, with path, from root

Returns:
* metadata: A dictionary of metadata loaded from the file tree.

## get_time_iso8601 ##

Return the date/time stamp in ISO 8601 format for a given time_t timestamp for UTC.

Prototype: `get_time_iso8601(timestamp) -> timestamp`

Arguments:
* timestamp: A time_t integer or float, in seconds since Jan 1 1970.

Returns:
* timestamp: A string in ISO8601 format of the date and timestamp, in the UTC timezone.

## get_date_iso8601 ##

Return the date stamp in ISO 8601 format for a given time_t timestamp for UTC.

Prototype: `get_date_iso8601(timestamp) -> timestamp`

Arguments:
* timestamp: A time_t integer or float, in seconds since Jan 1 1970.

Returns:
* timestamp: A string in ISO8601 format of the date stamp, in the UTC timezone.

## pygments_get_css ##

Return a blob of CSS produced from Pygments for a given `style`.

Prototype: `pygments_get_css(style) -> css`

Arguments:
* style (optional): A style identifier for the Pygments' HTMLFormatter.

Returns:
* css: A string of styles as returned by Pygments' HTMLFormatter.

## pygments_markup_contents_html ##

Format a code fragment with Pygments

Prototype: `pygments_markup_contents_html(input, filetype, style) -> html`

Arguments:
* input: A string containing the code to format (either literal, or imported with get_raw()).
* filetype: A string describing which lexer to use.
* style (optional) A style identifier for Pygments' HTMLFormatter.
