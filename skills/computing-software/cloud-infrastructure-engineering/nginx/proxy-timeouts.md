---
id: computing-software.cloud-infrastructure-engineering.nginx.proxy-timeouts
name: proxy-timeouts
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, proxy-timeouts, proxy-read-timeout, timeouts]
level: practitioner
status: docs-checked
description: "proxy_connect_timeout, proxy_send_timeout and proxy_read_timeout: what each measures, their 60s defaults, and why read and send are per-operation gaps."
sources: ["https://nginx.org/en/docs/http/ngx_http_proxy_module.html", "https://nginx.org/en/docs/http/websocket.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Three directives bound backend interaction, each defaulting to `60s`:

```nginx
proxy_connect_timeout 5s;    # establishing a connection with the proxied server
proxy_send_timeout    30s;   # between two successive writes of the request
proxy_read_timeout    30s;   # between two successive reads of the response
```

- `proxy_send_timeout` and `proxy_read_timeout` apply between two successive write or read operations, not to the whole transmission. If nothing is sent or received within the time, the connection is closed. A response that trickles a byte every 59 seconds therefore never times out under a 60s read timeout.
- The docs note that `proxy_connect_timeout` cannot usually exceed 75 seconds.
- Long-lived responses (for example WebSockets) need a larger `proxy_read_timeout`, or the proxied server must send data periodically (WebSocket ping frames); the WebSocket page notes the 60 second default closes idle tunnels.
- A timeout is a condition for `proxy_next_upstream` (`timeout`, on by default), so a timed-out request can go to the next server within `proxy_next_upstream_tries` / `proxy_next_upstream_timeout`.

## Checked
Date: 2026-11-03.
Confirmed in the ngx_http_proxy_module page: all three directives, defaults, per-operation wording, 75 second note, `proxy_next_upstream` default. Confirmed in the websocket page: the 60 second idle close and ping frames.
Removed as unconfirmed: the 502 versus 504 mapping, the "confirm" 75 second claim about builds, the shorter-connect-timeout failover advice, and the kill -STOP verify step.
Method: documentation only; no commands were run.
