---
id: computing-software.database-administration.postgresql.table-lock-modes-and-conflict-matrix
name: table-lock-modes-and-conflict-matrix
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, locking, mvcc, table-lock-modes, access-exclusive-lock, ddl-locks, lock-queue]
level: practitioner
status: verified
description: "Know which PostgreSQL commands take which of the eight table lock modes, what conflicts with what, and why a waiting ACCESS EXCLUSIVE request blocks all readers."
sources:
  - https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-TABLES
  - https://www.postgresql.org/docs/current/sql-altertable.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Table-level lock modes and the conflict matrix

## Modes, weakest to strongest, with typical takers
| Mode | Taken by |
|---|---|
| ACCESS SHARE | `SELECT` |
| ROW SHARE | `SELECT ... FOR UPDATE/SHARE` |
| ROW EXCLUSIVE | `INSERT`, `UPDATE`, `DELETE`, `MERGE` |
| SHARE UPDATE EXCLUSIVE | `VACUUM` (non-FULL), `ANALYZE`, `CREATE INDEX CONCURRENTLY`, `ALTER TABLE ... SET STATISTICS / VALIDATE CONSTRAINT`, `DETACH PARTITION CONCURRENTLY` |
| SHARE | `CREATE INDEX` (non-concurrent) |
| SHARE ROW EXCLUSIVE | `CREATE TRIGGER`, `ALTER TABLE ... ADD FOREIGN KEY` (on both the referencing and the referenced table) |
| EXCLUSIVE | `REFRESH MATERIALIZED VIEW CONCURRENTLY` |
| ACCESS EXCLUSIVE | `DROP`, `TRUNCATE`, `VACUUM FULL`, `CLUSTER`, `REFRESH MATERIALIZED VIEW`, most `ALTER TABLE` forms (add column, alter type, set not null, rename, set default) |
| SHARE on the table + ACCESS EXCLUSIVE on the index | `REINDEX TABLE` (non-concurrent): writes block, plain reads of the table do not, queries using that index do |

## Conflicts that matter in practice
- ACCESS EXCLUSIVE conflicts with **everything**, including plain SELECT.
- SHARE (plain CREATE INDEX) conflicts with ROW EXCLUSIVE: writes block for the whole build,
  reads continue.
- SHARE UPDATE EXCLUSIVE conflicts with itself: two `CREATE INDEX CONCURRENTLY` on the same
  table, or CIC vs a running autovacuum, wait for each other. An anti-wraparound autovacuum
  does not yield.
- Row modes (ROW SHARE / ROW EXCLUSIVE) do not conflict with each other; row-level conflicts
  are handled separately by row locks.

## The lock queue problem
Locks are granted in **queue order**. If a long SELECT holds ACCESS SHARE and an
`ALTER TABLE` requests ACCESS EXCLUSIVE, the ALTER waits, and every new SELECT queues behind
the ALTER. The table is effectively down until the long query ends. Defence:
```sql
SET lock_timeout = '2s';
ALTER TABLE orders ADD COLUMN note text;   -- fails fast instead of stalling traffic; retry
```

## Which ALTER TABLE forms are cheap
- Instant metadata only (still ACCESS EXCLUSIVE, but milliseconds): `ADD COLUMN` with no
  default or a non-volatile default (PG11+), `DROP COLUMN`, `RENAME`, `SET DEFAULT`.
- Full table rewrite under ACCESS EXCLUSIVE: `ALTER COLUMN TYPE` (unless binary-coercible,
  e.g. varchar(n) -> text), `ADD COLUMN ... DEFAULT random()`.
- Full scan under lock: `SET NOT NULL` (PG12+ skips the scan if a valid `CHECK (col IS NOT NULL)` exists).

## Inspect
```sql
SELECT relation::regclass, mode, granted, pid FROM pg_locks
WHERE relation = 'orders'::regclass;
```
Or `LOCK TABLE orders IN SHARE MODE;` explicitly in a transaction when you need a
consistent snapshot of a table that must not change.

## Verify
In a test, hold `BEGIN; SELECT * FROM t LIMIT 1;` open in one session, run the DDL with
`lock_timeout` in another, and confirm it times out instead of blocking a third session's SELECT.

## Checked
Run on PostgreSQL 17.6 (Windows build, two to eight real sessions via psycopg 3.3) on Windows: every row of the table was read from `pg_locks` inside a transaction (SELECT, FOR UPDATE/SHARE, INSERT/UPDATE, CREATE INDEX, CREATE TRIGGER, SET STATISTICS, TRUNCATE, ADD COLUMN, RENAME, SET DEFAULT, ADD FOREIGN KEY, REFRESH MATERIALIZED VIEW with and without CONCURRENTLY, CLUSTER, REINDEX, LOCK ... SHARE, ANALYZE, VALIDATE CONSTRAINT); conflicts by blocking real statements under `lock_timeout` (VACUUM FULL, CLUSTER, REINDEX and TRUNCATE blocked by a reader; CREATE INDEX, VACUUM, ANALYZE and CREATE INDEX CONCURRENTLY not; SHARE blocks UPDATE but not SELECT; SHARE UPDATE EXCLUSIVE blocks CIC, VACUUM and ANALYZE but not SELECT or UPDATE); the queue behind a pending ALTER; rewrite behaviour by `relfilenode` (`varchar(n)` to `text` or a wider `varchar` none, narrower `varchar` and `int` to `bigint` rewrite, `DEFAULT random()` rewrite, `DEFAULT 5` and `DEFAULT now()` none) and `SET NOT NULL` skipping the scan with a valid CHECK (server DEBUG1 message). Not run: DETACH PARTITION CONCURRENTLY, VACUUM FULL's lock mode directly (blocked-by-reader only), anti-wraparound autovacuum not yielding, Linux (lock modes are server logic, not OS specific).
