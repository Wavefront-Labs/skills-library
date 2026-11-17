---
id: computing-software.networking-hardware-and-wireless.caddy.file-server-browse-listings
name: file-server-browse-listings
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [browse, directory-listing, file-server, sort, file-limit, reveal-symlinks, export-template]
level: practitioner
status: docs-checked
description: "Enable and customise directory listings with file_server browse: JSON and plaintext output, custom template, sort, file_limit and reveal_symlinks."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/file_server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: show an index of a directory that has no index file.

Enable with `file_server browse`, or the block form `browse [<template_file>] { reveal_symlinks  sort <field> [<direction>]  file_limit <number> }`.

Output formats: the default is an HTML page produced by a template. Clients can ask for machine formats with the `Accept` header: `Accept: application/json` returns JSON (handy in scripts) and `Accept: text/plain` returns plain text (handy at a terminal), for example with curl.

Options: `sort` takes a field `name`, `namedirfirst`, `size` or `time` and an optional direction `asc` or `desc`, so `sort name desc` sorts names in descending order. `file_limit` caps the number of listed entries, default 10000; beyond that only the first N are shown. `reveal_symlinks` shows symlink targets, which are hidden by default (only the link file itself is listed).

Custom template: pass a template file after `browse`. To start from the stock one, run `caddy file-server export-template`, which prints the default template to stdout; edit and point `browse` at it. Templates may use actions from the standard `templates` module as well.

Interaction: an index file in the directory (per `index`) takes precedence over the listing, and entries matched by `hide` do not appear, so you can keep dotfiles out of listings with `hide .git`.

## Checked

2026-11-03: read caddyfile/directives/file_server against this skill. Confirmed: browse syntax, Accept header formats, sort fields and directions, file_limit default 10000, reveal_symlinks, export-template, precedence of index files and hide.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
