---
id: computing-software.database-administration.postgresql.pgbouncer-prepared-statements-in-transaction-mode
name: pgbouncer-prepared-statements-in-transaction-mode
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-connection-pooling, pgbouncer, pgbouncer-prepared-statements, max-prepared-statements, transaction-pooling, prepared-statement-does-not-exist, jdbc-preparethreshold]
level: practitioner
status: docs-checked
description: "Run protocol-level prepared statements through PgBouncer transaction pooling with max_prepared_statements, or disable them per driver when it is 0."
sources:
  - https://www.pgbouncer.org/config.html#max_prepared_statements
  - https://www.pgbouncer.org/changelog.html
  - https://jdbc.postgresql.org/documentation/use/#connection-parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prepared statements through PgBouncer transaction mode

**Goal:** stop `prepared statement "S_1" does not exist` / `already exists` errors while keeping transaction pooling.

## Why it breaks
Drivers prepare a named statement on server connection A, then the next transaction lands on B, which never saw it.

## Let PgBouncer track them (max_prepared_statements)
```ini
[pgbouncer]
pool_mode = transaction
max_prepared_statements = 200   ; 0 disables; default 200 since PgBouncer 1.24.0 (0 before)
```
PgBouncer rewrites client statement names to its own and prepares them lazily on whichever server connection is used. Prepared statement usage counters are exposed in `SHOW STATS` (PgBouncer 1.24.0 and later).

Limits:
- Only protocol-level (Parse/Bind) prepared statements are tracked. `DEALLOCATE ALL` and `DISCARD ALL` are supported when max_prepared_statements is non-zero; plain `DEALLOCATE` is not (PgBouncer changelog).
- Size `max_prepared_statements` for your app's distinct statement count (see the config page).

## max_prepared_statements = 0: turn named statements off in the driver
| Driver | Setting |
|---|---|
| PostgreSQL JDBC | `prepareThreshold=0` |
| Other drivers | see the driver's documentation for disabling named or cached prepared statements |

## Gotchas
- Unnamed statements are always safe: a Parse/Bind/Execute in one round trip completes within one transaction.
- Turning prepares off costs a little parse time per query; usually much cheaper than more server connections.

## Verify
Run a workload with more clients than `default_pool_size` for a few minutes; no `prepared statement ... does not exist` errors in app or PgBouncer logs.

## Checked

2026-10-28. Confirmed against the PgBouncer config page and changelog (max_prepared_statements default 200 since 1.24.0, usage counters in SHOW STATS since 1.24.0, DEALLOCATE ALL and DISCARD ALL supported, plain DEALLOCATE unsupported) and the PostgreSQL JDBC connection parameters page (prepareThreshold). Corrected: default-change version (1.24.0, not 1.22) and the SQL PREPARE/EXECUTE claim. Removed: version gate 1.21+, LRU eviction claim, SHOW SERVERS column and the non-JDBC driver settings (driver docs not fetched).

Method: documentation only; no commands were run.
