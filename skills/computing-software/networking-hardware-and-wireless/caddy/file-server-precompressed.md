---
id: computing-software.networking-hardware-and-wireless.caddy.file-server-precompressed
name: file-server-precompressed
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [precompressed, sidecar-files, brotli, zstd, gzip, content-encoding, file-server]
level: advanced
status: docs-checked
description: "Serve precompressed sidecar files with file_server precompressed (br, zstd, gzip), lookup order, Content-Encoding handling and the encode interaction."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/file_server
  - https://caddyserver.com/docs/caddyfile/directives/encode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve build-time compressed assets instead of compressing on every request.

Config: `file_server { precompressed [<formats...>] }`. Supported formats and their sidecar extensions are `gzip` (`.gz`), `zstd` (`.zst`) and `br` (`.br`). The arguments are an ordered preference list; when omitted they default to `br zstd gzip`, in that order.

Lookup flow: the file server first checks that the uncompressed file exists. Then, if the client's `Accept-Encoding` allows it, it looks for the sidecar with each enabled extension in order. For `/path/to/file` that means `/path/to/file.br`, `/path/to/file.zst`, `/path/to/file.gz`, serving the first one found with the matching `Content-Encoding` response header. If none exists, the plain file is served as normal.

Combining with `encode`: the `encode` directive compresses on the fly only responses that were not already precompressed, so `encode` plus `precompressed` gives sidecars where you built them and live compression elsewhere. Note `encode` supports only zstd and gzip, while precompressed also handles Brotli, so Brotli is available to clients only through sidecars.

Workflow: produce the `.br`/`.zst`/`.gz` files in your build step next to each asset, keeping the originals in place, since an uncompressed file must exist.

## Checked

2026-11-03: read caddyfile/directives/file_server, caddyfile/directives/encode against this skill. Confirmed: precompressed formats and extensions, default order br zstd gzip, lookup order, interaction with encode.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
