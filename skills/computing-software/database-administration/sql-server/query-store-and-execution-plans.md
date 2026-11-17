---
id: computing-software.database-administration.sql-server.query-store-and-execution-plans
name: query-store-and-execution-plans
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, azure-sql, t-sql, query-store, query-store-configuration, force-plan, execution-plan, actual-execution-plan, showplan, plan-regression, plan-forcing, sp-query-store-force-plan, parameter-sniffing, parameter-sensitive-plan, psp-optimization, query-store-hints, optimize-for-unknown, option-recompile, set-statistics-io, ssms, compatibility-level, cardinality-estimator, dmv, sys-dm-exec-query-stats]
level: advanced
status: docs-checked
description: "Enable and configure Query Store, find regressed and high-resource queries, read actual execution plans, and force or hint plans to fix parameter-sensitive regressions."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/monitoring-performance-by-using-the-query-store
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/best-practice-with-the-query-store
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/execution-plans
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-database-query-store-options-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/query-store-hints
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-query-store-force-plan-transact-sql
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Query Store and execution plans — find the regression, read the plan, pin the fix

**Goal:** use Query Store as the flight recorder for every database, so "it got slow
yesterday" becomes a specific query, a specific plan change and a reversible fix.

## 1. Turn Query Store on and size it
Query Store is on by default (READ_WRITE) for new databases from SQL Server 2022 and in Azure SQL Database/Managed Instance; SQL Server 2016-2019 need it enabled per
database (it cannot be enabled for `master` or `tempdb`):
```sql
ALTER DATABASE [<DB_NAME>] SET QUERY_STORE = ON (
  OPERATION_MODE = READ_WRITE,
  QUERY_CAPTURE_MODE = AUTO,          -- capture relevant queries by execution count and resource use (default is ALL on SQL Server, AUTO in Azure SQL Database)
  MAX_STORAGE_SIZE_MB = 2048,         -- default 100 MB through SQL Server 2017, 1 GB from 2019
  INTERVAL_LENGTH_MINUTES = 60,       -- default 60; allowed 1, 5, 10, 15, 30, 60, 1440
  CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30),   -- default 30; 0 disables
  SIZE_BASED_CLEANUP_MODE = AUTO,     -- default; starts at 90% of max size, stops near 80%
  WAIT_STATS_CAPTURE_MODE = ON);      -- 2017+
```
Check `SELECT desired_state_desc, actual_state_desc, readonly_reason, current_storage_size_mb FROM
sys.database_query_store_options;`. If `actual_state_desc` is READ_ONLY while desired is READ_WRITE, `readonly_reason` is a bitmask
(65536 = reached `max_storage_size_mb`, 524288 = database disk limit, 1/2/4/8 = read-only, single-user, emergency, secondary); raise the size or shorten retention.
`max_plans_per_query` defaults to 200. Actual state ERROR: from 2017 try `sp_query_store_consistency_check`, else `ALTER DATABASE ... SET QUERY_STORE CLEAR ALL`.
Query Store captures DML, not DDL such as `CREATE INDEX`; natively compiled procedures need `sys.sp_xtp_control_query_exec_stats`.

## 2. Find what to fix
In SSMS (version 16+; Query Wait Statistics needs 18+): *Database > Query Store* > **Regressed Queries** (filter by duration, CPU, reads, memory, wait time and more; Force Plan button) and
**Query Wait Statistics** (wait categories, 2017+). Or T-SQL; runtime statistics are aggregated per plan, execution type and interval (durations in microseconds, reads in 8-KB pages):
```sql
SELECT TOP 20 q.query_id, p.plan_id, qt.query_sql_text,
  SUM(rs.count_executions) AS execs,
  SUM(rs.avg_duration * rs.count_executions)/1000 AS total_ms,
  SUM(rs.avg_logical_io_reads * rs.count_executions) AS total_reads
FROM sys.query_store_runtime_stats rs
JOIN sys.query_store_plan p ON p.plan_id = rs.plan_id
JOIN sys.query_store_query q ON q.query_id = p.query_id
JOIN sys.query_store_query_text qt ON qt.query_text_id = q.query_text_id
WHERE rs.last_execution_time > DATEADD(hour, -24, SYSDATETIMEOFFSET())
GROUP BY q.query_id, p.plan_id, qt.query_sql_text
ORDER BY total_ms DESC;
```
A `query_id` with two or more `plan_id`s and very different averages is a plan change worth reviewing: Microsoft lists statistics, schema and index changes as
typical reasons plans evolve.

## 3. Read the plan
An execution plan defines the order in which tables are accessed, the access method for each (index seek, index scan, table scan) and how calculations, filters,
aggregation and sorting are done. Microsoft documents how to display and save plans (SSMS, XML) and the Query Optimizer inputs (query, schema, statistics). Compare the
plan Query Store holds for the good and the bad `plan_id`, and look for what changed: statistics, schema, indexes, parameter values. See Microsoft's pages
"Display and save execution plans" and "Showplan logical and physical operators reference" for operator-level reading; this skill does not restate them.

## 4. Fix it, smallest lever first
| Lever | Use when |
|---|---|
| `EXEC sp_query_store_force_plan @query_id, @plan_id;` | a known-good plan exists; immediate, reversible |
| `UPDATE STATISTICS dbo.T WITH FULLSCAN;` | complete statistics maintenance before adding hints (Microsoft's advice) |
| Query Store hints `EXEC sys.sp_query_store_set_hints @query_id = 39, @query_hints = N'OPTION(RECOMPILE)';` (SQL Server 2022+) | can't change app code; Query Store must be capturing; remove with `sys.sp_query_store_clear_hints` |
| Index change (covering/`INCLUDE`) | access paths dominate |
Plan forcing needs `ALTER` on the database; `sp_query_store_force_plan` also has `@disable_optimized_plan_forcing` and (2025, secondaries) `@replica_group_id`. The forced plan
may be only "the same or similar", so performance can differ and, rarely, regress: remove the forced plan then. If forcing fails an extended event fires and the optimizer
compiles normally. Use `sp_query_store_unforce_plan` to remove.
Query Store hints are a last resort: first check statistics and index maintenance and the latest compatibility level (compat 160 brings Parameter Sensitive Plan optimization, which
may already cover multi-plan needs; a `RECOMPILE` hint works on any supported level). Hints override statement hints and plan guides, are not supported for statements that qualify
for simple parameterization, and `RECOMPILE` is ignored with forced parameterization (warning 12461). Re-evaluate hints and forced plans when data volume or distribution
changes and after migrations; view hints in `sys.query_store_query_hints`.
Review forced plans after every schema release.

## Verify
- [ ] `actual_state_desc` is `READ_WRITE` on every user database you care about.
- [ ] The slow query is identified by `query_id`, with its good and bad `plan_id`.
- [ ] Good and bad plans were compared for what changed (statistics, schema, indexes, parameters).
- [ ] Fix applied; duration/reads in Query Store dropped over the next interval.
- [ ] Forced plans and hints are documented and reviewed after schema releases.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 pages for Monitor performance by using the Query Store, sys.database_query_store_options, sys.query_store_runtime_stats, Query Store hints, sp_query_store_force_plan and Execution plan overview.
Confirmed: default-on from 2022, option defaults and allowed values, readonly_reason bitmask, consistency check, SSMS reports, runtime statistics units, force-plan and hints syntax and caveats. Removed unconfirmed claims: 1-4 GB sizing, SSMS report names beyond those documented, plan-reading heuristics (the execution plan overview page does not contain them), `sp_query_store_set_hints` positional syntax, automatic tuning and `sys.dm_db_tuning_recommendations`, `force_failure_count`, the missing-index advice.
Method: documentation only; no commands were run.
