---
id: computing-software.networking-hardware-and-wireless.haproxy.http2-and-alpn
name: http2-and-alpn
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, http2, alpn-h2, h2-stream-limit, tune-h2, http2-backend]
level: practitioner
status: docs-checked
description: "Enable HTTP/2 on HAProxy frontends and backends with alpn h2, force protocols with proto, and tune the tune.h2 stream and window limits."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http2 and alpn
```
frontend fe_web
    bind :443 ssl crt /etc/haproxy/certs/ alpn h2,http/1.1
backend be_h2
    server app 10.0.0.11:8443 ssl verify required ca-file ca.pem alpn h2 check-alpn h2
```
- Bind `alpn <protocols>` enables the TLS ALPN extension with a comma-delimited list. ALPN is required to enable HTTP/2 on an HTTPS frontend. If a frontend has none of `npn`, `alpn` or `no-alpn`, the default `h2,http/1.1` is used for a regular HTTPS frontend. Protocols not advertised are not negotiated, so `alpn h2` alone refuses HTTP/1.1. A later `alpn` replaces an earlier one; `no-alpn` removes it.
- Server `alpn <protocols>` is required to connect to HTTP/2 servers; to support both, advertise `h2,http/1.1` in order of preference. `check-alpn <protocols>` sets the ALPN for health checks (the server ALPN is used if unset).
- `proto <name>` on a bind or server line forces the multiplexer protocol (for example `h2`); it must be compatible with the proxy mode and usable on that side, and the available protocols are listed by `haproxy -vv`. `h2` is flagged `HOL_RISK` (head-of-line blocking risk) and `NO_UPG`.
- Some old browsers (Firefox 88) had trouble with WebSocket over H2; the manual says to force `http/1.1` or `no-alpn` in the `alpn` string, or enable `h2-workaround-bogus-websocket-clients` globally. The server option `ws { auto | h1 | h2 }` selects the protocol used for websocket streams.
- Tuning in `global`: `tune.h2.max-concurrent-streams` (default 100; 0 disables the limit) with per-side `tune.h2.fe.max-concurrent-streams` and `tune.h2.be.max-concurrent-streams`; `tune.h2.initial-window-size` (default 65536) with `tune.h2.fe.initial-window-size` and `tune.h2.be.initial-window-size`; `tune.h2.header-table-size` (default 4096, at most 65536); `tune.h2.max-frame-size`; `tune.h2.fe.max-total-streams` (default 0 = no limit; sends GOAWAY after that many streams so clients reconnect); `tune.h2.fe.glitches-threshold` and `tune.h2.be.glitches-threshold` (default 0 = off). The manual recommends not changing most of these and preferring the per-side settings over the generic ones.
- With `http-reuse always` on an H2 backend the manual recommends reducing `tune.h2.be.max-concurrent-streams` (and keeping `tune.h2.be.initial-window-size` low), because head-of-line blocking lets one slow client slow others sharing a connection.
- HTTP/2 requires `tune.bufsize` to be 16384 or more.

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 configuration manual: bind and server `alpn`, `check-alpn`, `proto` (bind and server), the `tune.h2.*` keywords and defaults listed above, `ws`, `h2-workaround-bogus-websocket-clients` and the `tune.bufsize` HTTP/2 requirement. Removed: the h2c "prior-knowledge" claim, the gRPC paragraph, `option http-use-htx`, the `option abortonclose` remark, the `maxconn`/`balance source`/stick-table gotcha, and the `curl --http2`/`%HV` verification. Read as sections of the manual only.
Method: documentation only; no commands were run.
