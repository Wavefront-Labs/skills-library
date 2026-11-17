---
id: computing-software.database-administration.pgbouncer.zero-downtime-rolling-restart
name: zero-downtime-rolling-restart
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, rolling-restart, upgrade, so-reuseport, wait-for-clients]
level: sme
status: docs-checked
description: "Upgrade or restart PgBouncer without dropping connections using several processes on one port and SHUTDOWN WAIT_FOR_CLIENTS."
sources:
  - https://www.pgbouncer.org/usage.html
  - https://www.pgbouncer.org/faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restart or upgrade PgBouncer with zero downtime.

The FAQ answer to "how to upgrade PgBouncer without dropping connections" is the rolling restart described for `SHUTDOWN WAIT_FOR_CLIENTS`.

Prerequisite: two or more PgBouncer processes on the same port using `so_reuseport` (peering is recommended but not required). Restart them one by one so the others keep accepting connections.

Procedure:

1. Pick a process to restart first, call it A.
2. Run `SHUTDOWN WAIT_FOR_CLIENTS;` on A (or send it SIGTERM). A stops accepting new connections.
3. Cause all clients to reconnect. Either wait until a client-side pooler reconnects because of its own server_idle_timeout (or similar setting), or, if there is no client-side pooler, restart the clients.
4. Once all clients have reconnected elsewhere, A exits automatically because no clients remain.
5. Start A again (with the new binary or config).
6. Repeat steps 2 to 5 for each remaining process.

Notes: the Unix socket of a draining process stays open but only for admin console connections. Each process on the same host needs its own unix_socket_dir and pidfile (and logfile).

Version detail: SIGTERM means safe shutdown since 1.23.0; earlier versions treat it as immediate, so use the console command there.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. Removed: an inferred sentence about using the Unix socket for console access.

Method: documentation only; no commands were run.
