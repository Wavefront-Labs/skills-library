---
id: computing-software.cloud-infrastructure-engineering.nginx.hash-consistent-affinity
name: hash-consistent-affinity
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, upstream-hash, hash, consistent-hashing, affinity, cache-sharding]
level: advanced
status: docs-checked
description: "Using hash key [consistent] and ip_hash in nginx upstream groups for cache sharding or affinity, and how server changes remap keys."
sources: ["https://nginx.org/en/docs/http/ngx_http_upstream_module.html", "https://nginx.org/en/docs/http/ngx_http_core_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`hash key [consistent];` (upstream context, 1.7.2) maps a request to a server by a hashed key, which can be text, variables or a combination. Adding or removing a server may remap most keys. With `consistent`, ketama consistent hashing is used so only a few keys are remapped when a server is added or removed, which helps cache hit ratio on caching servers.

```nginx
upstream cache_pool {
    hash $request_uri consistent;
    server c1:8080;
    server c2:8080;
}
upstream by_cookie {
    hash $cookie_session_id consistent;
    server a:80;
    server b:80;
}
```

- `$cookie_name` is the request cookie called `name`; `$request_uri` is the full original request URI with arguments.
- `ip_hash;` hashes the first three octets of an IPv4 client address (or the whole IPv6 address), so a client keeps hitting the same server unless it is unavailable. Mark a server `down` rather than deleting it to preserve the current hashing.
- The `backup` server parameter cannot be used with `hash`, `ip_hash` or `random`; the same holds for `slow_start` (commercial).

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_upstream_module` page (`hash`, `ip_hash`, `down`, `backup`) and `ngx_http_core_module` (`$cookie_name`, `$request_uri`). Removed: claims about empty-key behaviour, weights in the key space, failover returning to the original server, realip advice and the Verify step.
Method: documentation only; no commands were run.
