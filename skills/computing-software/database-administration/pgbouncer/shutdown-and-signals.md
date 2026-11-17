---
id: computing-software.database-administration.pgbouncer.shutdown-and-signals
name: shutdown-and-signals
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, shutdown, signals, sigterm, sigint]
level: practitioner
status: docs-checked
description: "SHUTDOWN, SHUTDOWN WAIT_FOR_SERVERS and WAIT_FOR_CLIENTS, plus SIGHUP, SIGTERM, SIGINT, SIGQUIT, SIGUSR1 and SIGUSR2."
sources:
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop PgBouncer in the right way.

Console commands:

- `SHUTDOWN;`: the process exits immediately.
- `SHUTDOWN WAIT_FOR_SERVERS;`: stop accepting new connections and exit after all servers are released. Basically PAUSE then SHUTDOWN, but it also stops accepting new connections during the pause and eagerly disconnects clients waiting for a server. Unix sockets stay open but accept only admin console connections.
- `SHUTDOWN WAIT_FOR_CLIENTS;`: stop accepting new connections and exit once all existing clients have disconnected. Unix sockets stay open for the admin console only.

Signals:

- SIGHUP: reload config, same as RELOAD.
- SIGTERM: "super safe shutdown", same as SHUTDOWN WAIT_FOR_CLIENTS. If already shutting down, an immediate shutdown is triggered. In versions before 1.23.0, SIGTERM caused an immediate shutdown.
- SIGINT: safe shutdown, same as SHUTDOWN WAIT_FOR_SERVERS; if a shutdown is already in progress, immediate shutdown.
- SIGQUIT: immediate shutdown, same as SHUTDOWN.
- SIGUSR1: same as PAUSE.
- SIGUSR2: same as RESUME.

The shutdown-in-progress escalation means sending a second SIGTERM or SIGINT stops the process immediately.

```
kill -TERM $(cat /path/to/pgbouncer.pid)
```

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
