---
id: computing-software.networking-hardware-and-wireless.haproxy.tarpit-and-scanner-defence
name: tarpit-and-scanner-defence
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, tarpit, silent-drop, ban-ip, gpc0, scanner-blocking]
level: practitioner
status: docs-checked
description: "Slow and deny abusive HAProxy clients with tarpit, silent-drop, deny lists, bad-request tracking and ban windows using general purpose counters."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tarpit and scanner defence
`http-request tarpit` holds the client connection without answering for `timeout tarpit` (if unset, the backend's `timeout connect` is used), then returns a response so the client does not suspect it was tarpitted. The default status is 500; `status <code>` or `deny_status <code>` changes it. Logs show the `PT` termination flags. It is efficient against dumb robots and cheaper for firewalls than `deny`, but against well-written robots it can make things worse, because HAProxy and the front firewall must carry a huge number of concurrent connections.

```
backend st_ban
    stick-table type ip size 200k expire 1h store gpc0,http_req_rate(1m),http_err_rate(1m)
frontend fe_web
    timeout tarpit 10s
    http-request track-sc0 src table st_ban
    acl is_banned sc_get_gpc0(0,st_ban) gt 0
    acl scanner path_reg -i (wp-login|\.env|phpmyadmin|\.git/)
    http-request sc-inc-gpc0(0) if scanner
    http-request silent-drop if is_banned
    http-request tarpit deny_status 429 if scanner
    http-request deny deny_status 403 if { sc_http_err_rate(0,st_ban) gt 20 }
```
- `track-sc0` does not stop rule evaluation, and the counters it tracks are read by later `sc_*` fetches, so keep it before the rules that read them.
- `sc-inc-gpc0(<sc-id>)` increments the legacy `gpc0` counter of the tracked set; it needs `gpc0` in the table's `store` list.
- `type ip` tables store IPv4 addresses only; use `type ipv6` for IPv6 clients. `expire` is refreshed when an entry is updated through `track-sc`.
- `silent-drop` makes the client-facing connection disappear without telling the client: it tries to avoid sending any FIN or RST (using TCP_REPAIR), and falls back to an RST with TTL 1 if that fails (for example missing privileges). The client still sees an established connection, but stateful equipment between HAProxy and the client keeps it in its session table. `rst-ttl <ttl>` changes this behaviour; the docs say not to use it unless the consequences are understood.
- If a proxy or CDN in front rewrites the source address, `http-request set-src <expr>` (for example `hdr(x-forwarded-for)`) makes later `src` fetches return the real client address; otherwise you ban the proxy. Only do this when the header is trusted.
- Check that tarpit rules do not hit valid requests: the `CT` flags mean the client aborted while tarpitted, and the docs suggest lowering `timeout tarpit` toward the average `Tw` timer if many do.

Verify: request `/.env` repeatedly and read the table on the runtime API (`show table st_ban`); the `gpc0` value for your address rises and later requests are dropped.

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 configuration manual: `tarpit` action (default 500, `timeout tarpit` fallback to `timeout connect`, `PT` flags, firewall caveat, no further rules evaluated), `silent-drop` and `rst-ttl` behaviour, `track-sc0` semantics, `sc-inc-gpc0`, `sc_get_gpc0`, `sc_http_err_rate`, `set-src`, `stick-table` types and data types (`gpc0`, `http_req_rate`, `http_err_rate`), `expire`, `path_reg` and `CT` termination flags. Removed: the claims that silent-drop only works on real connections and that a separate tracking table is needed to keep a ban window, the allow-list advice using `src -f` file, and the `curl` verify detail "banned IP is dropped" beyond what the docs state. Read as partial sections (the manual is about 1.4 MB of text); sections not cited above were not read.
Method: documentation only; no commands were run.
