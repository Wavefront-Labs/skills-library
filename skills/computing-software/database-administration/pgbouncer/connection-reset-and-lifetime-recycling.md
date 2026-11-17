---
id: computing-software.database-administration.pgbouncer.connection-reset-and-lifetime-recycling
name: connection-reset-and-lifetime-recycling
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, server-lifetime, server-idle-timeout, recycling, close-needed]
level: advanced
status: docs-checked
description: "server_lifetime, server_idle_timeout and server_fast_close: how and when server connections are recycled."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: rotate server connections predictably.

- `server_lifetime` (default 3600.0 seconds): PgBouncer closes an unused server connection (not linked to any client) that has been connected longer than this. 0 means a connection is used only once, then closed. Can be set per database. The FAQ suggests a smaller value when load balancing with a TCP balancer.
- `server_idle_timeout` (default 600.0 seconds): a server connection idle longer than this is closed. 0 disables.
- `server_connect_timeout` (default 15.0 seconds): connect plus login must finish in this time.
- `server_fast_close` (default 0): in session pooling, a server in `close_needed` mode (set by RECONNECT, a RELOAD that changes connection settings, or a DNS change) is disconnected immediately or at the end of the current transaction rather than at session end. The client connection is also closed so the client notices. Running transactions are not interrupted, only idle sessions. In statement or transaction pooling it has no effect.

`close_needed` is visible in SHOW SERVERS (1 when the connection closes as soon as possible). Use `WAIT_CLOSE` to wait until it clears everywhere.

```
[pgbouncer]
server_lifetime = 1800
server_idle_timeout = 300
server_fast_close = 1
```

Enabling server_fast_close makes configuration changes apply sooner for long-lived sessions, but clients must reconnect and rebuild session state.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
