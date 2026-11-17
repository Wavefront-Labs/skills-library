---
id: computing-software.database-administration.query-optimisation.locking-and-pinning-statistics
name: locking-and-pinning-statistics
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, lock-statistics, plan-stability, pinned-statistics, query-statistics, plan-forcing]
level: practitioner
status: draft
description: "Stabilise plans by locking or pinning optimiser statistics (Oracle DBMS_STATS.LOCK, SQL Server NORECOMPUTE, PostgreSQL autovacuum analyze settings), or force plans instead."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/managing-optimizer-statistics-advanced-topics.html
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/update-statistics-transact-sql
  - https://www.postgresql.org/docs/current/routine-vacuuming.html#VACUUM-FOR-STATISTICS
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Locking or pinning statistics to stabilise plans

## When it helps
- Volatile tables (staging, queue tables) that are empty at night when stats are gathered and full during the day: gathered stats say "0 rows", plans are terrible at peak.
- A known-good statistics state that new gathers keep breaking (skew captured badly by sampling).

## Oracle
```sql
-- gather when the table is representative, then lock
EXEC DBMS_STATS.GATHER_TABLE_STATS(user, 'STAGING_ORDERS');
EXEC DBMS_STATS.LOCK_TABLE_STATS(user, 'STAGING_ORDERS');
-- or set representative values manually
EXEC DBMS_STATS.SET_TABLE_STATS(user, 'STAGING_ORDERS', numrows => 2000000, numblks => 40000);
EXEC DBMS_STATS.UNLOCK_TABLE_STATS(user, 'STAGING_ORDERS');
```
The automatic stats job skips locked tables; `GATHER_*` with `force => TRUE` overrides. Also `DBMS_STATS.EXPORT_TABLE_STATS`/`IMPORT_TABLE_STATS` to save and restore known-good stats; `RESTORE_TABLE_STATS(as_of_timestamp => ...)` rolls back to history.

## SQL Server
```sql
UPDATE STATISTICS dbo.staging_orders WITH FULLSCAN, NORECOMPUTE;   -- disables auto update for these stats
-- undo
UPDATE STATISTICS dbo.staging_orders;   -- without NORECOMPUTE re-enables
```
`sp_autostats 'dbo.staging_orders', 'OFF'` per table. Statistics with `PERSIST_SAMPLE_PERCENT = ON` (2016 SP1 CU4+) keeps a chosen sample rate across auto updates.

## PostgreSQL
No lock command. Options:
- Per-table autovacuum analyze settings: `ALTER TABLE staging_orders SET (autovacuum_analyze_threshold = 1000000000, autovacuum_analyze_scale_factor = 0)` effectively stops auto-analyze; run `ANALYZE` manually at a representative time.
- Extended statistics and higher statistics targets for skew.
- `pg_hint_plan` to pin plans; PostgreSQL 18 adds statistics import functions (`pg_restore_relation_stats`, `pg_restore_attribute_stats`) that can restore a saved statistics state.

## MySQL
`STATS_PERSISTENT=1, STATS_AUTO_RECALC=0` per table, then `ANALYZE TABLE` when representative; `STATS_SAMPLE_PAGES` for accuracy.

## Prefer plan control when the target is one query
Query Store plan forcing (SQL Server), SQL plan baselines (Oracle), `pg_hint_plan`: they pin the plan without freezing stats for every other query.

## Risks
Locked stats go stale as data grows; schedule a review. Document every lock (who, why, until when).

## Verify
After locking, stats timestamps stop changing (`last_analyzed`, `STATS_DATE`, `pg_stat_user_tables.last_autoanalyze`) and plans for the target queries remain stable through the nightly window.
