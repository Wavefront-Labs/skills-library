---
id: computing-software.database-administration.pgbouncer.pause-resume-disable-enable
name: pause-resume-disable-enable
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, pause, resume, disable, enable]
level: practitioner
status: docs-checked
description: "Console commands PAUSE, RESUME, DISABLE and ENABLE: draining servers for a database restart and blocking new clients."
sources:
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control traffic flow without restarting PgBouncer.

- `PAUSE [db];`: PgBouncer tries to disconnect from all servers (or only the named database). Each server connection is released according to the pooling mode: the transaction must finish in transaction mode, the statement in statement mode, and the client must disconnect in session mode. The command does not return until all server connections are disconnected. Intended for database restarts. New client connections to a paused database wait until RESUME.
- `RESUME [db];`: resume after PAUSE or KILL.
- `DISABLE db;`: reject all new client connections on that database.
- `ENABLE db;`: allow new client connections again after DISABLE.

Typical database restart:

```
PAUSE;
-- restart or fail over PostgreSQL
RESUME;
```

SHOW DATABASES exposes `paused` and `disabled` flags per database, and SHOW STATE reports the process-level state (active or paused).

Signals: SIGUSR1 equals PAUSE and SIGUSR2 equals RESUME.

For a server whose address changes, RECONNECT or RELOAD may suffice instead; the docs say that if all connections must switch at the same time, PAUSE is recommended over RECONNECT.

In session pooling PAUSE waits for clients to disconnect, so a long session can stall it. KILL is the immediate alternative.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
