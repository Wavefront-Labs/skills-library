---
id: computing-software.cloud-infrastructure-engineering.nginx.gzip-compression
name: gzip-compression
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, gzip, gzip-types, compression, vary]
level: practitioner
status: docs-checked
description: "Enabling gzip in nginx with gzip_types, gzip_min_length, gzip_comp_level, gzip_proxied and gzip_vary, and the BREACH warning for TLS."
sources: ["https://nginx.org/en/docs/http/ngx_http_gzip_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Defaults from the `ngx_http_gzip_module` page: `gzip off`, `gzip_comp_level 1` (range 1 to 9), `gzip_min_length 20`, `gzip_proxied off`, `gzip_types text/html`, `gzip_vary off`, `gzip_http_version 1.1`.

```nginx
gzip on;
gzip_comp_level 5;
gzip_min_length 256;
gzip_vary on;
gzip_proxied any;
gzip_types text/css application/javascript application/json image/svg+xml text/plain;
```

- `text/html` responses are always compressed once `gzip on` is set; `gzip_types` adds other MIME types, and `*` matches any type.
- `gzip_min_length` is judged only from the `Content-Length` response header.
- A request is treated as proxied when it carries a `Via` header. `gzip_proxied` then decides per response: `expired`, `no-cache`, `no-store`, `private`, `no_last_modified`, `no_etag`, `auth`, or `any` for all proxied requests.
- `gzip_vary on` adds `Vary: Accept-Encoding` when `gzip`, `gzip_static` or `gunzip` is active.
- `gzip_disable regex ...` skips clients whose `User-Agent` matches; `msie6` is a special fast mask.
- `$gzip_ratio` holds the achieved compression ratio and can be logged.
- With SSL/TLS, compressed responses may be subject to BREACH attacks.

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_gzip_module` page (all directives, defaults, `Via` rule, BREACH note). Removed: the "4 to 6 sweet spot" advice, claims about already-compressed formats, backend `Accept-Encoding` stripping, `gzip_static` details, token-masking advice and the Verify step.
Method: documentation only; no commands were run.
