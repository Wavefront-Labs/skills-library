---
id: computing-software.networking-hardware-and-wireless.haproxy.per-ip-rate-limiting
name: per-ip-rate-limiting
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, rate-limiting, http-req-rate, conn-cur, 429-too-many-requests, per-ip-limit]
level: practitioner
status: docs-checked
description: "Limit request rate and concurrent connections per client IP in HAProxy using stick tables, track-sc, deny_status 429 and gpc0 counters."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# per ip rate limiting
Pattern: track by source address in a stick table, compare the counters, deny.

```
backend st_rl
    stick-table type ip size 500k expire 1m store http_req_rate(10s),conn_cur,gpc0
frontend fe_web
    bind :443 ssl crt /etc/haproxy/certs/
    http-request track-sc0 src table st_rl
    acl too_fast sc_http_req_rate(0,st_rl) gt 200
    acl too_many sc_conn_cur(0,st_rl) gt 50
    http-request deny deny_status 429 if too_fast || too_many
```
- `deny` ends rule evaluation and rejects the request; `deny_status` sets the status code (default for requests is 403). It implies `default-errorfiles`, so an `errorfile 429` can supply the body; use `http-request return` for full control, including headers such as `Retry-After` (`hdr <name> <fmt>`).
- A second tier for a path uses another counter set and table, for example `http-request track-sc1 src table st_login if { path_beg /login }` with a separate table and its own threshold.
- `sc_http_req_rate` counts every started request, valid or not, and `sc_conn_cur` counts concurrent connections tracking the same entry, so the sc0 rate and connection count are read from the tracked entry.
- To count only failures, store `http_err_rate(<period>)` (errors from the client side: invalid, denied, tarpitted requests, failed authentication, server 4xx), or increment `gpc0` with `http-response sc-inc-gpc0(0)` under a condition of your choice and ban when it passes a threshold.
- Behind a trusted proxy, key the table on the client address from the proxy header instead of `src`, for example `req.hdr_ip(x-forwarded-for,-1)` (last value); this is only safe when the upstream is trusted.

Gotchas: hosts behind NAT share one source address, so whitelist them or give them a higher limit (for instance `tcp-request connection accept if { src -f <file> }` before tracking). A client that keeps sending stays above the rate while denied requests are still counted.

Verify: send a burst above the threshold and confirm 429 responses; `show table st_rl` on the runtime API lists `http_req_rate` and `conn_cur` per key.

## Checked
2026-11-03. Confirmed against configuration.html: `stick-table` data types, `http-request track-sc*`, `deny`/`deny_status`, `return`, `sc_http_req_rate`, `sc_conn_cur`, `sc-inc-gpc0`, `tcp-request connection accept/track-sc0` example, `req.hdr_ip` example and `http_err_cnt` definition. Removed: the `/etc/haproxy/errors/429.http` Retry-After instruction (replaced with `return hdr`) and the `ab` benchmark verify command. The claim that a denied flood keeps itself blocked is kept only as far as the docs support it (denied requests still count as started requests).
Method: documentation only; no commands were run.
