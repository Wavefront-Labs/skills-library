---
id: computing-software.database-administration.sql-server.memory-grants-and-tempdb-spills
name: memory-grants-and-tempdb-spills
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, query-store, execution-plan, memory-grant, tempdb-spill, resource-semaphore-waits, memory-grant-feedback]
level: advanced
status: docs-checked
description: "Diagnose SQL Server memory grant problems: oversized grants causing RESOURCE_SEMAPHORE waits, undersized grants spilling sorts and hashes to tempdb, and fixes."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-query-memory-grants-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/intelligent-query-processing-memory-grant-feedback
  - https://learn.microsoft.com/en-us/sql/relational-databases/event-classes/sort-warnings-event-class
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory grants and tempdb spills

Sorts, hash joins and hash aggregates need **workspace memory** granted before execution,
sized from cardinality estimates.

## Too big: RESOURCE_SEMAPHORE
Overestimated rows -> huge grants -> other queries queue for memory.
```sql
SELECT * FROM sys.dm_exec_query_memory_grants WHERE grant_time IS NULL;   -- queries waiting for a grant
```
`ideal_memory_kb` is the grant needed to fit everything in memory, based on the cardinality
estimate. The wait type is typically `RESOURCE_SEMAPHORE`.

## Too small: spills
Underestimated rows -> grant too small -> data spills to tempdb. Look for spill warnings
in actual plans.

## Fixes, in order
1. **Fix estimates**: update statistics, avoid functions and
   implicit conversions on predicates, break huge queries into steps with temp tables.
2. **Reduce what needs memory**: select fewer/narrower columns (wide `varchar(max)` columns
   inflate grant estimates), index to provide order instead of sorting.
3. **Memory grant feedback** (IQP): row mode needs database compatibility level 150 or higher;
   percentile and persistence mode (SQL Server 2022) needs Query Store enabled and in read-write state.
   It adjusts grants after repeated executions.

## Verify
After the fix, the actual plan has no spill warnings and RESOURCE_SEMAPHORE waits fall.

## Checked
2026-10-28. Confirmed against the memory grants, intelligent query processing and sys.dm_exec_query_memory_grants pages: grants are sized from cardinality estimates, queries waiting for a grant have grant_time IS NULL, ideal_memory_kb, wait type RESOURCE_SEMAPHORE, row mode memory grant feedback needs compatibility level 150 or higher, percentile and persistence mode are in SQL Server 2022 and need Query Store enabled in read-write state.
Removed unconfirmed claims: the DMV column list beyond grant_time and ideal_memory_kb, XE event names, Hash Warning text, Query Store avg_tempdb_space_used, table-variable estimate note, batch mode 2017/compat 140 gate, plan XML attribute, MIN/MAX_GRANT_PERCENT, Resource Governor default of 25%, both gotchas.
Method: documentation only; no commands were run.
