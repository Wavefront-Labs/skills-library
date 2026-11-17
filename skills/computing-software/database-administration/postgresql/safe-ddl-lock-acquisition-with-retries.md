---
id: computing-software.database-administration.postgresql.safe-ddl-lock-acquisition-with-retries
name: safe-ddl-lock-acquisition-with-retries
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, locking, safe-ddl-locking, lock-timeout, schema-migration, zero-downtime, nowait]
level: practitioner
status: verified
description: "Run DDL on busy PostgreSQL tables without freezing traffic: lock_timeout plus retry loops, NOWAIT, short transactions and splitting heavy changes into online steps."
sources:
  - https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-LOCK-TIMEOUT
  - https://www.postgresql.org/docs/current/sql-lock.html
  - https://www.postgresql.org/docs/current/sql-altertable.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe DDL lock acquisition with retries

## Problem
Most `ALTER TABLE` forms need ACCESS EXCLUSIVE. Waiting for it behind one long query makes
all other queries on the table queue behind the DDL. A 50 ms DDL becomes a multi-minute outage.

## Pattern: fail fast, retry
```sql
SET lock_timeout = '2s';            -- cap the wait for the lock
SET statement_timeout = '30s';      -- cap the DDL itself (metadata-only changes are fast)
ALTER TABLE orders ADD COLUMN source text;
```
Wrap in a retry with backoff (shell example):
```bash
for i in 1 2 3 4 5 6 7 8 9 10; do
  psql -v ON_ERROR_STOP=1 -c "SET lock_timeout='2s'; ALTER TABLE orders ADD COLUMN source text;" && break
  sleep $((i * 3))
done
```
`ERROR: canceling statement due to lock timeout` (SQLSTATE 55P03) is the retryable signal.
Migration frameworks: set `lock_timeout` in the migration connection (Rails `strong_migrations`,
Django per-migration `SET`, Flyway `-initSql`).

`NOWAIT` is the zero-wait variant: `LOCK TABLE orders IN ACCESS EXCLUSIVE MODE NOWAIT;` then the
DDL in the same transaction. Fails immediately if anyone holds a conflicting lock.

## Keep the locked window short
- One DDL per transaction for hot tables. Locks are held until COMMIT; a migration that alters
  five tables in one transaction holds all five locks until the end.
- Never mix DDL with data backfills in one transaction.
- Kill or wait out long queries first: check
  `SELECT pid, now()-xact_start, query FROM pg_stat_activity WHERE xact_start < now() - interval '1 min';`

## Replace heavy DDL with online steps
| Instead of | Do |
|---|---|
| `CREATE INDEX` | `CREATE INDEX CONCURRENTLY` (outside a transaction) |
| `ADD FOREIGN KEY` | `ADD CONSTRAINT ... NOT VALID` then `VALIDATE CONSTRAINT` (SHARE UPDATE EXCLUSIVE) |
| `SET NOT NULL` | `ADD CONSTRAINT c CHECK (col IS NOT NULL) NOT VALID`, `VALIDATE`, then `SET NOT NULL` (skips scan, PG12+) |
| `ALTER COLUMN TYPE int -> bigint` | new column, trigger/batched backfill, swap in a short transaction |
| `ADD COLUMN DEFAULT volatile()` | add nullable column, backfill in batches, then set default |
| `REINDEX` | `REINDEX CONCURRENTLY` |

## Gotchas
- `lock_timeout` applies per lock acquisition, not to the whole statement.
- Setting `lock_timeout` in postgresql.conf globally affects every session; set it per
  migration role (`ALTER ROLE migrator SET lock_timeout = '3s'`).
- On a primary with synchronous standbys, commit also waits on the standby.

## Verify
Run the migration while `pgbench` drives traffic and confirm no latency spike beyond the
lock_timeout window, and that retries succeed within the loop.

## Checked
Run on PostgreSQL 17.6 (Windows build, two to eight real sessions via psycopg 3.3) on Windows: the shell retry loop (run through Git bash: attempt 1 failed with `canceling statement due to lock timeout` while a reader held the table, the loop slept, and a later attempt succeeded once the reader ended); `psql -v ON_ERROR_STOP=1` returns exit status 1 on the timeout; `LOCK TABLE ... NOWAIT` raising 55P03 `could not obtain lock on relation`; `ALTER ROLE migrator SET lock_timeout = '3s'` applying to the role's new sessions (the default role stayed 0); `CREATE INDEX CONCURRENTLY` and `REINDEX CONCURRENTLY` refusing to run inside a transaction block; `VALIDATE CONSTRAINT` taking `SHARE UPDATE EXCLUSIVE` on the table (and `ROW SHARE` on the referenced table for a foreign key); `int` to `bigint` and a volatile default rewriting the table; the CHECK-based `SET NOT NULL` path. Not run: pgbench traffic during a migration, synchronous standby commit waits, Rails/Django/Flyway settings, `lock_timeout` per lock versus per statement (documented behaviour only). The loop uses bash; on Windows PowerShell write the equivalent loop.
