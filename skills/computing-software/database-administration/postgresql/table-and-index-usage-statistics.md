---
id: computing-software.database-administration.postgresql.table-and-index-usage-statistics
name: table-and-index-usage-statistics
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-stat-user-indexes, pg-stat-user-tables, unused-indexes, seq-scan, index-usage, monitoring]
level: practitioner
status: verified
description: "Use pg_stat_user_tables and pg_stat_user_indexes to find unused indexes, tables hit by sequential scans, HOT update ratios and dead-tuple build-up."
sources:
  - https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ALL-TABLES-VIEW
  - https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ALL-INDEXES-VIEW
  - https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STATIO-ALL-TABLES-VIEW
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Table and index usage statistics

Counters are cumulative since the last stats reset (`pg_stat_reset()` or crash). Check `stats_reset` in `pg_stat_database` before drawing conclusions.

## Unused indexes (drop candidates)
```sql
SELECT s.schemaname, s.relname, s.indexrelname, s.idx_scan, s.last_idx_scan,
       pg_size_pretty(pg_relation_size(s.indexrelid)) AS size
FROM pg_stat_user_indexes s JOIN pg_index i USING (indexrelid)
WHERE s.idx_scan = 0 AND NOT i.indisunique AND NOT i.indisprimary
ORDER BY pg_relation_size(s.indexrelid) DESC;
```
`last_idx_scan` is PG16+ (PG16 release notes: statistics on the last sequential and index scans). Before dropping: check **every replica** (stats are per node; reports may run on a standby), keep indexes backing constraints, and wait a full business cycle (month-end jobs). Drop with `DROP INDEX CONCURRENTLY`.

## Tables scanned sequentially a lot
```sql
SELECT relname, seq_scan, seq_tup_read, idx_scan, seq_tup_read / nullif(seq_scan,0) AS avg_rows_per_seq,
       n_live_tup
FROM pg_stat_user_tables ORDER BY seq_tup_read DESC LIMIT 20;
```
High `seq_tup_read` with large `avg_rows_per_seq` on a big table = missing index (find the queries in pg_stat_statements). Small tables with many seq scans are fine.

## HOT updates and fillfactor
```sql
SELECT relname, n_tup_upd, n_tup_hot_upd, round(100.0*n_tup_hot_upd/nullif(n_tup_upd,0),1) AS hot_pct
FROM pg_stat_user_tables WHERE n_tup_upd > 10000 ORDER BY n_tup_upd DESC;
```
Low HOT % on update-heavy tables: an indexed column is being updated, or pages are full. Lower `fillfactor` (e.g. 90) and avoid indexing frequently-updated columns.

## Dead tuples / vacuum health
```sql
SELECT relname, n_live_tup, n_dead_tup, last_autovacuum, autovacuum_count
FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 20;
```

## Cache hit by table
```sql
SELECT relname, heap_blks_read, heap_blks_hit, idx_blks_read, idx_blks_hit FROM pg_statio_user_tables ORDER BY heap_blks_read DESC LIMIT 20;
```

## Gotchas
- Stats are kept in shared memory since PG15 and written at clean shutdown; all counters reset after an immediate shutdown, a crash, starting from a base backup, or point-in-time recovery (docs: monitoring-stats).
- `idx_scan` counts scans, not usefulness; an index used once a day by a critical report is not unused.
- Duplicate indexes (same columns, same order) both show usage; find them by comparing `pg_index.indkey`.

## Checked
PostgreSQL 17.6: every query above runs and returns sensible columns (unused-index list showed three never-scanned indexes including a 10 MB trigram index; the seq-scan query ranked a 100,002-row table scanned 6 times first; the HOT query showed 100% for tables updated on unindexed columns and 0% for a table whose updated column is in a unique index; `n_dead_tup` was non-zero after updates); `pg_stat_force_next_flush()` was needed to see fresh counters in the same session. PG15/PG16 behaviour from the docs and release notes cited. `pg_stat_reset()` ran and zeroed the scan counters.
