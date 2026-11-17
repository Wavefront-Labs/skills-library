---
id: computing-software.cloud-infrastructure-engineering.nginx.websocket-proxying
name: websocket-proxying
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, websocket, upgrade, connection-upgrade, proxy-read-timeout]
level: practitioner
status: docs-checked
description: "Proxying WebSockets through nginx with Upgrade and Connection headers, a map for $connection_upgrade, and the 60-second idle timeout."
sources: ["https://nginx.org/en/docs/http/websocket.html", "https://nginx.org/en/docs/http/ngx_http_proxy_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Since 1.3.13 nginx can set up a tunnel between client and proxied server when the server answers with code 101 (Switching Protocols) to a client `Upgrade` request. `Upgrade` and `Connection` are hop-by-hop headers and are not passed from client to proxied server, so they must be set explicitly.

```nginx
http {
    map $http_upgrade $connection_upgrade {
        default upgrade;
        ''      close;
    }

    server {
        location /chat/ {
            proxy_pass http://backend;
            # proxy_http_version 1.1;   # needed before 1.29.7
            proxy_set_header Upgrade    $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
        }
    }
}
```

- The simple form is `proxy_set_header Upgrade $http_upgrade;` with `proxy_set_header Connection "upgrade";`. The `map` version sends `Connection: close` when the client sent no `Upgrade` header.
- By default the connection is closed if the proxied server transmits no data within 60 seconds. Raise `proxy_read_timeout`, or have the proxied server send WebSocket ping frames periodically.

## Checked
Date: 2026-11-03.
Confirmed in the websocket page and the ngx_http_proxy_module page: the 101 tunnel behaviour and version, hop-by-hop rule, both examples, the 1.29.7 note, the 60 second timeout and ping frames, `proxy_read_timeout` semantics.
Removed as unconfirmed: the `Host` header line, the 3600s timeout, advice on keepalive in a separate location, cloud load balancer timeouts, ip_hash affinity, the `proxy_buffering` remark, and the curl 101 verify step.
Method: documentation only; no commands were run.
