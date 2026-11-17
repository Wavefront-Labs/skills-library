---
id: computing-software.cloud-infrastructure-engineering.nginx.stale-cache-and-lock
name: stale-cache-and-lock
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, proxy-cache-use-stale, proxy-cache-lock, background-update, stampede]
level: practitioner
status: docs-checked
description: "Limiting cache stampedes and serving stale content in nginx with proxy_cache_lock, use_stale updating and proxy_cache_background_update."
sources: ["https://nginx.org/en/docs/http/ngx_http_proxy_module.html", "https://nginx.org/en/docs/http/ngx_http_upstream_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

```nginx
proxy_cache_lock on;                 # default off
proxy_cache_lock_timeout 5s;         # default 5s
proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
proxy_cache_background_update on;    # default off; nginx 1.11.10+
proxy_cache_revalidate on;           # default off
```

- With `proxy_cache_lock`, only one request at a time populates a new cache element; other requests for the same key wait for the response or for the lock to be released, up to `proxy_cache_lock_timeout`. After the timeout the request goes to the proxied server and its response is not cached. `proxy_cache_lock_age` (default 5s) lets one more request through if the first has not completed in that time.
- `proxy_cache_use_stale` takes the same parameters as `proxy_next_upstream`, plus `updating` (serve stale while it is being updated). `error` also covers the case where no proxied server can be selected.
- `proxy_cache_background_update` starts a background subrequest to refresh an expired item while the stale response is returned; the use of a stale response must be allowed (for example with `updating`).
- `proxy_cache_revalidate` revalidates expired items with conditional requests (`If-Modified-Since`, `If-None-Match`).
- Since 1.11.10 the `Cache-Control` extensions `stale-while-revalidate` and `stale-if-error` allow stale use for a number of seconds after the response became stale; the directive parameters take priority.
- `$upstream_cache_status` reports `STALE` or `UPDATING` for such responses.

## Checked
Date: 2026-11-03.
Confirmed in the ngx_http_proxy_module page: every directive, default and behaviour above. Confirmed in ngx_http_upstream_module: `$upstream_cache_status` values.
Removed as unconfirmed: the claim that stale content lives only until `inactive` removes it, the "long proxy_cache_valid" pairing advice, and the stopped-backend curl verify step.
Method: documentation only; no commands were run.
