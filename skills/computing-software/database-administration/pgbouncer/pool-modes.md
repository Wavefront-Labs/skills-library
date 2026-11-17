---
id: computing-software.database-administration.pgbouncer.pool-modes
name: pool-modes
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, pool-mode, session-pooling, transaction-pooling, statement-pooling]
level: intro
status: docs-checked
description: "The three pool_mode values (session, transaction, statement), when a server connection is released and what each forbids."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose when a server connection is handed back to the pool.

`pool_mode` is set globally in [pgbouncer], and can be overridden per database in [databases] or per user in [users]. The default is `session`.

- `session`: the server connection is released back to the pool after the client disconnects. The most polite method; the whole client session owns one server connection.
- `transaction`: the server connection is released after the transaction finishes. Clients must not use session-based features, because each transaction can land on a different connection and thus a different session state.
- `statement`: the server connection is released after each query finishes. Multi-statement transactions are disallowed because they would break.

Precedence for a given pool: the user's pool_mode, otherwise the database's pool_mode, otherwise the default pool_mode.

```
[pgbouncer]
pool_mode = transaction

[databases]
reportdb = host=db2 pool_mode=session

[users]
batchuser = pool_mode=session
```

SHOW POOLS reports the mode in use in its pool_mode column, and SHOW DATABASES shows each database's override (NULL if the default applies).

In transaction pooling, server_reset_query is not used unless server_reset_query_always is on. Named prepared statements need max_prepared_statements to work in transaction or statement mode.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
