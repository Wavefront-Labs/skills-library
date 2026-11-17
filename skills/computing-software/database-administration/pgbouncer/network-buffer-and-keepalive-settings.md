---
id: computing-software.database-administration.pgbouncer.network-buffer-and-keepalive-settings
name: network-buffer-and-keepalive-settings
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, pkt-buf, tcp-keepalive, sbuf-loopcnt, network]
level: advanced
status: docs-checked
description: "pkt_buf, max_packet_size, sbuf_loopcnt, tcp_keepalive, tcp_keepidle, tcp_keepintvl, tcp_keepcnt, tcp_user_timeout, tcp_defer_accept."
sources:
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune low-level network behaviour.

- `pkt_buf` (default 4096): internal packet buffer size; affects TCP packet size and memory use. libpq packets can be larger, so no need to set it large.
- `max_packet_size` (default 2147483647): largest PostgreSQL packet allowed through. One packet is one query or one result set row; the full result set can be larger.
- `sbuf_loopcnt` (default 5): times to process data on one connection before moving on, so one big result set cannot stall PgBouncer. One loop handles one pkt_buf of data. 0 means no limit.
- `tcp_keepalive` (default 1): basic keepalive with OS defaults. Linux defaults are tcp_keepidle=7200, tcp_keepintvl=75, tcp_keepcnt=9.
- `tcp_keepidle`, `tcp_keepintvl`, `tcp_keepcnt`, `tcp_socket_buffer`: default not set.
- `tcp_user_timeout` (default 0): sets TCP_USER_TIMEOUT in milliseconds, the longest transmitted data may remain unacknowledged before the connection is closed. 0 uses the OS default. Linux only.
- `tcp_defer_accept` (default 1 on Linux, otherwise 0): Boolean; sets TCP_DEFER_ACCEPT, with the value hardcoded to 45 seconds when enabled. Linux only.
- `listen_backlog` (default 128): listen(2) backlog; further attempts are dropped when the queue is full.
- `disable_pqexec` (default 0): disables the Simple Query protocol (PQexec), which allows multiple queries per packet and certain SQL injection classes. Only clients exclusively using Extended Query keep working.

```
tcp_keepidle = 60
tcp_keepintvl = 10
tcp_keepcnt = 5
```

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
