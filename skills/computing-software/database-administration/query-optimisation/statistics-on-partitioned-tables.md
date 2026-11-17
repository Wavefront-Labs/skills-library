---
id: computing-software.database-administration.query-optimisation.statistics-on-partitioned-tables
name: statistics-on-partitioned-tables
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, partition-statistics, incremental-statistics, partitioned-tables, query-statistics, partition-pruning]
level: practitioner
status: draft
description: "Keep optimiser statistics accurate on partitioned tables: partition-level vs global stats, incremental statistics, PostgreSQL parent ANALYZE, and new-partition stats."
sources:
  - https://www.postgresql.org/docs/current/ddl-partitioning.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/gathering-optimizer-statistics.html
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/create-statistics-transact-sql
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Statistics on partitioned tables

## Two levels
- **Partition-level stats**: used when the query prunes to one partition.
- **Global (table-level) stats**: used when several partitions are touched; must not be just a sum, since distinct counts do not add up.

## PostgreSQL
- Autovacuum analyzes **leaf partitions** only; it never analyzes the partitioned parent. Planner estimates for queries spanning partitions use parent stats if present.
- Run `ANALYZE parent_table;` periodically: it samples across all partitions for the parent's stats and also re-analyzes each partition. PostgreSQL 18 adds `ANALYZE ONLY parent_table` to refresh just the parent.
- New partition after attach/creation: `ANALYZE` it right after bulk load; an empty-stats partition gets default estimates.
- Partition pruning happens at plan time (constants) and at execution (`Subplans Removed: N` in EXPLAIN ANALYZE); prepared statements with generic plans rely on runtime pruning.

## Oracle
- Incremental global statistics (synopses) avoid rescanning all partitions:
```sql
EXEC DBMS_STATS.SET_TABLE_PREFS(user, 'SALES', 'INCREMENTAL', 'TRUE');
EXEC DBMS_STATS.GATHER_TABLE_STATS(user, 'SALES', granularity => 'AUTO');
```
Only changed partitions are rescanned; global NDV is derived from synopses.
- Copy stats to a new partition before data arrives: `DBMS_STATS.COPY_TABLE_STATS(user, 'SALES', srcpartname => 'P2026_09', dstpartname => 'P2026_10')` so the "current month" partition does not look empty.

## SQL Server
- Statistics are table-level by default; one histogram (max 200 steps) for the whole partitioned table, which is coarse for many partitions.
- `CREATE STATISTICS ... WITH INCREMENTAL = ON` (or database `AUTO_CREATE_STATISTICS ON (INCREMENTAL = ON)`) keeps per-partition stats merged into the global, and `UPDATE STATISTICS t (st) WITH RESAMPLE ON PARTITIONS (12)` refreshes one partition. The optimiser still uses the merged global histogram.
- Filtered statistics on the hot partition range can help.

## MySQL
InnoDB keeps index stats per partition and aggregates; `ANALYZE TABLE t PARTITION (p202610)` (via `ALTER TABLE ... ANALYZE PARTITION`).

## Verify
For a query hitting the newest partition, estimated rows match actual; `pg_stats` / `DBA_TAB_PARTITIONS.LAST_ANALYZED` / `sys.dm_db_incremental_stats_properties` show recent stats for active partitions.
