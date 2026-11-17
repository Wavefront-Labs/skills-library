---
id: computing-software.database-administration.pgbouncer.transaction-pooling-session-state
name: transaction-pooling-session-state
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, transaction-pooling, session-state, reset-query, leaks]
level: sme
status: docs-checked
description: "What breaks in transaction pooling: session features, SET leakage and the settings that mitigate it."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid state leaking across clients sharing a server connection.

In transaction pooling each transaction can end up on a different server connection, so clients must not use session-based features. The docs say server_reset_query is not used in this mode, because there is no need for it.

Known mitigation settings:

- `server_reset_query_always = 1`: runs the reset query in all pooling modes. The docs call it a workaround for broken setups where applications use session features over transaction pooling; it turns non-deterministic breakage into deterministic breakage, since clients always lose state after each transaction.
- `track_extra_parameters`: add parameters PgBouncer should keep in the client variable cache and restore on the server when the client becomes active. Default-tracked parameters include application_name, client_encoding, DateStyle, IntervalStyle, session_authorization, standard_conforming_strings and TimeZone.
- Parameters Postgres does not report to clients cannot be fully tracked; SET changes to them leak to other clients unless server_reset_query_always is used.
- Named protocol-level prepared statements work if `max_prepared_statements` is non-zero (default 200), but SQL-level PREPARE, EXECUTE and DEALLOCATE are forwarded unmanaged.
- `statement` mode additionally disallows multi-statement transactions.

```
[pgbouncer]
pool_mode = transaction
max_prepared_statements = 200
server_reset_query_always = 0
```

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. Removed: an unconfirmed advice paragraph about a session-mode user for migrations.

Method: documentation only; no commands were run.
