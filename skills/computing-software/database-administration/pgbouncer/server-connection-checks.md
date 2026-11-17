---
id: computing-software.database-administration.pgbouncer.server-connection-checks
name: server-connection-checks
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, server-check-query, server-check-delay, health, server-connections]
level: practitioner
status: docs-checked
description: "server_check_query and server_check_delay: how PgBouncer validates idle server connections before reuse."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide how released server connections are verified before reuse.

- `server_check_delay` (default 30.0 seconds): how long released connections stay available for immediate reuse without running server_check_query. 0 means the check always runs.
- `server_check_query` (default `<empty>`): a simple do-nothing query to test that the connection is alive. An empty string disables sanity checking; the literal value `<empty>` sends an empty query as the check.

In SHOW POOLS, `sv_idle` are connections immediately usable, `sv_used` are connections idle longer than server_check_delay that need server_check_query before reuse, and `sv_tested` are connections currently running either server_reset_query or server_check_query.

Runtime change example from the console:

```
SET server_check_query = 'select 2';
```

Related lifetime controls: `server_lifetime` (default 3600.0 seconds) closes unused server connections connected longer than that (0 means use once, then close; can be set per database); `server_idle_timeout` (default 600.0) closes connections idle longer than that (0 disables); `server_connect_timeout` (default 15.0) closes connections whose connect and login do not finish in time.

`server_fast_close` (default 0) makes session-pooled servers in close_needed state disconnect immediately or after the current transaction; the client connection is closed too so it notices.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
