---
id: computing-software.cloud-infrastructure-engineering.nginx.proxy-cache-path-zone
name: proxy-cache-path-zone
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, proxy-cache, proxy-cache-path, keys-zone, caching, inactive]
level: practitioner
status: docs-checked
description: "Defining an nginx proxy cache with proxy_cache_path, keys_zone sizing, levels, inactive and max_size, then enabling it per location."
sources: ["https://nginx.org/en/docs/http/ngx_http_proxy_module.html", "https://nginx.org/en/docs/http/ngx_http_upstream_module.html", "https://nginx.org/en/docs/http/ngx_http_headers_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A cache needs a path and a shared memory zone (`http` context), then `proxy_cache` in the location.

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=appcache:10m
                 max_size=2g inactive=60m use_temp_path=off;

location / {
    proxy_cache appcache;
    proxy_cache_valid 200 301 10m;
    proxy_cache_valid 404 1m;
    add_header X-Cache-Status $upstream_cache_status always;
    proxy_pass http://app;
}
```

- `levels` takes 1 to 3 levels, each 1 or 2; file names are the MD5 of the cache key.
- One megabyte of `keys_zone` holds about 8 thousand keys, so `10m` is roughly 80 thousand keys (about 4 thousand per MB in the commercial subscription).
- `inactive` removes data not accessed within that time regardless of freshness; the default is 10 minutes.
- The cache manager process enforces `max_size` (and `min_free`) by removing least recently used data.
- `use_temp_path=off` puts temporary files directly in the cache directory; otherwise `proxy_temp_path` is used, and a copy across file systems replaces a cheap rename. Keep cache and temp directory on one file system.
- `proxy_cache_valid` with only a time caches 200, 301 and 302 responses. A `Set-Cookie` response, or `Vary: *`, is not cached; `X-Accel-Expires`, `Expires` and `Cache-Control` override the directive. `proxy_ignore_headers` turns that processing off, so use it with care.
- `$upstream_cache_status` is one of MISS, BYPASS, EXPIRED, STALE, UPDATING, REVALIDATED, HIT.

## Checked
Date: 2026-11-03.
Confirmed in the ngx_http_proxy_module page: proxy_cache_path parameters, levels, MD5 file names, 8 thousand keys per MB (4 thousand commercial), inactive default 10 minutes, cache manager and max_size, use_temp_path, proxy_cache_valid behaviour and the header rules. Confirmed in ngx_http_upstream_module: `$upstream_cache_status` values. Confirmed in ngx_http_headers_module: `add_header ... always`.
Removed as unconfirmed: the "disk can overshoot briefly" claim, `Cache-Control: private` as a blocker, the curl/grep verify step.
Method: documentation only; no commands were run.
