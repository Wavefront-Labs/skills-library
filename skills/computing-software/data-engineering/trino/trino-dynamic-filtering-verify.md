---
id: computing-software.data-engineering.trino.trino-dynamic-filtering-verify
name: trino-dynamic-filtering-verify
category: computing-software
field: data-engineering
product: trino
tags: [dynamic-filtering, dynamic-partition-pruning, enable-dynamic-filtering, explain-plan, join-optimization]
level: advanced
status: docs-checked
description: "How Trino dynamic filtering prunes probe-side reads for selective joins and how to confirm it in EXPLAIN, EXPLAIN ANALYZE and QueryInfo statistics."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/dynamic-filtering.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino dynamic filtering verify

Dynamic filtering speeds up selective joins, such as a large fact table joined to a filtered dimension table, by avoiding reads that the join would discard. Without it, only the dimension predicate is pushed down and the whole fact table is scanned. With it, Trino collects candidate join-key values from the build (right) side; for broadcast joins the runtime predicate is pushed into the local probe-side scan on the same worker. It also goes to the coordinator for split enumeration (in Hive this is dynamic partition pruning), and for partitioned joins the coordinator distributes completed filters to workers. Benefits: faster queries, less network traffic and less load on the data source.

It is on by default; disable with `enable-dynamic-filtering` or session `enable_dynamic_filtering` set to false.

Planner support: inner and right joins with `=`, `<`, `<=`, `>`, `>=` or `IS NOT DISTINCT FROM`, and semi-joins with `IN`. Connectors must support using the filters at scan time (Hive pushes them into ORC and Parquet readers for stripe or row-group pruning) and at split enumeration.

Confirm it:
- `EXPLAIN` shows `dynamicFilterAssignments = {d_date_sk -> #df_370}` on the `InnerJoin` and `dynamicFilters = {"ss_sold_date_sk" = #df_370}` on the `ScanFilterProject`.
- QueryInfo JSON (Web UI) has `queryStats.dynamicFiltersStats` with domain, `collectionDuration`, and totals.
- Operator stats show `dynamicFilterSplitsProcessed` after pushdown.
- `EXPLAIN ANALYZE` lists the filters under `Dynamic filters:` with collection time.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. All claims match the page; unchanged.
