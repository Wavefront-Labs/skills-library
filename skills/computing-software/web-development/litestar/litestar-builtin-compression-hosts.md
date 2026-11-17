---
id: computing-software.web-development.litestar.litestar-builtin-compression-hosts
name: litestar-builtin-compression-hosts
category: computing-software
field: web-development
product: litestar
tags: [litestar, middleware, allowed-hosts, compression, gzip, brotli, zstd, cors, csrf]
level: practitioner
status: docs-checked
description: "Configure Litestar AllowedHostsConfig and CompressionConfig for gzip, brotli and zstd, plus CORS and CSRF config basics."
sources: [https://docs.litestar.dev/latest/usage/middleware/builtin-middleware.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar built-in middleware: hosts, compression (and CORS/CSRF)

Goal: enable allowed-hosts checking and response compression with the documented options.

## Method

Allowed hosts (checks the `Host` or `X-Forwarded-Host` header):

```python
from litestar.config.allowed_hosts import AllowedHostsConfig
app = Litestar(route_handlers=[...],
    allowed_hosts=AllowedHostsConfig(allowed_hosts=["*.example.com", "www.wikipedia.org"]))
```

A plain list of domains also works. Wildcards only as a prefix (`*.`), matching any subdomain depth; `*` allows all (like turning it off); wildcards in the middle or end raise a validation exception.

Compression: pass `CompressionConfig` (from `litestar.config.compression`) as `compression_config`.

- gzip (built in): `CompressionConfig(backend="gzip", gzip_compress_level=9)`; `minimum_size` default 500; level 0-9, default 9.
- brotli: `pip install 'litestar[brotli]'`; `CompressionConfig(backend="brotli", brotli_gzip_fallback=True)`. Options: `brotli_quality` (0-11, default 5), `brotli_mode` (`generic`/`text`/`font`, default `text`), `brotli_lgwin` (10-24, default 22), `brotli_lgblock` (16-24 or 0, default 0), `brotli_gzip_fallback`.
- zstd: `pip install 'litestar[zstd]'`; `CompressionConfig(backend="zstd", zstd_gzip_fallback=True)`. Options: `zstd_compress_level` (int >= 0, 0 = library default, default 0), `zstd_gzip_fallback` (default True).

CORS: `Litestar(route_handlers=[...], cors_config=CORSConfig(allow_origins=["https://www.example.com"]))` (`litestar.config.cors`).

CSRF: `CSRFConfig(secret="my-secret")` passed as `csrf_config`; defaults cookie `csrftoken`, header `x-csrftoken`, form key `_csrf_token` (not configurable). Exempt a handler with `exclude_from_csrf=True` or use `CSRFConfig.exclude` path patterns.

## Verify

Per the page, a CSRF client that sends the header but no persisted cookie gets a 403 containing "CSRF token verification failed"; one using a cookie-persisting `httpx.Client` succeeds.

## Checked

2026-11-07. Read the full cited page(s) (usage/middleware/builtin-middleware.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
