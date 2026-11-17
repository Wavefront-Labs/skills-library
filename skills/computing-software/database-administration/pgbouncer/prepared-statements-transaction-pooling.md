---
id: computing-software.database-administration.pgbouncer.prepared-statements-transaction-pooling
name: prepared-statements-transaction-pooling
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, prepared-statements, max-prepared-statements, transaction-pooling, protocol]
level: sme
status: docs-checked
description: "max_prepared_statements: tracking protocol-level prepared statements in transaction pooling, its memory cost and the cached plan error."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use prepared statements through transaction or statement pooling.

`max_prepared_statements` (default 200): when non-zero, PgBouncer tracks protocol-level named prepared statements from clients in transaction and statement pooling. It renames each unique query string to `PGBOUNCER_{unique_id}`, rewrites client commands to use that name, and transparently prepares the statement on whichever server connection is assigned. The value is the size of an LRU cache of prepared statements per server connection. 0 disables support.

Not tracked: SQL-level PREPARE, EXECUTE and DEALLOCATE go straight to Postgres. Exceptions that work: DEALLOCATE ALL and DISCARD ALL clear what PgBouncer tracked for that client.

Size it above the number of commonly used prepared statements. Higher values increase memory on PostgreSQL connections and in PgBouncer. Each unique query is stored once; each client keeps a rewrite buffer of at most 4 times pkt_buf. The docs' example: 1000 clients, 200 unique queries of 5kB, pkt_buf 4096 gives 200 x 5kB + 1000 x 4 x 4kB = about 17MB. Tracking also costs CPU; run several instances with so_reuseport.

Downside of sharing: if a prepared statement's argument or result types change, Postgres raises `ERROR:  cached plan must not change result type`. This commonly occurs after DDL migrations (added column, changed type). Run `RECONNECT` on the console after the migration to force re-preparation.

SHOW STATS has total_client_parse_count, total_server_parse_count and total_bind_count (and avg_ versions) for this mode. The FAQ notes this feature exists since version 1.21.0.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
