---
id: computing-software.cloud-infrastructure-engineering.nginx.upstream-server-params
name: upstream-server-params
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, upstream-max-fails, upstream, max-fails, fail-timeout, backup, down]
level: practitioner
status: docs-checked
description: "upstream server parameters weight, max_fails, fail_timeout, backup and down, and how unsuccessful attempts mark a server unavailable."
sources: ["https://nginx.org/en/docs/http/ngx_http_upstream_module.html", "https://nginx.org/en/docs/http/ngx_http_proxy_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

```nginx
upstream app {
    server 10.0.0.11:8080 weight=3 max_fails=3 fail_timeout=30s;
    server 10.0.0.12:8080;
    server 10.0.0.20:8080 backup;
    server 10.0.0.13:8080 down;
}
```

- `weight=number`: default 1. The default method is weighted round-robin.
- `max_fails=number`: unsuccessful attempts within `fail_timeout` that make the server unavailable. Default 1; `0` disables the accounting. What counts as unsuccessful is set by `proxy_next_upstream` (and the fastcgi/uwsgi/scgi/memcached/grpc equivalents).
- `fail_timeout=time`: both the window in which the failures must happen and how long the server is then considered unavailable. Default 10 seconds.
- `backup`: receives requests only when the primary servers are unavailable. Cannot be used with the `hash`, `ip_hash` and `random` methods.
- `down`: marks the server permanently unavailable. With `ip_hash`, marking a server `down` preserves the current hashing of client addresses.
- With a single server in the group, `max_fails`, `fail_timeout` and `slow_start` are ignored and the server is never considered unavailable.
- `slow_start` is a commercial-subscription parameter, as is the dynamic group with periodic health checks in the module's example. `max_conns=number` limits simultaneous connections to a server (default 0, no limit); without a shared-memory zone the limit is per worker process.

## Checked
Date: 2026-11-03.
Confirmed in the ngx_http_upstream_module page: all parameters, defaults, single-server rule, ip_hash note, commercial markers. Confirmed in ngx_http_proxy_module: `proxy_next_upstream` defines unsuccessful attempts.
Removed as unconfirmed: the claim that open source nginx has only passive checks and needs Lua or other modules for active probes, the "hash" wording on down, and the kill-a-backend verify step.
Method: documentation only; no commands were run.
