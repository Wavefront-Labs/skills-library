---
id: computing-software.cloud-infrastructure-engineering.nginx.proxy-set-header-forwarding
name: proxy-set-header-forwarding
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, proxy-set-header, x-forwarded-for, host-header, real-ip]
level: practitioner
status: docs-checked
description: "Setting Host, X-Real-IP, X-Forwarded-For and X-Forwarded-Proto toward upstreams, and the inheritance trap of proxy_set_header."
sources: ["https://nginx.org/en/docs/http/ngx_http_proxy_module.html", "https://nginx.org/en/docs/http/ngx_http_realip_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

By default nginx sends `Host: $proxy_host` and `Connection: close` (when HTTP/1.0 or 1.1 proxying is on), so backends do not see the original Host.

```nginx
proxy_set_header Host              $host;
proxy_set_header X-Real-IP         $remote_addr;
proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

- `$host` is the server name from the `Host` request header, or the primary server name if the header is absent. `$http_host` passes the header unchanged but sends nothing if the client omitted it.
- `$proxy_add_x_forwarded_for` is the client's `X-Forwarded-For` with `$remote_addr` appended after a comma; if the client sent none it equals `$remote_addr`. The client controls any earlier entries.
- Inheritance trap: `proxy_set_header` is inherited from the previous level only if the current level defines none. A single `proxy_set_header` in a `location` discards all those set at `server` level, so repeat the full set or `include` a snippet.
- A header whose value is an empty string is not passed to the proxied server.
- If nginx sits behind another proxy, `ngx_http_realip_module` (not built by default; `--with-http_realip_module`) replaces the client address: `set_real_ip_from` (trusted addresses), `real_ip_header X-Forwarded-For`, and `real_ip_recursive on` (use the last non-trusted address in the header).
- With caching on, `If-Modified-Since`, `If-Unmodified-Since`, `If-None-Match`, `If-Match`, `Range` and `If-Range` from the client are not passed upstream.

## Checked
Date: 2026-11-03.
Confirmed in the ngx_http_proxy_module page: proxy_set_header defaults, inheritance rule, $http_host vs $host, empty-string rule, caching header list, `$proxy_add_x_forwarded_for`. Confirmed in ngx_http_realip_module: directives, recursion semantics, build flag.
Removed as unconfirmed: the "backend must trust only the rightmost hops" advice and the echo-server verify step.
Method: documentation only; no commands were run.
