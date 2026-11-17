---
id: computing-software.networking-hardware-and-wireless.caddy.reverse-proxy-streaming-websockets-buffering
name: reverse-proxy-streaming-websockets-buffering
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [flush-interval, websocket, request-buffers, response-buffers, stream-timeout, stream-close-delay, sse, reverse-proxy]
level: advanced
status: docs-checked
description: "Tune reverse_proxy streaming: flush_interval low-latency mode, request and response buffers, WebSocket close behaviour on reload, stream_timeout and Incremental handling."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control buffering and long-lived connections.

By default the proxy partially buffers responses. WebSockets are supported: the upgrade is performed and the connection becomes a bidirectional tunnel. On config reload WebSockets are forcibly closed (Close sent to client and upstream) because each holds a config reference; tune this with `stream_timeout` and `stream_close_delay`.

- `flush_interval <duration>`: default no periodic flush. A negative value (typically -1) means low-latency mode: no buffering, flush after every write, and the backend request continues even if the client leaves. It is ignored (immediate flush) for `Content-Type: text/event-stream`, `Incremental: ?1`, unknown `Content-Length`, and HTTP/2 on both sides with unknown length and no or identity `Accept-Encoding`.
- `request_buffers <size>`: read up to this much of the body before sending upstream; inefficient, only for upstreams that need it; `unlimited` buffers all and sets `Content-Length` (required by fastcgi for bodies lacking it).
- `response_buffers <size>`: buffer response bytes; avoid unless the backend has tight memory limits.
- `stream_timeout`: forcibly close streams after this long; the page suggests `24h`; default none.
- `stream_close_delay`: keep streams open this long after a reload to avoid a thundering herd; suggested `5m`; default none.
- `proxy_status_name`: name in the `Proxy-Status` header when Caddy refuses an `Incremental: ?1` message with `501` (Caddy 2.11.7 or newer).

## Checked
2026-11-03. Confirmed against the Caddy reverse_proxy directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
