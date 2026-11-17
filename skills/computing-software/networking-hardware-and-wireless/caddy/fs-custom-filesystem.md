---
id: computing-software.networking-hardware-and-wireless.caddy.fs-custom-filesystem
name: fs-custom-filesystem
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [fs, filesystem, global-option, file-server, embedded, caddy-fs]
level: advanced
status: docs-checked
description: "Point Caddy file I/O at a named alternate filesystem with the fs directive and the filesystem global option, including per-path use."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/fs
  - https://caddyserver.com/docs/caddyfile/directives/file_server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve or inspect files from something other than the local disk.

Two steps. First declare a named filesystem with the `filesystem` global option, giving the name and a module from the `caddy.fs` namespace plus its settings. The example uses an imaginary module: `{ filesystem foo custom { api_key abc123 } }`. Then select it in a site with `fs [<matcher>] <filesystem>`.

Site example: `example.com { fs foo  root /srv  file_server }`. The root path or prefix still applies inside the alternate filesystem. To mix backends, give a path matcher: `fs /images* foo` serves images from `foo` while the rest comes from the default (local disk) filesystem.

`fs` affects the file-reading directives, typically `file_server` and `try_files`, and is normally combined with `root`. The `file_server` directive also has its own `fs <backend...>` subdirective for the same purpose on a single handler.

Embedded files: `xcaddy` v0.4.0 added an `--embed` flag that embeds a directory tree in a custom Caddy build and registers an `fs` module named `embedded`, so a static site ships as a single executable.

## Checked

2026-11-03: read caddyfile/directives/fs, caddyfile/directives/file_server against this skill. Confirmed: filesystem global option, fs directive syntax and matcher form, file_server fs subdirective, xcaddy v0.4.0 --embed and the embedded fs module (stated on the file_server page).
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
