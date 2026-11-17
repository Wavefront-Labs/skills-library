---
id: computing-software.database-administration.sql-server.intelligent-query-processing
name: intelligent-query-processing
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, azure-sql, intelligent-query-processing, iqp, memory-grant-feedback, adaptive-joins, batch-mode-on-rowstore, scalar-udf-inlining, table-variable-deferred-compilation, dop-feedback, ce-feedback, compatibility-level, query-store]
level: advanced
status: docs-checked
description: "Turn on SQL Server intelligent query processing via compatibility level, know what each feature changes, and disable one that regresses without losing the rest."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/intelligent-query-processing
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/intelligent-query-processing-details
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Intelligent query processing (IQP)

**Goal:** get the automatic plan improvements of newer SQL Server versions by raising
compatibility level, with a controlled path when one feature hurts a query.

## Features by compatibility level
| Compat | Feature | What it does |
|---|---|---|
| 140 (SQL Server 2017) | Batch mode memory grant feedback | adds memory after spills; cuts the grant when a query wastes more than 50% of it, on later executions |
| 140 | Batch mode adaptive joins | defers hash vs nested loops choice until the first input is scanned |
| 140 | Interleaved execution (MSTVF) | actual row counts for multi-statement TVFs instead of a fixed guess (100 from SQL Server 2014) |
| 150 (2019) | Row mode memory grant feedback | the same feedback for row mode queries |
| 150 | Batch mode on rowstore | batch mode without a columnstore index (on-disk heaps and B-trees only) |
| 150 | Scalar UDF inlining | transforms scalar UDFs into relational expressions |
| 150 | Table variable deferred compilation | actual row count instead of the one-row guess |
| any level, 2019+ | Approximate count distinct | `APPROX_COUNT_DISTINCT` (approximate percentile functions arrive in 2022) |
| 160 (2022) | Parameter sensitive plan (PSP) optimization | several plans for one parameterized query |
| 160 | DOP feedback | tunes DOP for repeating queries; needs Query Store enabled |
| 160 | CE feedback | adjusts cardinality-estimation assumptions for repeating queries; needs Query Store READ_WRITE |
| 2022 (compat 140+) | Memory grant feedback percentile and persistence | persistence needs Query Store enabled and READ_WRITE |
| 170 (2025) | Optional parameter plan optimization (OPPO); CE feedback for expressions (needs 160+); `OPTIMIZED_SP_EXECUTESQL` | newer additions |

Enable by raising the compatibility level, e.g. `ALTER DATABASE appdb SET COMPATIBILITY_LEVEL = 160;` (SQL Server 2025 supports 170). Turn Query Store
on first and let it capture a baseline.

## Safe upgrade procedure
1. Enable Query Store at the old compat level, run a representative workload period.
2. Raise compat level.
3. Use Query Store "Regressed Queries"; force the old plan for regressions.
4. Disable a single feature if it is the cause, rather than dropping compat level:
```sql
ALTER DATABASE SCOPED CONFIGURATION SET TSQL_SCALAR_UDF_INLINING = OFF;                 -- 2019+
ALTER DATABASE SCOPED CONFIGURATION SET BATCH_MODE_ON_ROWSTORE = OFF;                   -- 2019+, default ON
ALTER DATABASE SCOPED CONFIGURATION SET DEFERRED_COMPILATION_TV = OFF;                  -- table variable deferred compilation
ALTER DATABASE SCOPED CONFIGURATION SET INTERLEAVED_EXECUTION_TVF = OFF;                -- 2019+ name; 2017 used DISABLE_INTERLEAVED_EXECUTION_TVF = ON
ALTER DATABASE SCOPED CONFIGURATION SET PARAMETER_SENSITIVE_PLAN_OPTIMIZATION = OFF;    -- 2022+
ALTER DATABASE SCOPED CONFIGURATION SET ROW_MODE_MEMORY_GRANT_FEEDBACK = OFF;           -- 2019+
-- per query (USE HINT overrides scoped configuration):
SELECT ... OPTION (USE HINT('DISABLE_INTERLEAVED_EXECUTION_TVF'));
SELECT ... OPTION (USE HINT('DISABLE_DEFERRED_COMPILATION_TV'));
SELECT ... OPTION (USE HINT('DISALLOW_BATCH_MODE'));       -- ALLOW_BATCH_MODE forces it back on for a query
```
For the scalar UDF inlining, memory grant feedback, PSP, DOP and CE feedback pages, Microsoft documents the per-feature hints, plan attributes and
catalog views; read those pages for the exact names before relying on them.

## Observe
- Interleaved execution: showplan attributes `ContainsInterleavedExecutionCandidates` and `IsInterleavedExecuted`; extended events
  `interleaved_exec_status`, `interleaved_exec_stats_update`, `Interleaved_exec_disabled_reason`.
- Interleaved plans can be forced in Query Store; the cached plan keeps the revised estimates from the first execution.

## Gotchas
- Interleaved execution: only read-only statements, and MSTVFs must use runtime constants; a plain `SELECT *` from an MSTVF gains nothing.
- Table variable deferred compilation shifts the first compile to first execution; it does not add column statistics and gains little when the row count varies widely.
- Batch mode on rowstore reduces CPU only (no help for I/O-bound or cold-cache queries); it does not apply to in-memory OLTP tables or when LOB columns are fetched or filtered; the optimizer may still choose row mode.
- DOP, CE and (percentile/persistence) memory grant feedback depend on Query Store being enabled and READ_WRITE.

## Verify
- [ ] Query Store captured a baseline before the compat change (and is READ_WRITE where feedback features need it).
- [ ] Regressions after the change are forced or a single feature disabled, documented.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 pages for Intelligent Query Processing and Intelligent Query Processing Details (2017-2025 tables).
Confirmed: feature-by-compatibility-level table, Query Store requirements, 2019 approximate count distinct, interleaved execution, table variable deferred compilation and batch mode on rowstore disable options, hints, XE events and showplan attributes. Removed unconfirmed specifics from other pages: UDF inlining hint and `INLINE = OFF`, `is_inlineable`, grant-feedback and adaptive-join plan attributes, `sys.query_store_plan_feedback`, optimized locking as an IQP item, and the Query Store Regressed Queries steps (see the query-store skill).
Method: documentation only; no commands were run.
