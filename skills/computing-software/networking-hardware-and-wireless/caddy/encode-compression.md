---
id: computing-software.networking-hardware-and-wireless.caddy.encode-compression
name: encode-compression
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [encode, compression, gzip, zstd, accept-encoding, minimum-length, caddyfile]
level: practitioner
status: docs-checked
description: "Compress responses with the Caddyfile encode directive: zstd and gzip, levels, minimum_length, the default content-type match and how clients negotiate."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/encode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: enable response compression in a Caddyfile and understand which responses are actually compressed.

Syntax: `encode [<matcher>] [<formats...>] { gzip [<level>]  zstd [<level>]  minimum_length <length>  match <inline_response_matcher> }`. With no formats listed, `zstd` (preferred) and `gzip` are both enabled, so a bare `encode` equals `encode zstd gzip`. When several formats are on, the choice follows the request's `Accept-Encoding` header; if the client has no strong preference by q-factor, the first supported format in your list wins, which is why listing order expresses preference.

Levels: `zstd` accepts `default`, `fastest`, `better` or `best`; the default is roughly Zstandard level 3. `gzip` takes an optional level number.

`minimum_length` is the smallest body in bytes that will be encoded, default 512. Server-sent events (`Content-Type: text/event-stream`) and responses carrying `Incremental: ?1` are exempt from holding back: headers go out immediately and the body streams as written.

`match` takes an inline response matcher, so only matching responses are compressed. The default list is content-type based: `text/*`, `font/*`, JSON and JSON-flavoured types (`application/json*`, `application/ld+json*`, `application/vnd.api+json*`), XML and feeds (`application/xml*`, `application/rss+xml*`, `application/xhtml+xml*`), JavaScript, `application/wasm*`, `image/svg+xml*`, `image/x-icon*` and several font types.

Typical site: `root /srv`, `encode`, `file_server`.

## Checked
2026-11-03. Confirmed against the Caddy encode directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
