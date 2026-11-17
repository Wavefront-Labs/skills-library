---
id: computing-software.networking-hardware-and-wireless.haproxy.websocket-and-long-lived-connections
name: websocket-and-long-lived-connections
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, websocket, timeout-tunnel, upgrade-header, long-lived-connections]
level: practitioner
status: docs-checked
description: "Keep websocket and other long-lived streams alive through HAProxy with timeout tunnel, upgrade ACLs, keepalives and the ws option."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# websocket and long lived connections
When a connection is upgraded (for example to WebSocket, or a CONNECT request is forwarded), HAProxy treats it as a tunnel and `timeout tunnel` supersedes the client and server timeouts. In HTTP mode the tunnel timeout also applies after the first response when no keep-alive or close option is specified.

```
frontend fe_web
    bind :443 ssl crt /etc/haproxy/certs/
    acl is_ws_path path_beg /ws/
    use_backend be_ws if is_ws_path
    option clitcpka
backend be_ws
    balance leastconn
    timeout tunnel 2h
    option srvtcpka
    server ws1 10.0.0.21:9000 check
```
- `timeout tunnel` is not allowed in a frontend; it is specific to backends, and can be set once in `defaults`, which the manual calls one of the easiest ways not to forget it.
- The manual advises also setting `timeout client-fin` for long-lived connections, so a client that disappears without acknowledging a close does not leave sessions piling up in FIN_WAIT.
- Choose timeouts slightly above multiples of 3 seconds (for example 4 or 5 seconds minimum) so they survive TCP packet loss.
- `option clitcpka` (frontend side) and `option srvtcpka` (backend side) enable socket-level TCP keep-alives to stop session-aware middleboxes expiring idle sessions. The probe interval is controlled by the operating system, not HAProxy.
- The server-line `ws { auto | h1 | h2 }` option sets the protocol used to relay websocket streams; it matters mostly with HTTP/2 backends that lack RFC 8441 websocket support (`h2` needs a server that supports RFC 8441).
- `hard-stop-after <time>` in `global` caps how long a soft-stopping (SIGUSR1) instance stays alive while connections remain open, so decide deliberately whether to bound old long-lived streams, and expect clients to reconnect.

Verify: a websocket client stays connected past the value of `timeout server` and the `timeout client`, and is only closed after `timeout tunnel` of inactivity.

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 configuration manual: `timeout tunnel` (when it applies, backend-only, defaults, `timeout client-fin` advice, multiples-of-3-seconds advice), `option clitcpka` and `option srvtcpka` (sections and purpose), `ws` server option, `hard-stop-after`. Removed: the claim that without `timeout tunnel` the socket dies after 30-60 seconds, the claim that app ping/pong is the dependable fix, the SSE and gRPC paragraph, `option http-server-close` and `wscat`/`show sess` verification. Also removed: the `hdr(Upgrade)` ACL. `path_beg`, `use_backend` and `balance leastconn` are documented keywords. Read as sections of the manual only.
Method: documentation only; no commands were run.
