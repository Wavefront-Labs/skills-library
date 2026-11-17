---
id: computing-software.networking-hardware-and-wireless.caddy.file-server-basics
name: file-server-basics
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [file-server, static-files, canonical-uris, index-files, hide, pass-thru, caddyfile]
level: practitioner
status: docs-checked
description: "Serve static files with Caddy file_server: root pairing, canonical URI redirects, index files, hide, status override, pass_thru and the symlink and systemd /home caveats."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/file_server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve a directory with `file_server` and know its defaults.

Paths are built by appending the request URI path to the site root. Pair it with the `root` directive (`root /srv` then `file_server`); the `root` subdirective inside file_server only affects that handler, so `try_files` and `templates` will not see it. Default root: `{http.vars.root}` or the working directory.

Canonical URIs: by default it redirects directories lacking a trailing slash (to add it) and files with one (to remove it), except when an internal rewrite changed the last path element. `disable_canonical_uris` turns that off.

Other subdirectives: `index` lists index filenames (default `index.html index.txt`); `hide` lists file-system paths (not request paths) to pretend do not exist, accepts globs and placeholders, a bare name matches anywhere, the active Caddyfile is hidden automatically, repeated uses append, and matching is case-sensitive so it is not a security boundary; `status` overrides the response code (placeholders allowed, useful in error pages); `pass_thru` continues to the next handler instead of a 404, only useful in a `route` with handlers after it, since file_server is ordered last.

Errors (404, 403) invoke `handle_errors` routes. Matcher use: `file_server /static/*` serves only that subtree.

Security notes: it blocks directory traversal in path components, but symlinks inside the root can still reach outside it, so the root is not a sandbox. Under systemd, the `caddy` user cannot traverse `/home`; use `/srv` or `/var/www/html`.

## Checked

2026-11-03: read caddyfile/directives/file_server against this skill. Confirmed: root handling, canonical URIs and disable_canonical_uris, index default index.html index.txt, hide, status, pass_thru, error handling, traversal and symlink notes, systemd /home note.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
