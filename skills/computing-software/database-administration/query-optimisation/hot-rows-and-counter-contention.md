---
id: computing-software.database-administration.query-optimisation.hot-rows-and-counter-contention
name: hot-rows-and-counter-contention
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, hot-row-contention, counter-contention, row-locking, query-patterns, sharded-counters]
level: practitioner
status: draft
description: "Fix write contention on hot rows (global counters, inventory, balances) with sharded counters, batching, append-and-aggregate tables, and short transactions."
sources:
  - https://www.postgresql.org/docs/current/explicit-locking.html
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-locking-and-row-versioning-guide
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hot rows and counter contention

## Symptom
Throughput plateaus while CPU is idle; lock waits on the same row (`UPDATE counters SET n = n + 1 WHERE id = 1`). Every writer serialises on one row lock and holds it until commit.

Detect:
- PostgreSQL: `pg_stat_activity` `wait_event_type = 'Lock'`, `wait_event = 'transactionid'` or `tuple`; `pg_locks` shows many waiters on the same relation/tuple.
- MySQL: `performance_schema.data_lock_waits`, `SHOW ENGINE INNODB STATUS` lock waits on one PK.
- SQL Server: `LCK_M_U`/`LCK_M_X` waits on one key (`sys.dm_tran_locks`).

## Fixes
1. **Shorten the transaction**: increment last, right before commit; no network calls or slow work while holding the row.
2. **Sharded counter**: N rows per counter, writers pick one randomly, readers sum.
```sql
CREATE TABLE page_views (page_id bigint, shard smallint, n bigint DEFAULT 0, PRIMARY KEY (page_id, shard));
UPDATE page_views SET n = n + 1 WHERE page_id = $1 AND shard = floor(random() * 16);
SELECT sum(n) FROM page_views WHERE page_id = $1;
```
3. **Append, aggregate later**: insert one row per event (no contention), roll up periodically into a summary table.
4. **Buffer in memory/Redis**: increment in Redis (`INCR`) and flush to the database every few seconds.
5. **Inventory**: conditional decrement in one statement avoids read-then-write races and keeps lock time minimal: `UPDATE stock SET qty = qty - 1 WHERE sku = $1 AND qty > 0 RETURNING qty`.
6. **Queues**: `SELECT ... FOR UPDATE SKIP LOCKED` so workers do not wait on each other's rows.

## Engine notes
- PostgreSQL: each update creates a new row version: very hot rows also bloat; keep `fillfactor` < 100 for HOT updates and ensure autovacuum keeps up.
- InnoDB: gap/next-key locks can widen contention under REPEATABLE READ; use unique key equality lookups.
- SQL Server: optimised locking (2025 / Azure SQL) and `OPTIMIZE_FOR_SEQUENTIAL_KEY` (last-page insert contention) address related hotspots.

## Verify
Benchmark with production-like concurrency: throughput scales with writers after the change, and lock-wait time in the top waits drops.
