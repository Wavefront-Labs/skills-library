---
id: computing-software.database-administration.sql-server.plan-cache-and-optimize-for-ad-hoc-workloads
name: plan-cache-and-optimize-for-ad-hoc-workloads
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, plan-cache, optimize-for-ad-hoc-workloads, single-use-plans, forced-parameterization, sys-dm-exec-cached-plans, sys-dm-exec-query-stats, dbcc-freeproccache, compilations, query-hash]
level: advanced
status: docs-checked
description: "Inspect the SQL Server plan cache, find single-use plan bloat and top resource queries, and apply optimize for ad hoc workloads or forced parameterization."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/optimize-for-ad-hoc-workloads-server-configuration-option
  - https://learn.microsoft.com/en-us/sql/relational-databases/query-processing-architecture-guide
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-query-stats-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plan cache and optimize for ad hoc workloads

## Top queries from the cache
```sql
SELECT TOP 20 qs.total_worker_time/1000 AS cpu_ms, qs.execution_count,
       qs.total_logical_reads, qs.total_elapsed_time/1000 AS elapsed_ms,
       qs.query_hash, DB_NAME(st.dbid) db,
       SUBSTRING(st.text, qs.statement_start_offset/2+1,
         (CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(st.text) ELSE qs.statement_end_offset END
          - qs.statement_start_offset)/2+1) AS stmt,
       qp.query_plan
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) st
CROSS APPLY sys.dm_exec_query_plan(qs.plan_handle) qp
ORDER BY qs.total_worker_time DESC;
```
Group by `query_hash` to aggregate the same query with different literals. Cached plans are cleared by events such as restarts, failovers and setting a database offline, and can be removed by memory pressure or recompilation.

## Single-use plan bloat
```sql
SELECT objtype, COUNT(*) plans, SUM(CAST(size_in_bytes AS bigint))/1048576 AS mb,
       SUM(CASE WHEN usecounts = 1 THEN 1 ELSE 0 END) single_use
FROM sys.dm_exec_cached_plans GROUP BY objtype ORDER BY mb DESC;
```
Many GB of `Adhoc` plans with `usecounts = 1` = an app concatenating literals into SQL.
```sql
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'optimize for ad hoc workloads', 1; RECONFIGURE;
```
First execution caches only a small stub; the full plan is cached on the second
execution (the stub lets the engine recognise a batch it compiled before). Changing the option does not clear existing plans; clear the plan cache or restart to apply it at once.

## Compilation pressure
Compare compilation counters with batch requests in Performance Monitor.
`ALTER DATABASE appdb SET PARAMETERIZATION FORCED;` makes the engine parameterize more statements (see the query processing architecture guide for what changes); test it before production.
The real fix is parameterized queries in the app (`sp_executesql`, ORM parameters).

## Evicting plans
```sql
DBCC FREEPROCCACHE (0x0600...);                 -- one plan_handle
ALTER DATABASE SCOPED CONFIGURATION CLEAR PROCEDURE_CACHE;   -- SQL Server 2016+, database in scope
-- DBCC FREEPROCCACHE without arguments removes all plans: avoid in production
```
`sp_recompile 'dbo.proc'` marks one module for recompilation.

## Gotchas
- Memory pressure can remove plans from the cache.
- `sys.dm_exec_query_stats` only covers plans that are in the cache: counts are lost when plans leave.

## Verify
- [ ] `optimize for ad hoc workloads` = 1; single-use Adhoc MB trending down.
- [ ] Top CPU queries identified by query_hash and owned by someone.

## Checked

2026-10-28. Confirmed against Microsoft Learn (optimize for ad hoc workloads option, query processing architecture guide, sys.dm_exec_query_stats): compiled plan stub on first compile, existing plans stay until the cache is cleared, DBCC FREEPROCCACHE single plan or all, ALTER DATABASE SCOPED CONFIGURATION CLEAR PROCEDURE_CACHE (2016+), sp_recompile, PARAMETERIZATION FORCED, query_hash, plans cleared by restart, failover, offline, memory pressure and recompilation. Removed unconfirmed: the Query Store durability remark, scoped-configuration OPTIMIZE_FOR_AD_HOC_WORKLOADS, percentage threshold for compilations, plan guide TEMPLATE advice, nvarchar length remark, OPTION (RECOMPILE) note.

Method: documentation only; no commands were run.
