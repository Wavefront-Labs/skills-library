---
id: computing-software.database-administration.pgbouncer.statement-pooling-mode
name: statement-pooling-mode
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, statement-pooling, pool-mode, autocommit, restrictions]
level: advanced
status: docs-checked
description: "Statement pooling releases the server after every query; multi-statement transactions are disallowed."
sources:
  - https://www.pgbouncer.org/usage.html
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know when statement pooling fits and what it rejects.

Statement pooling is the most aggressive pooling mode: the server connection returns to the pool immediately after each query completes. Multi-statement transactions are disallowed because they would break, as the usage docs state.

Enable globally, per database or per user:

```
[pgbouncer]
pool_mode = statement
```

Behaviour notes from the docs:

- A server connection is released at the end of each query.
- Prepared statements: named protocol-level prepared statements can be tracked in statement mode when `max_prepared_statements` is non-zero; SQL-level PREPARE/EXECUTE/DEALLOCATE are not tracked.
- `server_fast_close` has no effect in statement or transaction mode because immediate disconnect at release is already the behaviour there.
- The server_reset_query is not run in this mode unless `server_reset_query_always` is on.

Check the mode actually applied with `SHOW POOLS;` (pool_mode column) and per-database overrides with `SHOW DATABASES;`.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. Removed: a padded comparison paragraph.

Method: documentation only; no commands were run.
