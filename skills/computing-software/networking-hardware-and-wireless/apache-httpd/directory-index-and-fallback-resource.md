---
id: computing-software.networking-hardware-and-wireless.apache-httpd.directory-index-and-fallback-resource
name: directory-index-and-fallback-resource
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-dir, directoryindex, directoryslash, fallbackresource, front-controller]
level: practitioner
status: docs-checked
description: "Control what a directory request returns: DirectoryIndex, DirectorySlash, DirectoryIndexRedirect, and FallbackResource for front-controller apps."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_dir.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_dir: index files and fallback
## DirectoryIndex
Default `index.html`. Files are tried in order; if none exist and `Indexes` is on, a listing is generated. Repeated directives in one context add to the list. `disabled` resets it.
```apache
DirectoryIndex index.html index.txt /cgi-bin/index.pl
```

## DirectorySlash
Default `On`: a directory request without trailing slash is redirected to one, giving a canonical URL and working relative links. Turning it off can disclose information: with `+Indexes` and an index file, the slash form shows the file but the bare form lists the directory.

## DirectoryIndexRedirect
Default `off`. Values `on`/`temp` (302), `permanent` (301), `seeother` (303) or a 3xx code send an external redirect to the index.

## FallbackResource
Handles requests that map to no file or handler instead of 404.
```apache
FallbackResource /index.php
<Directory "/web/example.com/htdocs/blog/images">
    FallbackResource disabled
</Directory>
```
Existing files are still served. For a sub-URI give the full path. It does not override `SetHandler` or `AddHandler`.

## DirectoryCheckHandler
Default `Off`: mod_dir processes the request even when another handler is set. `On` makes it do nothing then (pre-2.4 behaviour).

## Checked
2026-11-04. Confirmed against the mod_dir reference: DirectoryIndex default, ordering, accumulation and disabled; DirectorySlash default and information-disclosure warning; DirectoryIndexRedirect values; FallbackResource behaviour, sub-URI and handler interaction; DirectoryCheckHandler default. Nothing removed.
Method: documentation only; no commands were run.
