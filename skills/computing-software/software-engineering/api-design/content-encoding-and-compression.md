---
id: computing-software.software-engineering.api-design.content-encoding-and-compression
name: content-encoding-and-compression
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, content-encoding, compression, gzip, brotli, accept-encoding, vary-header]
level: practitioner
status: docs-checked
description: "Compress API responses correctly: Accept-Encoding negotiation, Vary, which bodies to skip, and 415 handling for compressed request bodies."
sources: ["https://www.rfc-editor.org/rfc/rfc9110#section-8.4", "https://www.rfc-editor.org/rfc/rfc9110#field.accept-encoding", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Compression"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Content-Encoding and compression

## Negotiation
```http
GET /v1/events HTTP/1.1
Accept-Encoding: br, gzip;q=0.8, *;q=0.1

HTTP/1.1 200 OK
Content-Encoding: br
Vary: Accept-Encoding
```
- The client lists acceptable codings with optional `q` weights; `*` matches any coding not listed. Among acceptable codings with the same purpose, choose the one with the highest non-zero weight.
- A representation with no coding is acceptable unless `identity;q=0` or `*;q=0` (without a more specific `identity` entry) excludes it. A coding with `q=0` is unacceptable. With no `Accept-Encoding` header any coding is acceptable; with an empty one the client wants none.
- If nothing the server has is acceptable, SHOULD send the response without coding unless identity is ruled out.
- Always send `Vary: Accept-Encoding` with a negotiated response so caches keep separate representations (MDN).
- `Content-Encoding` lists the codings in the order applied and is a property of the representation: the representation is defined in terms of the coded form. Do not list `identity`. Registered codings include `gzip`, `deflate` and `compress`; MDN names `gzip` (most common) and `br` as the two relevant for the web.

## What to compress
MDN recommends compression for all files except already-compressed ones (images, audio, video); compressing twice usually gains nothing and can enlarge the file. Compression is configured in the web server or proxy: Apache `mod_deflate`, nginx `ngx_http_gzip_module`, IIS `httpCompression`. Check your server's documentation for size thresholds and type lists.

## Request bodies
A server may answer `415 Unsupported Media Type` when a request body has a content coding it cannot accept. When the 415 is about a content coding, it ought to include an `Accept-Encoding` header listing the supported codings; a 415 for any other reason MUST NOT include `Accept-Encoding`. Cap the decompressed size of anything you do accept.

## Gotchas
- Byte ranges refer to the encoded bytes (see range-requests-and-partial-content).
- Compression middleware may buffer streamed responses such as `text/event-stream`; test through your real path.
- Some non-conformant implementations send `deflate` data without the zlib wrapper; prefer `gzip`.

Verify: send a request with `Accept-Encoding: gzip` and check the response has `Content-Encoding: gzip` and `Vary: Accept-Encoding`; the same request with `Accept-Encoding: identity` returns uncompressed bytes.

## Checked
2026-11-08. Confirmed against RFC 9110 sections 8.4 and 12.5.3 (read in full) and the MDN Compression in HTTP guide (read in full). Removed: the nginx config values, weak-ETag advice, the BREACH paragraph, zstd, "browsers send br over HTTPS only" and the Content-Length remark (none in the sources). The SSE note is general advice, not from these pages.
Method: documentation only; no commands were run.
