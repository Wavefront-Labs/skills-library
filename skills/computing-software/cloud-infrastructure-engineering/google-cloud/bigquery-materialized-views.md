---
id: computing-software.cloud-infrastructure-engineering.google-cloud.bigquery-materialized-views
name: bigquery-materialized-views
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, bigquery, bigquery-materialized-views, query-performance, smart-tuning, cost-control]
level: practitioner
status: docs-checked
description: "Use BigQuery materialized views to cut cost and latency of repeated aggregations: supported SQL, refresh settings, max_staleness, smart tuning, partition alignment and monitoring."
sources: ["https://cloud.google.com/bigquery/docs/materialized-views-intro", "https://cloud.google.com/bigquery/docs/materialized-views-create", "https://cloud.google.com/bigquery/docs/materialized-views-manage", "https://cloud.google.com/bigquery/docs/materialized-views-use"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BigQuery materialized views

## 1. Create
```sql
CREATE MATERIALIZED VIEW `<P>.mart.daily_sales_mv`
PARTITION BY dt
CLUSTER BY store_id
OPTIONS (enable_refresh = TRUE, refresh_interval_minutes = 60, max_staleness = INTERVAL 4 HOUR)
AS SELECT DATE(ts) AS dt, store_id, SUM(amount) AS revenue, COUNT(*) AS orders
FROM `<P>.raw.sales`
GROUP BY dt, store_id;
```
- The create page shows partition-aligned MVs over a partitioned base table; for partitioned MVs over `UNION ALL`, all base tables must have the same partition expiration (TTL) or incremental refreshes fail.
- By default only incremental queries are allowed. Incremental MVs support aggregates including `AVG`, `APPROX_COUNT_DISTINCT` and `HLL_COUNT.INIT`; `LEFT OUTER JOIN` support is in Preview. Non-incremental MVs (`allow_non_incremental_definition = true`) support most syntax that incremental MVs do not, and cannot use smart tuning.

## 2. Smart tuning
If any part of a query against a base table can be answered by an incremental MV, BigQuery reroutes it to read the MV (smart tuning). Smart tuning is not supported for MVs with `UNION ALL` or `LEFT OUTER JOIN`, and the `max_staleness` option changes how fresh the served data must be (see "Smart tuning and the max_staleness option" in the intro page).

## 3. Manage
```sql
CALL BQ.REFRESH_MATERIALIZED_VIEW('<P>.mart.daily_sales_mv');
SELECT * FROM `<P>.mart.INFORMATION_SCHEMA.TABLES`;   -- MV metadata
```
Refresh jobs and MV details are available through the BigQuery API (see "Monitor materialized views").

## Gotchas
- Limits: each base table can have at most 100 MVs within a project (500 per organization).
- MVs over BigLake tables need metadata caching on the base table and an MV `max_staleness` greater than the base table's; the MV cannot be partitioned, so any deletion in the base table causes a full refresh.

## Verify
- [ ] A query on the base table that the MV can answer reads from the MV (check the job details) and processes fewer bytes.

## Checked

2026-10-27. Confirmed in the materialized views intro, create, manage and use pages: `CREATE MATERIALIZED VIEW` options `enable_refresh`, `refresh_interval_minutes`, `max_staleness`, `allow_non_incremental_definition`, `CALL BQ.REFRESH_MATERIALIZED_VIEW`, smart tuning behaviour and its exclusions, supported aggregates, LEFT OUTER JOIN in Preview, partition alignment and UNION ALL TTL rule, BigLake base table requirements, the 100-per-base-table and 500-per-organization limits. Removed: the 20-MV limit (wrong), the same-dataset-location claim, `INFORMATION_SCHEMA.MATERIALIZED_VIEWS` columns and job-id pattern, `materialized_view_statistics` field path, cost claims. Read end to end.

Method: documentation only; no commands were run.
