---
id: computing-software.cloud-infrastructure-engineering.nginx.keepalive-timeouts-client
name: keepalive-timeouts-client
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, keepalive-timeout, keepalive-requests, client-connections, idle]
level: practitioner
status: docs-checked
description: "Client-side keepalive in nginx: keepalive_timeout 75s default, keepalive_requests, keepalive_time, send_timeout and reset_timedout_connection."
sources: ["https://nginx.org/en/docs/http/ngx_http_core_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Defaults and meanings from the `ngx_http_core_module` page (all valid in `http`, `server`, `location`):

- `keepalive_timeout timeout [header_timeout];` default `75s`. The first value is how long an idle client connection stays open; `0` disables keep-alive. The optional second value sets the `Keep-Alive: timeout=` response header.
- `keepalive_requests number;` default `1000` (it was `100` before 1.19.10): maximum requests per keep-alive connection. Closing periodically frees per-connection memory, so a very high value is not recommended.
- `keepalive_time time;` default `1h` (1.19.10): maximum time requests can be processed through one connection; after it is reached the connection is closed following the next request.
- `keepalive_min_timeout timeout;` default `0` (1.27.4): time during which a keep-alive connection is not closed server-side for reuse or on graceful worker shutdown.
- `send_timeout time;` default `60s`: timeout between two successive write operations when sending a response; if the client receives nothing in that time the connection is closed.
- `reset_timedout_connection on | off;` default `off`: sets `SO_LINGER` with timeout 0 before closing so TCP RST is sent and the socket's memory is freed immediately instead of lingering in `FIN_WAIT1`.

```nginx
keepalive_timeout  30s 25s;
keepalive_requests 1000;
send_timeout       30s;
reset_timedout_connection on;
```

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_core_module` page for each directive, default and version note above. Removed: cloud load balancer idle-timeout advice, HTTP/2 and HTTP/3 idle claims (including the "confirm" marker), connection slot arithmetic, and the curl/ss Verify step.
Method: documentation only; no commands were run.
