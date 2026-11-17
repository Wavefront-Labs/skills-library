---
id: computing-software.messaging-and-integration.prosody.mod-http-files
name: mod-http-files
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, http, static-files, web, modules]
level: intro
status: docs-checked
description: "mod_http_files in Prosody: serve a static directory over HTTP with http_files_dir, index files, directory listing, MIME types file and cache size."
sources:
  - https://prosody.im/doc/modules/mod_http_files
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_http_files

Serves static files over HTTP. It is not for sharing files between XMPP clients; use `mod_http_file_share`.

```lua
modules_enabled = { "http_files"; }
http_files_dir = "/var/www"
```

| Option | Default |
|---|---|
| `http_files_dir` | none (required) |
| `http_index_files` | `{ "index.html", "index.htm" }` |
| `http_dir_listing` | false |
| `mime_types_file` | `"/etc/mime.types"` |
| `http_files_cache_max_file_size` | 4096 |

Files in `http_files_dir` must be readable by the user Prosody runs as (commonly prosody). An HTML file at `/var/www/index.html` should show up at `https://prosody.example:5281/files/`.

Notes on the options: `http_index_files` are served for a request for a directory if it contains one; `http_dir_listing` controls whether a directory listing is created where no index file is found; `http_files_cache_max_file_size` is the max file size for the in-memory cache.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_http_files (all five options and defaults, /files/ URL, readability). Removed a generic verify line.
Method: documentation only; no commands were run.
