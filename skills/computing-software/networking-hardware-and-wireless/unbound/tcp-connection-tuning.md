---
id: computing-software.networking-hardware-and-wireless.unbound.tcp-connection-tuning
name: tcp-connection-tuning
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, tcp-idle-timeout, edns-tcp-keepalive, incoming-num-tcp, tcp-connection-limit]
level: advanced
status: docs-checked
description: "Tune Unbound TCP handling: buffers, idle and keepalive timeouts, upstream connection reuse and per-netblock connection limits."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/core/performance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tcp connection tuning
Buffers per thread: `incoming-num-tcp` and `outgoing-num-tcp` (default 10 each). 0 or `do-tcp: no` means no TCP in that direction. `stream-wait-size` (default 4m) caps memory for queued TCP/TLS response buffers.

Client side:
- `tcp-idle-timeout` (30000 ms) is the idle wait for a query; it shrinks under buffer pressure, with a 200 ms floor.
- `edns-tcp-keepalive: yes` (default no) enables EDNS TCP Keepalive; `edns-tcp-keepalive-timeout` (120000 ms) is sent to supporting clients and overrides the idle timeout.
- `tcp-connection-limit` limits simultaneous connections per netblock; excess ones are closed immediately (experimental, disabled by default).

Upstream side:
- `tcp-reuse-timeout` (60000 ms) keeps persistent connections to authorities open.
- `max-reuse-tcp-queries` (200) caps queries per persistent connection.
- `tcp-auth-query-timeout` (3000 ms) is the TCP query timeout to auth servers.

Linux TCP listen backlog is requested at about 256 and silently capped by the kernel; raise `net.core.somaxconn` and `net.ipv4.tcp_max_syn_backlog` for more.

## Checked
2026-11-04. Confirmed against the unbound.conf manual and the performance page: TCP buffer, timeout and reuse options with their defaults, the 200 ms idle-timeout floor, tcp-connection-limit wording and the Linux backlog note. Nothing removed.
Method: documentation only; no commands were run.
