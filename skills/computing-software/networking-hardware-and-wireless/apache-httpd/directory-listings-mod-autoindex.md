---
id: computing-software.networking-hardware-and-wireless.apache-httpd.directory-listings-mod-autoindex
name: directory-listings-mod-autoindex
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-autoindex, indexes, indexoptions, indexignore, directory-listing]
level: practitioner
status: docs-checked
description: "Generate and tune directory listings with mod_autoindex: Options Indexes, IndexOptions, IndexIgnore, header and readme files, icons, and query arguments."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_autoindex.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_autoindex directory listings
A listing is generated when no `DirectoryIndex` file exists; enable it with `Options +Indexes`.

## IndexOptions
`+`/`-` change inherited options; an unprefixed keyword clears them.
```apache
IndexOptions FancyIndexing HTMLTable FoldersFirst VersionSort
IndexOptions +SuppressSize -IconsAreLinks
```
- `HTMLTable` builds a table (needed for UTF-8 or mixed-direction names).
- `NameWidth=n|*` (default 20 bytes), `FoldersFirst`, `IgnoreCase`, `VersionSort`.
- `SuppressColumnSorting`; `IgnoreClient` ignores all client arguments and implies it.
- `SuppressHTMLPreamble`; `None` must appear alone.

## Hiding and framing
- `IndexIgnore .??* *~ *#` hides files (`?` and `*` only; default `.`; accumulates). `IndexIgnoreReset ON` clears inherited entries.
- `HeaderName /include/HEADER.html`, `ReadmeName FOOTER.html`.
- `AddIconByType (IMG,/icons/image.png) image/*` is preferred over `AddIcon`.
- `IndexOrderDefault Descending Date`; `IndexStyleSheet` (table id `indexlist`).

## Client arguments
`C=` N/M/S/D sort column, `O=` A/D order, `F=` 0/1/2 format, `V=` version sort, `P=` pattern. Example `/docs/?C=M&O=D&F=1`. Parsing stops at the first unknown argument, so put such arguments last.

## Checked
2026-11-04. Confirmed against the mod_autoindex reference: Options +Indexes, IndexOptions incremental syntax, HTMLTable, NameWidth default, IgnoreClient, None, IndexIgnore and IndexIgnoreReset, HeaderName/SuppressHTMLPreamble, AddIconByType preference, IndexStyleSheet id, query arguments and parser behaviour. Nothing removed.
Method: documentation only; no commands were run.
