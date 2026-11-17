---
id: computing-software.cloud-infrastructure-engineering.nginx.upstream-keepalive
name: upstream-keepalive
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, upstream-keepalive, keepalive, upstream, http-1-1, connection-reuse]
level: practitioner
status: docs-checked
description: "Keepalive connections to upstream servers: the keepalive directive and its defaults, keepalive_requests, keepalive_timeout, and the HTTP/1.1 Connection header settings."
sources: ["https://nginx.org/en/docs/http/ngx_http_upstream_module.html", "https://nginx.org/en/docs/http/ngx_http_proxy_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

```nginx
upstream app {
    server 10.0.0.11:8080;
    keepalive 32;
    keepalive_requests 1000;
    keepalive_timeout  60s;
}
location / {
    proxy_http_version 1.1;          # default since 1.29.7
    proxy_set_header Connection "";  # needed before 1.29.7
    proxy_pass http://app;
}
```

- `keepalive connections [local]` sets the maximum number of idle keepalive connections kept in the cache of each worker process; least recently used ones are closed on overflow, and `0` disables them. It does not limit the total number of connections a worker opens to upstream servers, so keep it small enough for upstream servers to accept new connections.
- Since 1.29.7 the default is `keepalive 32 local`: enabled, and cached connections are not shared between locations. `local` disables sharing across locations even when the upstream address matches.
- Before 1.29.7, when a load balancing method other than round-robin is used it must be activated before `keepalive`.
- `keepalive_requests` (default 1000; 100 before 1.19.10) caps requests per connection, `keepalive_time` (default 1h) caps the time requests may be processed through one connection, and `keepalive_timeout` (default 60s) is how long an idle upstream connection stays open. These are `upstream`-context directives (1.15.3+ for requests and timeout).
- For HTTP, `proxy_http_version` must be `1.1` (default since 1.29.7) or `2`, and before 1.29.7 the `Connection` header must be cleared.

## Checked
Date: 2026-11-03.
Confirmed in the ngx_http_upstream_module and ngx_http_proxy_module pages: all defaults, versions and behaviours above.
Removed as unconfirmed: the ephemeral-port exhaustion intro, the sporadic-502 advice about backend idle timeouts, the variable-upstream remark, and the `ss` verify step.
Method: documentation only; no commands were run.
