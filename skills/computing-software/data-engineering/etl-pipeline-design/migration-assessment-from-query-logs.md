---
id: computing-software.data-engineering.etl-pipeline-design.migration-assessment-from-query-logs
name: migration-assessment-from-query-logs
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, migration-assessment, query-logs, inventory, warehouse-migration]
level: advanced
status: draft
description: "Assess a warehouse or ETL migration from query logs and metadata: inventory objects, usage and lineage, find dead assets, size complexity and plan migration waves."
sources:
  - https://docs.snowflake.com/en/sql-reference/account-usage/query_history
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/monitoring-performance-by-using-the-query-store
  - https://github.com/tobymao/sqlglot
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration assessment and inventory from query logs

**Goal:** know exactly what must be migrated, what can be retired, and how hard each piece is, before committing to a plan.

## Inventory
- Objects: tables, views, procedures, functions, jobs/schedules, ETL packages, users/roles, external integrations. Pull from system catalogs (`information_schema`, `sys.objects`, `DBA_OBJECTS`, Teradata `DBC.TablesV`).
- Sizes and growth per table; partitioning; refresh frequency.

## Usage from query logs
Collect 3-6 months (cover month/quarter-end):
- Teradata `DBQL`, Oracle AWR/`V$SQL`, SQL Server Query Store / Extended Events, Redshift `STL_QUERY`/`SYS_QUERY_HISTORY`, Snowflake `ACCESS_HISTORY`, BigQuery `INFORMATION_SCHEMA.JOBS`.
- Parse queries (sqlglot) to extract referenced tables/columns; aggregate by object: query count, distinct users, last access, source application.
```python
import sqlglot
from sqlglot import exp
tables = {t.sql() for t in sqlglot.parse_one(sql, read="tsql").find_all(exp.Table)}
```

## Classify
| Class | Rule | Action |
|---|---|---|
| Dead | no reads in 6 months | archive, do not migrate |
| Low use | few users, ad hoc | migrate late or replace |
| Critical | feeds exec reporting, many users, SLAs | migrate early with parallel run |
Lineage from parsed INSERT...SELECT / ETL metadata defines dependency order.

## Complexity scoring
Per object: SQL dialect features (procedural code, cursors, proprietary functions), lines of code, number of dependencies, ETL tool constructs. Run automated translation (sqlglot, vendor tools) on everything and count failures as a complexity signal.

## Plan waves
Group by domain and dependency so each wave can be validated and cut over independently; start with a representative but non-critical domain to calibrate estimates.

## Verify
Every object in the inventory has a class, owner and wave; dead-object list reviewed with owners before exclusion.
