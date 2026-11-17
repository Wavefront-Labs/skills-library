---
id: computing-software.cloud-infrastructure-engineering.azure.sql-query-store-performance-insight-and-automatic-tuning
name: sql-query-store-performance-insight-and-automatic-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-sql, sql-performance, query-store, query-performance-insight, automatic-tuning, force-last-good-plan, plan-regression, wait-stats, dmvs, database-watcher, intelligent-insights]
level: advanced
status: docs-checked
description: "Diagnose Azure SQL performance: Query Store top queries and plan regressions, Query Performance Insight, DMVs, automatic tuning (force plan, indexes) and resource limits."
sources: ["https://learn.microsoft.com/en-us/sql/relational-databases/performance/monitoring-performance-by-using-the-query-store", "https://learn.microsoft.com/en-us/azure/azure-sql/database/query-performance-insight-use", "https://learn.microsoft.com/en-us/azure/azure-sql/database/automatic-tuning-overview", "https://learn.microsoft.com/en-us/azure/azure-sql/database/monitoring-with-dmvs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure SQL performance — Query Store, QPI and automatic tuning

**Goal:** from "the database is slow" to the specific query, plan or resource limit
responsible, and a fix that sticks (forced plan, index, or right-sized tier).

## 1. Is it the tier or the query?
```sql
SELECT TOP 20 end_time, avg_cpu_percent, avg_data_io_percent, avg_log_write_percent, avg_memory_usage_percent, max_worker_percent
FROM sys.dm_db_resource_stats ORDER BY end_time DESC;     -- recent resource history for the database (see the DMV article for retention)
```
- CPU, data IO or log write near 100 % means a resource limit is being hit (bigger tier or less work); `PAGEIOLATCH_*` waits point to data IO.
- Worker percentage near 100 (`max_worker_percent`) points to too many concurrent requests (fix pooling), not a single query.

## 2. Query Store (on by default in Azure SQL)
```sql
ALTER DATABASE CURRENT SET QUERY_STORE = ON (OPERATION_MODE = READ_WRITE);
EXEC sp_query_store_force_plan @query_id = 4711, @plan_id = 42;     -- pin a known-good plan
```
- SSMS Query Store reports include *Regressed Queries* and *Query Wait Statistics*; use them to find the query and plan behind the load.

## 3. Query Performance Insight and automatic tuning
- Portal → database → **Query Performance Insight**: top CPU/duration/execution-count queries
  over a time range from Query Store, with per-query charts — the quick view for non-DBAs.
- **Automatic tuning** options: `FORCE_LAST_GOOD_PLAN`, `CREATE_INDEX`, `DROP_INDEX`; changes are validated. The overview article says which options
  are available per platform and what new servers inherit by default.
```sql
ALTER DATABASE CURRENT SET AUTOMATIC_TUNING (FORCE_LAST_GOOD_PLAN = ON, CREATE_INDEX = ON);
```

## Gotchas
- Forced plans can stop applying after schema changes; re-check Queries With Forced Plans after deployments.
- Parameter sniffing shows as two plans with very different cost for the same query_id.
- Scaling up to fix a missing index costs money every month; check indexes and plans first.

## Verify
- [ ] Query Store is `READ_WRITE` with headroom; top 10 queries identified with their plans.
- [ ] Automatic tuning options show the intended effective state.
- [ ] After the fix, `sys.dm_db_resource_stats` shows the limiting resource back below its limit with headroom at peak.

## Checked
2026-10-27. Confirmed on Microsoft Learn: Query Store article (enabled by default for new Azure SQL Database and Managed Instance databases, `OPERATION_MODE`, `sp_query_store_force_plan`,
Regressed Queries and Query Wait Statistics reports), automatic-tuning-overview (FORCE_LAST_GOOD_PLAN, CREATE_INDEX, DROP_INDEX, validation, T-SQL enablement, server inheritance),
monitoring-with-dmvs (`sys.dm_db_resource_stats`, `max_worker_percent`, `PAGEIOLATCH`), query-performance-insight-use.
Removed: 15-second and one-hour retention figures, wait-type list, top-CPU catalog-view query, MAX_STORAGE_SIZE_MB and capture-mode settings, READ_ONLY meaning, on/off-by-default
for each tuning option, the `az sql db update` command, Advisor and database watcher notes, `force_failure_count`, PSP and hints names, serverless note, the 70 % target.

Method: documentation only; no commands were run.
