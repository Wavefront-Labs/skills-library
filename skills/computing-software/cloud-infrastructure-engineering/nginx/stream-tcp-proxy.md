---
id: computing-software.cloud-infrastructure-engineering.nginx.stream-tcp-proxy
name: stream-tcp-proxy
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, stream, tcp, udp, l4-proxy]
level: practitioner
status: docs-checked
description: "Proxying raw TCP and UDP with nginx stream blocks: listen, proxy_pass to an upstream, timeouts, UDP reuseport and proxy_responses, and stream logging."
sources: ["https://nginx.org/en/docs/stream/ngx_stream_core_module.html", "https://nginx.org/en/docs/stream/ngx_stream_proxy_module.html", "https://nginx.org/en/docs/stream/ngx_stream_upstream_module.html", "https://nginx.org/en/docs/stream/ngx_stream_log_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `stream` context proxies TCP and UDP. `ngx_stream_core_module` (1.9.0) is not built by default and needs `--with-stream`.

```nginx
stream {
    upstream pg { server 10.0.0.5:5432; server 10.0.0.6:5432 backup; }
    server {
        listen 5432;
        proxy_pass pg;
        proxy_connect_timeout 3s;    # default 60s
        proxy_timeout 10m;           # default 10m
    }
    server {
        listen 53 udp reuseport;
        proxy_pass 10.0.0.2:53;
        proxy_responses 1;
    }
}
```

- `proxy_timeout` is the timeout between two successive read or write operations on the client or proxied connection; with no data in that time the connection is closed.
- A `backup` server in a stream upstream receives connections when the primary servers are unavailable. Stream upstream servers need an explicit port.
- The `udp` parameter of `listen` handles datagrams; to keep packets from one address and port in the same session, also specify `reuseport`.
- `proxy_responses` is the number of datagrams expected from the proxied server in response to a client datagram, a hint for session termination; 0 means no response is expected. Unlimited by default.
- `listen ... so_keepalive=on|off|[keepidle]:[keepintvl]:[keepcnt]` configures TCP keepalive on the listening socket.
- Stream logging uses `ngx_stream_log_module`: `log_format name string ...;` in `stream`, then `access_log path format;`. Stream variables include `$remote_addr`, `$bytes_sent` and `$session_time`.
- `proxy_protocol on;` in a stream `server` sends a PROXY protocol v1 header to the proxied server so it can learn the client address.

## Checked
Date: 2026-11-03.
Confirmed in the stream core, proxy, upstream and log module pages: build flag, directives, defaults, udp/reuseport, proxy_responses, so_keepalive, log directives and variables.
Removed as unconfirmed: the dynamic-module remark, "no virtual hosting without SNI", and the nginx -V / nc / ss verify step.
Method: documentation only; no commands were run.
