---
id: computing-software.database-administration.query-optimisation.plan-visualizers
name: plan-visualizers
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, plan-visualizer, explain-depesz, explain-dalibo, plan-explorer, execution-plans]
level: practitioner
status: draft
description: "Use execution plan visualizers (explain.depesz.com, explain.dalibo.com/PEV2, SQL Sentry Plan Explorer, MySQL Workbench visual explain) to find the expensive node fast."
sources:
  - https://explain.depesz.com/
  - https://explain.dalibo.com/
  - https://www.solarwinds.com/free-tools/plan-explorer
  - https://dev.mysql.com/doc/workbench/en/wb-performance-explain.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Plan visualizers

**Goal:** turn a 300-line plan into "this node takes 80% of time because estimates are off by 1000x".

## PostgreSQL
Capture a complete plan:
```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, SETTINGS, FORMAT JSON) SELECT ...;   -- or FORMAT TEXT for depesz
```
- **explain.depesz.com**: paste TEXT plan; colours exclusive time per node, row estimate misses (the "rows x" column), loops. Has an anonymise option before sharing.
- **explain.dalibo.com (PEV2)**: paste JSON or text plus the query; graphical tree, flags for misestimates, buffers per node. PEV2 can be self-hosted (single HTML file) for sensitive plans.
- `auto_explain` logs plans of slow queries in production in the same formats.

Read for: highest exclusive time node, biggest estimate vs actual ratio, high loops on nested loops, `Rows Removed by Filter`, `Buffers: read` (cold I/O), sorts/hash spills (`Disk:`).

## SQL Server
- SSMS: Include Actual Execution Plan (Ctrl+M); right-click → Compare Showplan; Query Store plan views.
- **SolarWinds Plan Explorer** (free): sortable statement tree, per-operator costs by CPU/IO, actual vs estimated rows, wait stats with the plan, index analysis tab.
- Share `.sqlplan` XML (anonymise object names if needed).

## MySQL
- `EXPLAIN ANALYZE` (8.0.18+) text tree; `EXPLAIN FORMAT=JSON` for costs.
- MySQL Workbench Visual Explain draws the JSON plan with colour-coded costs.

## Oracle
- `DBMS_XPLAN.DISPLAY_CURSOR(format => 'ALLSTATS LAST')` with `gather_plan_statistics`; SQL Monitor active reports (`DBMS_SQLTUNE.REPORT_SQL_MONITOR(type => 'ACTIVE')`) give an interactive timeline.

## Caveats
- Visualizers show the plan you captured: with ANALYZE the query actually ran (careful with DML: wrap in a transaction and roll back).
- Percentages based on estimated cost (SSMS "Query cost relative to batch") can be badly wrong; trust actual time/rows.
- Public paste sites store plans: do not paste sensitive literals; use anonymisation or self-hosted tools.

## Verify
After a fix, paste the new plan next to the old one and confirm the hot node's exclusive time dropped.
