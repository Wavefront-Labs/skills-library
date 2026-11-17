---
id: computing-software.database-administration.pgbouncer.server-reset-query
name: server-reset-query
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, server-reset-query, discard-all, session-pooling, state]
level: practitioner
status: docs-checked
description: "server_reset_query and server_reset_query_always: cleaning session state when a server connection is released."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/faq.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give the next client a clean server session.

`server_reset_query` (default `DISCARD ALL`) is sent to the server when a connection is released, before another client can use it. No transaction is in progress at that moment, so do not include ABORT or ROLLBACK.

DISCARD ALL cleans everything but leaves the next client with no pre-cached state. A lighter value such as `DEALLOCATE ALL` just drops prepared statements; use it only if the application tolerates some state being kept.

In transaction pooling the reset query is not used, because clients must not rely on session features there: every transaction may land on a different connection with different state.

`server_reset_query_always` (default 0): when 0, the reset query runs only for pools in session pooling mode. When 1 it runs in all pooling modes. The docs describe this as a workaround for broken setups where applications use session features over transaction pooling; it changes non-deterministic breakage into deterministic breakage, because clients always lose state after each transaction.

```
server_reset_query = DISCARD ALL
server_reset_query_always = 0
```

For session pooling with prepared statements, the FAQ says the reset query must clear old prepared statements: DISCARD ALL or at least DEALLOCATE ALL. SHOW POOLS counts connections currently running the reset or check query under sv_tested.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
