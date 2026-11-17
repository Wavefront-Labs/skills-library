---
id: computing-software.data-engineering.data-warehouse-architecture.pre-aggregation-and-caching-layers
name: pre-aggregation-and-caching-layers
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-serving, pre-aggregation, cube-dev, semantic-cache, rollup-tables, bi-performance, materialized-views]
level: advanced
status: docs-checked
description: "Speed up dashboards and APIs with pre-aggregation: rollup tables, materialized views, Cube pre-aggregations, BI extracts and caches, with refresh and consistency trade-offs."
sources:
  - https://cube.dev/docs/product/caching/using-pre-aggregations
  - https://docs.snowflake.com/en/user-guide/views-materialized
  - https://cloud.google.com/bigquery/docs/materialized-views-intro
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pre-aggregation and caching layers

**Goal:** sub-second dashboards and data APIs at predictable cost, without users querying raw fact tables for every click.

## Options by layer
| Layer | Mechanism | Fresh by | Best for |
|---|---|---|---|
| Warehouse table | dbt rollup models (`fct_sales_daily_by_store`) | pipeline schedule | known, stable query patterns |
| Warehouse MV | Snowflake and BigQuery materialized views | maintained automatically in the background | repeated, predictable aggregate queries |
| Semantic layer cache | Cube pre-aggregations | refresh keys / schedules | many BI tools/APIs sharing metrics |
| BI tool | the BI tool's own extracts or caches | extract schedules | single-tool dashboards |
| Result cache | warehouse result cache, an API cache with a TTL | TTL / invalidation | repeated identical queries |

Materialized view facts from the vendor pages: Snowflake MVs are maintained by a background service, a materialized view can query only a single table, storage and maintenance cost credits so check the saving outweighs them, the optimizer can rewrite queries to use the MV, and privileges are not inherited from the base table. If maintenance falls behind, queries may be slower but results stay current. BigQuery MVs add base-table changes incrementally with no user action and return fresh results; incremental MVs support a limited set of SQL and enable smart tuning (query rerouting), while non-incremental MVs (`allow_non_incremental_definition = true`) run the full query on every refresh and do not guarantee fresh results.

## Rollup design
- Choose grain from dashboard filters: date x store x category instead of order line.
- Keep measures additive (sums, counts); ratios and distinct counts do not roll up from coarser grains, so plan for them separately.
- Incremental refresh by date partition with a lookback window for late data (Cube: `partition_granularity` plus `incremental` and `update_window`).
- Aggregate awareness: Cube tries to match each query to a pre-aggregation first and otherwise queries the source, unless rollup-only mode is enabled (`CUBEJS_ROLLUP_ONLY`), which also lets the warehouse stay suspended between refreshes.

## Cube pre-aggregation example
```yaml
cubes:
  - name: orders
    sql_table: analytics.fct_orders
    measures:
      - {name: revenue, sql: amount, type: sum}
      - {name: count, type: count}
    dimensions:
      - {name: status, sql: status, type: string}
      - {name: created_at, sql: created_at, type: time}
    pre_aggregations:
      - name: daily_by_status
        type: rollup
        measures: [revenue, count]
        dimensions: [status]
        time_dimension: created_at
        granularity: day
        partition_granularity: month
        refresh_key: {every: 1 hour, incremental: true, update_window: 7 day}
```
Cube builds the rollups and serves matching queries from them. The default `refresh_key` is every 1 hour; an incremental refresh with `update_window` reloads only the latest partitions. The example is an illustration, check the Cube docs for your version.

## Consistency and freshness
- Every cache has a staleness window; display "data as of" in dashboards.
- Coordinate refresh with upstream completion (trigger rollup rebuild after the dbt job, not on an unrelated cron).
- Late data: rebuild trailing partitions (update window).

## Cost trade-offs
Rollup refresh compute vs repeated scans saved: compute both from query history (frequency x bytes scanned). MVs on frequently changing base tables can cost more in maintenance than they save.

## Gotchas
- Too many rollups become their own maintenance burden; start with the most expensive or slowest dashboard queries.
- Row-level security must apply to rollups too (design this explicitly; Snowflake MVs do not inherit base-table privileges).
- Distinct counts and percentiles do not roll up from finer rollups.

## Verify
- [ ] Dashboard latency and warehouse credits before/after (Snowflake advises recording costs before adding an MV).
- [ ] Rollup totals reconcile with base-table queries for sampled periods.

## Checked
Date: 2026-11-09. Confirmed: Cube pre-aggregation matching, rollup-only mode, default refresh_key, partitioning and update_window (searched, not read in full); Snowflake MV maintenance, cost, single-table and privilege notes (searched); BigQuery MV page (first part read: incremental vs non-incremental, freshness, smart tuning). Removed as unconfirmed: dbt SL caching, AtScale, Tableau, Power BI, Looker, Databricks MVs, HyperLogLog advice, Cube Store as the only location, the "top 5" rule.
Method: documentation only; no commands were run.
