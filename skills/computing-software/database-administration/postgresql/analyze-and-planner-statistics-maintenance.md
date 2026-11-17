---
id: computing-software.database-administration.postgresql.analyze-and-planner-statistics-maintenance
name: analyze-and-planner-statistics-maintenance
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgres-analyze, autovacuum-analyze, planner-statistics, default-statistics-target, pg-stats, extended-statistics]
level: practitioner
status: verified
description: "Keep PostgreSQL planner statistics fresh: when autovacuum runs ANALYZE, per-table scale factors, statistics targets, and manual ANALYZE after bulk changes."
sources:
  - https://www.postgresql.org/docs/current/routine-vacuuming.html#VACUUM-FOR-STATISTICS
  - https://www.postgresql.org/docs/current/sql-analyze.html
  - https://www.postgresql.org/docs/current/runtime-config-autovacuum.html
  - https://www.postgresql.org/docs/current/planner-stats.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Updating planner statistics (ANALYZE)

Bad row estimates are the most common cause of bad plans; stale statistics cause most bad estimates.

## When autovacuum analyzes
A table is auto-analyzed when rows changed since the last analyze exceed:
`autovacuum_analyze_threshold (50) + autovacuum_analyze_scale_factor (0.1) * reltuples`
On a 200M-row table that is 20M changes: new data (today's dates, new IDs) is invisible to the planner for a long time.

```sql
SELECT relname, n_mod_since_analyze, last_analyze, last_autoanalyze, n_live_tup
FROM pg_stat_user_tables ORDER BY n_mod_since_analyze DESC LIMIT 20;
```

## Per-table tuning for big/fast tables
```sql
ALTER TABLE events SET (autovacuum_analyze_scale_factor = 0.0, autovacuum_analyze_threshold = 500000);
```
Fixed thresholds work better than percentages on very large tables.

## Statistics target (histogram/MCV detail)
```sql
SHOW default_statistics_target;                       -- 100: samples 300*100 = 30000 rows
ALTER TABLE events ALTER COLUMN tenant_id SET STATISTICS 1000;
ANALYZE events (tenant_id);
SELECT n_distinct, most_common_vals, histogram_bounds FROM pg_stats WHERE tablename='events' AND attname='tenant_id';
```
Raise it per column for skewed columns used in WHERE/joins; raising it globally makes ANALYZE and planning slower everywhere.

## Correlated columns: extended statistics
```sql
CREATE STATISTICS events_city_zip (dependencies, ndistinct, mcv) ON city, zip FROM events;
ANALYZE events;
```

## Run ANALYZE manually when
- After bulk loads, big deletes, `CREATE INDEX` on an expression (expression indexes get their own stats only from ANALYZE).
- After `pg_upgrade` / logical restore (stats are not carried over before PG18): `vacuumdb --all --analyze-in-stages`.
- Temporary tables: autovacuum never touches them; ANALYZE them in the job that fills them.
- Partitioned parents: autovacuum analyzes partitions but **not the parent**; run `ANALYZE parent_table` periodically for queries planned against the whole hierarchy.

## Verify
```sql
EXPLAIN (ANALYZE) SELECT ... ;   -- compare rows= estimate with actual rows on each node
```
Estimates off by 10x or more at a low node point at stats.

## Gotchas
- ANALYZE takes a `SHARE UPDATE EXCLUSIVE` lock: concurrent with reads/writes, but conflicts with VACUUM/DDL on the same table.
- `ANALYZE` inside a long transaction holds that lock for the whole transaction.

## Checked
- PostgreSQL 17.6 with 100,000 rows: autoanalyze defaults 50 and 0.1; per-table `autovacuum_analyze_*` reloptions; `default_statistics_target` 100 and `SET STATISTICS 1000` gives 10 MCVs for a 10-value column; `CREATE STATISTICS ... (dependencies, ndistinct, mcv)` stores kinds `{d,f,m}` and dependencies; an expression index has no `pg_stats` rows until `ANALYZE`; `ANALYZE` holds `ShareUpdateExclusiveLock`; with `autovacuum_naptime=2s` a plain table and a partition were auto-analyzed while the partitioned parent and a temporary table never were; the 18 notes say `pg_upgrade` retains statistics.
