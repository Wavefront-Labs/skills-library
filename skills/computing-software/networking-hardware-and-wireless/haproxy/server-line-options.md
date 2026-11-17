---
id: computing-software.networking-hardware-and-wireless.haproxy.server-line-options
name: server-line-options
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, server-line, inter-rise-fall, slowstart, backup-server, maxconn-server, server-template]
level: practitioner
status: docs-checked
description: "Configure HAProxy server lines: check, inter/rise/fall, weight, maxconn, backup, slowstart, verify, send-proxy, init-addr and server-template."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# server line options
```
backend be_app
    default-server inter 3s fall 3 rise 2 slowstart 30s maxconn 200
    server a 10.0.0.11:8080 check
    server b 10.0.0.12:8080 check weight 50
    server c 10.0.0.13:8080 check backup
    server s1 10.0.0.20:8443 check ssl verify required ca-file /etc/haproxy/ca.pem sni req.hdr(host)
```
`default-server` sets parameters shared by the servers of a backend; the same options as on `server` apply (manual section 5).

- `check`: without it no health checking is done and the server is always considered available. With it and no other method, the server is up when a connection can be made at the highest configured transport layer (TCP, or TLS when `ssl` or `check-ssl` is set), optionally preceded by a PROXY header. Setting `addr` or `port` for checks stops the encapsulation parameters being reused; then set `check-ssl` and `check-send-proxy` explicitly.
- `inter <delay>` defaults to 2000 ms and also acts as the check timeout when `timeout check` is unset. `fastinter` applies while a server is transitioning or unchecked; `downinter` applies while fully down (each falls back to `inter`).
- `fall <count>` (default 3) consecutive failures mark a server down; `rise <count>` (default 2) consecutive successes mark it up.
- `weight` defaults to 1, maximum 256; 0 removes the server from load balancing but it still accepts persistent connections. The manual suggests starting between 10 and 100 to leave room to adjust.
- `maxconn` (default 0 = unlimited) queues connections above the limit and protects fragile servers. In HTTP mode it limits concurrent requests, not connections. `maxqueue` (default 0 = unlimited) redispatches extra requests to other servers, which breaks persistence.
- `backup`: used only when all non-backup servers are unavailable, though requests with a persistence cookie for that server are still served. Only the first operational backup is used unless `allbackups` is set in the backend.
- `slowstart <time>`: after a server comes back from failure, its maxconn (and its weight for dynamic weighted algorithms) grows linearly from near zero to full over that time. Keep `inter` smaller than `slowstart`. It never applies at HAProxy startup.
- `disabled` starts the server in maintenance (no traffic except via persist mode), good for introducing new servers; `enabled` cancels an inherited `disabled`.
- `on-marked-down shutdown-sessions` terminates all connections to the server when it goes down; those are logged with termination code `D`. `on-marked-up shutdown-backup-sessions` kills streams on backup servers when an active server returns (logged `U`); the manual says to use it with extreme care.
- `ssl` plus `verify required` (the default unless the global `ssl_server_verify` says otherwise) checks the server certificate against `ca-file` and the names from `sni` or `verifyhost`. Without SNI use `verifyhost`. `verify none` disables verification, which exposes you to trivial man-in-the-middle attacks. `ca-file @system-ca` uses the system CAs.
- `sni <expression>` sets the SNI sent to the server. The manual says not to use it for HTTPS with `ssl_fc_sni`; use `req.hdr(host)` instead because SNI must match the Host field.
- `send-proxy` sends a PROXY protocol header on connections to the server (only when the server understands it); health checks use it automatically unless `port` or `addr` is set, in which case add `check-send-proxy`.
- `init-addr {last | libc | none | <ip>},...` sets how an FQDN is resolved at startup; default `last,libc`. `none` starts the server down with no address; if every method fails an error is raised.
- `server-template <prefix> <num|range> <fqdn>[:<port>] [params*]` (backend and listen only) creates servers named `<prefix>1` up to `<prefix><num>` (or the given range) sharing one FQDN and parameters, for example `server-template srv 1-3 google.com:80 check`.
- `cookie <value>` assigns the persistence cookie value for the server; several servers may share one value.

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 configuration manual: `server-template`, `default-server`, and the server keywords `backup`, `ca-file`, `check`, `cookie`, `disabled`/`enabled`, `fall`, `rise`, `inter`/`fastinter`/`downinter`, `init-addr`, `maxconn`, `maxqueue`, `on-marked-down`, `on-marked-up`, `send-proxy`, `slowstart`, `sni`, `verify`, `verifyhost`, `weight`. Removed: the claim that a server without `check` causes mid-request 503s, the `agent-check` summary (covered by another skill), `show servers state` and `fall * inter` verification, and the explicit `server` line syntax. Read as sections of the manual only.
Method: documentation only; no commands were run.
