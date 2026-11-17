---
id: computing-software.database-administration.query-optimisation.stale-statistics-after-bulk-loads
name: stale-statistics-after-bulk-loads
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, cardinality-estimation, stale-statistics, analyze-after-load, ascending-key-problem, auto-analyze-threshold, update-statistics, etl-tuning]
level: practitioner
status: draft
description: "Prevent bad plans right after bulk loads, ETL batches and new-partition inserts by refreshing statistics explicitly, and handle the ascending-key problem per engine."
sources:
  - https://www.postgresql.org/docs/current/routine-vacuuming.html#VACUUM-FOR-STATISTICS
  - https://learn.microsoft.com/en-us/sql/relational-databases/statistics/statistics#UpdateStatistics
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-persistent-stats.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stale statistics after bulk loads

**Goal:** the query that runs right after the nightly load uses a plan based on
tonight's data, not yesterday's.

## Why it happens
Auto-stats trigger on thresholds and run asynchronously:
- PostgreSQL autovacuum analyzes when changed rows > `autovacuum_analyze_threshold`
  (50) + `autovacuum_analyze_scale_factor` (10%) × rows, at the next autovacuum
  cycle (up to `autovacuum_naptime` later, often longer on busy systems).
- SQL Server auto-update fires on the next query compile after ~sqrt(1000 × rows)
  changes (2016+ dynamic threshold); with async stats, the first queries still use old stats.
- MySQL InnoDB recalculates after ~10% change in the background.
A batch job that loads data and immediately queries it (staging → transform)
runs before any of that, with estimates of ~0 rows for the new data.

## Fix: analyze as part of the job
```sql
-- PostgreSQL
COPY staging FROM ...; ANALYZE staging;
-- SQL Server
UPDATE STATISTICS dbo.staging WITH FULLSCAN;   -- or SAMPLE 10 PERCENT on huge tables
-- MySQL
ANALYZE TABLE staging;
-- Oracle
EXEC DBMS_STATS.GATHER_TABLE_STATS(user, 'STAGING', no_invalidate => FALSE);
```
Temporary tables in PostgreSQL are **never** analyzed by autovacuum: always ANALYZE them manually.

## The ascending-key problem
New rows have keys/timestamps beyond the histogram's last bucket: a query for
"today" estimates ~1 row although 1M rows arrived. Mitigations:
- PostgreSQL reads actual min/max from an index at plan time for out-of-range
  values (`get_actual_variable_range`), which helps, but ANALYZE after loads anyway.
- SQL Server 2014+ CE assumes some rows exist beyond the histogram; for the
  legacy CE, trace flags 2389/2390 or more frequent updates on the key column's stats.
- Oracle: gather stats after each partition load, or copy stats from a prior
  partition (`DBMS_STATS.COPY_TABLE_STATS`) for new partitions.

## Gotchas
- Huge FULLSCAN updates during business hours compete with workload; sample on very large tables.
- Updating stats invalidates cached plans (SQL Server recompiles): expected.

## Verify
In the batch's EXPLAIN (or captured actual plan) estimated rows for the new data
are in the right order of magnitude; `pg_stat_user_tables.last_analyze`,
`STATS_DATE()` (SQL Server), `mysql.innodb_table_stats.last_update` show the job's run time.
