---
id: computing-software.database-administration.clickhouse.materialized-views-vs-projections
name: materialized-views-vs-projections
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, materialized-views, projections, comparison, target-table]
level: practitioner
status: docs-checked
description: "Decide between a ClickHouse incremental materialized view and a projection by query pattern, flexibility and storage cost."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/data-modeling/projections/2_materialized-views-versus-projections.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# materialized views vs projections
Both precompute data at insert time, but they differ in where the data lives and how queries find it.

Projections:
- Live inside the source table's parts, are chosen automatically by the optimizer, and need no change to queries.
- Limited to a single MergeTree-family table: no JOINs or WHERE clause in the definition, cannot be chained, and not compatible with FINAL queries or parallel replicas.
- Are updated in the background upon INSERT and maintained automatically; by default incompatible with lightweight deletes.

Materialized views:
- Write into a separate target table with its own schema and engine (usually MergeTree family).
- You query the target table explicitly; they support WHERE, JOINs (incremental views trigger only on left-most table inserts) and chaining.
- Incremental views are insert triggers; they can go stale when source data is frequently updated or deleted, and often need manual backfilling.

Choose a projection when you need a second ordering or a rollup that stays transparent to existing queries on a single table. Choose a materialized view when you need a different schema, longer or shorter retention for the aggregate, joins, multiple sources or fan-in, or you want to drop the raw data and keep only the summary (`Null` engine source).

The page also recommends not treating the choice as either/or: they can be used together.

## Checked
2026-11-03. Confirmed against the ClickHouse docs page "Materialized views versus projections": every comparison point above (storage, update mechanism, JOIN and WHERE support, chaining, engines, FINAL, parallel replicas, lightweight deletes, when to choose each). Removed: the insert-cost, GROUP BY, column-drop and rows_read claims.
Method: documentation only; no commands were run.
