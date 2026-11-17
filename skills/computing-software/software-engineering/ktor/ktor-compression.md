---
id: computing-software.software-engineering.ktor.ktor-compression
name: ktor-compression
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, compression, gzip, deflate, zstd, http-encoding, kotlin-server]
level: practitioner
status: docs-checked
description: "Use the Ktor Compression plugin to choose gzip, deflate or zstd encoders, set priorities, size and content-type rules, BREACH mitigation and request decompression."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-compression.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compress responses and decompress requests in Ktor

The `Compression` plugin (artifact `io.ktor:ktor-server-compression`) compresses response bodies and can decompress request bodies. Plain `install(Compression)` enables the `gzip`, `deflate` and `identity` encoders. For Zstandard also add the `ktor-server-compression-zstd` dependency. It does not support SSE responses, and the page says native servers are not supported.

## Pick encoders and priorities

```kotlin
install(Compression) {
    gzip { priority = 0.9 }
    deflate { priority = 1.0 }
    zstd { priority = 0.8 }
}
```

Calling `gzip()`, `deflate()`, `zstd()` enables only those. Higher priority wins, but the server first looks at the quality values in `Accept-Encoding`, then at your priorities. Zstd level defaults to 3: `zstd(level = 20)`.

## Limit what gets compressed

- By default `audio`, `video`, `image` and `text/event-stream` are not compressed. Use `matchContentType` to include types and `excludeContentType` to exclude them.
- `minimumSize(1024)` inside an encoder block skips responses not larger than that many bytes.
- `condition { request.uri == "/orders" }` applies an encoder only when your predicate on the request is true.

## BREACH mitigation

HTTPS with compression is vulnerable to BREACH. One mitigation is a `condition` on the `Referrer` header, for example `request.headers[HttpHeaders.Referrer]?.startsWith("https://my.domain/") == true`, so cross-site requests are not compressed.

## Decompress requests

Responses are compressed by default. To decode request bodies set `mode = CompressionConfig.Mode.DecompressRequest` and enable decoders such as `gzip()`. Decompression happens before other receive transformations like deserialization and multipart processing.

## Custom encoder

Implement the `ContentEncoder` interface; `GzipEncoder` is the reference example.

Related: serving pre-compressed static files is covered in the static content docs.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-compression.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
