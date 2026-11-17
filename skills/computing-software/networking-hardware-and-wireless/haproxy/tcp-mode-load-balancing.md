---
id: computing-software.networking-hardware-and-wireless.haproxy.tcp-mode-load-balancing
name: tcp-mode-load-balancing
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, mode-tcp, tcplog, tcp-request, layer4-load-balancing, postgres-load-balancing]
level: practitioner
status: docs-checked
description: "Load balance non-HTTP traffic with mode tcp using option tcplog, tcp-request rules, option tcpka, long timeouts and on-marked-down."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tcp mode load balancing
`mode tcp` is the default mode: a full-duplex connection is built between client and server with no layer 7 examination, suited to SSL, SSH, SMTP and similar. HTTP headers, cookies and HTTP ACLs are unavailable.

```
listen pg
    bind :5432
    mode tcp
    option tcplog
    option tcpka
    balance leastconn
    timeout connect 3s
    timeout client 1h
    timeout server 1h
    default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions
    server pg1 10.0.1.1:5432 check
    server pg2 10.0.1.2:5432 check backup
```
- `option tcplog` gives a richer log line (timers, stream state, connection counts, frontend, backend and server) and is the choice for pure TCP proxies; use `option httplog` for HTTP. It overrides any earlier `log-format`.
- `option tcpka` enables TCP keep-alive probes on both sides, for sessions with long idle periods behind session-aware firewalls (remote desktops, for instance). It is meaningful only in `defaults` or `listen` sections; in a frontend only the client side gets probes, in a backend only the server side. Probe timing is set by the operating system.
- `on-marked-down shutdown-sessions` immediately terminates all connections to a server that goes down, useful when a check detects a case (such as a stuck database) where long timeouts would leave the service unresponsive. Such connections are logged with the `D` termination code.
- `leastconn` suits long sessions such as databases (see the balance skill); `balance`, `backup` and `check` behave as in HTTP mode.
- Layer 4 rules: `tcp-request connection reject if { src_conn_rate gt 10 }` with `tcp-request connection track-sc0 src`; `tcp-request inspect-delay` plus `tcp-request content accept|reject` act on payload, for example rejecting an SMTP connection if the client speaks first (`tcp-request content reject if { req.len gt 0 }`).
- A frontend and its backend must use the same mode when content switching, except that a TCP frontend may switch to an HTTP backend (see the `use_backend` description).

Gotcha: long-lived streams need `timeout client` and `timeout server` above their idle time, and `timeout tunnel` overrides them once a connection becomes a tunnel; the docs recommend keeping client and server timeouts equal in TCP mode.

Verify: `haproxy -c -f <config>`, then connect through the listener and confirm the `tcplog` line names the expected server.

## Checked
2026-11-03. Confirmed against configuration.html: `mode`, `option tcplog`, `option tcpka`, `on-marked-down`, `timeout client/server/tunnel`, `tcp-request connection`, `tcp-request content` examples and `use_backend`. Removed: the Postgres `tcp-check send-binary` bytes, the Patroni `httpchk /primary` pattern and port 8008, `check port` use, "HTTP defaults kill idle DB connections at 30s" (no default exists; unset means infinite), the `req.payload(0,3)` rule, and the `psql` verify.
Method: documentation only; no commands were run.
