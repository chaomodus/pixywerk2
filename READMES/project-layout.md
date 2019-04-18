# Project Layout #

It is recommended that in general your project for PixyWerk2 site be layed out like:
```
project_top/
   Makefile              - Convenient for building your site
   src/                  - All "source" pages are contained in here.
     .meta               - Top-level default metadata is set here
     templates/          - Templates go in here
       default.jinja2    - Default template that will be used if none are specified
   publish/              - The path the build process will create, where the post-processed files go.
```


## Makefile ##

Makefile is suggested, but not essential, for encapsulating your build commands to produce your
site. Something as simple as:

```
build: src/templates/* src/*
	python -mpixywerk2 src publish
```

## src/ ##

This is the top level path that all of your templates, page fragments, images, etc. will be stored. This is basically the "source code" for your site.

## src/.meta ##

This is the top level metadata that is used as the default for all subsidiary metadata. It is in JSON format (with JS style comments). See <METADATA.md> for more information.

Example .meta file:

```
{
	"title": "My Website", // this is the default title applied if none are specified
	"author": "Super Web Dude",
	"site_root": "http://example.com",
	"uuid-oid-root": "example.com-", // this is used to generate UUIDs
}
```

## src/templates/ ##

Templates are all stored here, as this is the search path for Jinja.

## templates/default.jinja2 ##

If a page specifies a `template` metadata key, the named template is used, however, if not this template is used. Generally speaking this is a complete HTML file, with the `{{ content }}` template string placed where the content of subsidiary pages will be embedded.

A simple default.jinja2 example:

```
<!DOCTYPE html>
<html>
<head>
<title>{{ title }}</title>
</head>
<body>
{{content}}
</body>
</html>
```


## publish/ ##

This is arbitrary, and will be created by pixywerk at build time, but it will be the root path that should be published to your web server.
