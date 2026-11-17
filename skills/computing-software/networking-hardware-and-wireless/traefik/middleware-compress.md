---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-compress
name: middleware-compress
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, compress, gzip, brotli, zstd, content-encoding, middleware]
level: practitioner
status: docs-checked
description: "Enable gzip, brotli or zstd response compression with the compress middleware and tune thresholds and excluded content types."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/compress.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware compress
The `compress` middleware compresses responses with Gzip, Brotli (`br`) or Zstandard (`zstd`). Options: `encodings` (default gzip, br, zstd; list order sets priority), `defaultEncoding` (used when `Accept-Encoding` is absent or contains `*`), `excludedContentTypes`, `includedContentTypes` and `minResponseBodyBytes` (default 1024).

```yaml
http:
  middlewares:
    test-compress:
      compress:
        encodings: [zstd, br, gzip]
        minResponseBodyBytes: 1200
        excludedContentTypes:
          - text/event-stream
```
A response is compressed only when all hold: `Accept-Encoding` contains `gzip`, `*`, `br` and/or `zstd` (absent means no encoding unless `defaultEncoding` is set; an empty value turns compression off); the response has no `Content-Encoding` already; its `Content-Type` is not excluded (or is included); and the body is at least `minResponseBodyBytes`.

Gotchas: `excludedContentTypes` and `includedContentTypes` are mutually exclusive. `application/grpc` is never compressed. If the response has no or an empty `Content-Type`, Traefik detects one and sets the header.

## Checked
2026-11-03. Confirmed against the Traefik compress reference page (docs/content/reference/routing-configuration/http/middlewares/compress.md): options, defaults, activation criteria, mutual exclusivity, gRPC and Content-Type detection. Removed: the claim that compressing event streams "delays flushing", advice about images and archives, the "confirm against your version" hedge, and the curl Verify step.
Method: documentation only; no commands were run.
