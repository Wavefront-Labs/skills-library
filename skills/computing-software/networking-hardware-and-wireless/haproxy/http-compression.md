---
id: computing-software.networking-hardware-and-wireless.haproxy.http-compression
name: http-compression
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, compression-filter, gzip-compression, compression-offload, compression-algo]
level: practitioner
status: docs-checked
description: "Enable gzip compression in HAProxy with compression algo, type and offload, know when it is skipped, and cap its CPU cost."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http compression
The `compression` keywords enable and configure compression; since HAProxy 1.7 compression is implemented as a filter. When no other filter is used, the `compression` keywords are enough. An explicit `filter compression` line is mandatory only when at least one filter other than cache or fcgi-app is used on the same proxy, because it fixes the filter evaluation order. With a cache, compression is always done after the response is stored.

```
backend be_app
    compression algo gzip
    compression type text/html text/plain text/css application/javascript application/json
```
`compression algo` (response algorithms; `algo-res` and `algo-req` are the explicit forms) accepts `identity` (debugging only), `gzip`, `deflate` and `raw-deflate`. The docs say `gzip`/`deflate`/`raw-deflate` need zlib or libslz built in, and that `deflate` is not worth using (ambiguous or no support in recent browsers; never combine it with `raw-deflate`). `compression type` lists the MIME types to compress. `compression direction request|response|both` (default `response`) chooses whether requests, responses or both are compressed.

Compression is applied from the request's `Accept-Encoding`. If the backend already compresses, HAProxy sees the compressed response and does not compress again. It is disabled when, among others: the request advertises no supported algorithm; the response is not HTTP/1.1 or above; the status is not 200, 201, 202 or 203; the response has neither `Content-Length` nor chunked `Transfer-Encoding`; the `Content-Type` starts with `multipart`; `Cache-Control` contains `no-transform`; the response has a `Content-Encoding`; or it has an invalid or multiple `ETag` headers.

`compression offload` removes `Accept-Encoding` so backends do not compress. The docs strongly recommend against it (all compression work lands on HAProxy); it exists for buggy gateways whose compression cannot be turned off. In a `defaults` section it only warns and is ignored.

Cost control: global `maxcomprate` (kB/s of input per process, default 0 = no limit), global `maxcompcpuusage` (percent of CPU, default 100 = no limit) and `tune.comp.maxlevel` (default 1).

Verify: `haproxy -c -f <config>` accepts the settings; a request with `Accept-Encoding: gzip` for a listed type should come back with `Content-Encoding: gzip`.

## Checked
2026-11-03. Confirmed against configuration.html: `compression algo/algo-req/algo-res/type/direction/offload`, section 9.2 (compression filter), `filter` example, `maxcomprate`, `maxcompcpuusage`, `tune.comp.maxlevel`. Removed: brotli/zstd support claims, the "Content-Length below a small threshold" and "206 ranges" and "images/video" skip conditions, the BREACH advice, "Vary: Accept-Encoding is automatic", and the "confirm syntax" marker; the earlier recommendation of `offload` as normal practice was reversed to match the docs. The `curl | grep` verify line was dropped.
Method: documentation only; no commands were run.
