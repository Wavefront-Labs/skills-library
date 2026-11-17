---
id: computing-software.networking-hardware-and-wireless.apache-httpd.proxy-worker-parameters-and-timeouts
name: proxy-worker-parameters-and-timeouts
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-proxy, workers, connection-pool, timeouts, proxy-http, environment-variables]
level: advanced
status: docs-checked
description: "Tune proxy backends with worker parameters (timeout, ttl, retry, max) and mod_proxy_http environment variables like proxy-sendcl and proxy-initial-not-pooled."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_proxy.html
  - https://httpd.apache.org/docs/2.4/mod/mod_proxy_http.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxy worker parameters and timeouts
Set on `ProxyPass`, `ProxySet` or `BalancerMember`:

| Parameter | Purpose |
|---|---|
| `connectiontimeout` | seconds to wait for a backend connection |
| `timeout` | seconds to wait for backend data |
| `max` / `min` / `smax` | pool sizing |
| `ttl` | close connections idle longer than this |
| `retry` | seconds before retrying a worker in error (default 60) |
| `disablereuse` | close after each use |
| `keepalive` | TCP keepalive probes through firewalls |

```apache
ProxyPass "/example" "http://backend.example.com" max=20 ttl=120 retry=300
```
`ProxyTimeout` defaults to `Timeout`.

## mod_proxy_http environment variables
Variables without specific values are enabled when set to any value:
- `proxy-nokeepalive`: close backend connection after each request.
- `force-proxy-request-1.0`: send HTTP/1.0 to the backend.
- `proxy-sendcl`: force Content-Length (may buffer whole body); `proxy-sendchunks`: chunked request bodies.
- `proxy-interim-response`: `RFC` (default) passes 1xx; `Suppress` drops them.
- `proxy-initial-not-pooled`: avoids "error reading status line from remote server" at a performance cost.
- `proxy-chain-auth`: forwards proxy credentials down a chain; only if you need it.

mod_proxy_http supports HTTP/0.9, 1.0 and 1.1, has no directives and no caching (use mod_cache).

## Checked
2026-11-04. Confirmed against the mod_proxy worker parameter table, ProxyTimeout, and the mod_proxy_http reference (environment variables, protocol support, no caching). Reworded the environment variable intro to what the page says.
Method: documentation only; no commands were run.
