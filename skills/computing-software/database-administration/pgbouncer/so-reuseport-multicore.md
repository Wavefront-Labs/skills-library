---
id: computing-software.database-administration.pgbouncer.so-reuseport-multicore
name: so-reuseport-multicore
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, so-reuseport, multicore, peering, performance]
level: sme
status: docs-checked
description: "Run several PgBouncer processes on one port with so_reuseport and peering to use multiple CPU cores."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use more than one CPU core, since PgBouncer is single-threaded.

`so_reuseport` (default 0) sets SO_REUSEPORT on TCP listening sockets so multiple instances on one host can share a port and the kernel spreads connections. It works as intended on sufficiently recent Linux, DragonFlyBSD and FreeBSD (where SO_REUSEPORT_LB is used). Some other operating systems accept the option but only one process receives connections. On systems without the option, enabling it causes an error.

Each instance on the same host needs different `unix_socket_dir` and `pidfile`, and different `logfile` if used. You can no longer connect to a specific instance over TCP/IP, which affects monitoring and metrics. Set up peering so query cancellations keep working.

First process:

```
[databases]
postgres = host=localhost dbname=postgres
[peers]
1 = host=/tmp/pgbouncer1
2 = host=/tmp/pgbouncer2
[pgbouncer]
listen_addr=127.0.0.1
auth_file=auth_file.conf
so_reuseport=1
unix_socket_dir=/tmp/pgbouncer1
peer_id=1
```

The second process is identical except `unix_socket_dir=/tmp/pgbouncer2` and `peer_id=2`.

The same pattern enables a zero-downtime rolling restart with SHUTDOWN WAIT_FOR_CLIENTS. Prepared-statement tracking also costs CPU, which this approach spreads.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
