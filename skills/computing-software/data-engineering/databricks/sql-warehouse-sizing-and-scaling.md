---
id: computing-software.data-engineering.databricks.sql-warehouse-sizing-and-scaling
name: sql-warehouse-sizing-and-scaling
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, sql-warehouse-sizing, sql-warehouses, concurrency-scaling, serverless-sql]
level: practitioner
status: docs-checked
description: "Size Databricks SQL warehouses: cluster size for query complexity vs min/max clusters for concurrency, serverless vs pro vs classic, auto stop, and reading queueing."
sources:
  - https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-behavior
  - https://docs.databricks.com/aws/en/compute/sql-warehouse/create
  - https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-types
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL warehouse sizing and scaling

**Goal:** dashboards and ad-hoc queries fast enough, without paying for idle capacity.

## Two dials
- **Size** (2X-Small ... 4X-Large): compute per cluster. Increase when single queries are slow because of large scans, spill to disk, or big joins (query profile shows spill/shuffle).
- **Scaling (min/max clusters)**: number of clusters. Increase max when queries **queue** under concurrent load. Rough planning figure: about 10 concurrent queries per cluster.

## Types
| Type | Start time | Notes |
|---|---|---|
| Serverless | seconds (typically 2-6) | intelligent workload management, rapid upscaling |
| Pro | several minutes (typically about 4) | use when serverless is unavailable in a region or you need custom networking |
| Classic | several minutes (typically about 4) | supports Photon but not Predictive IO or intelligent workload management |

## Auto stop
Serverless default is 10 minutes (minimum 5 in the UI). Pro and classic default is 45 minutes (minimum 10).

## Diagnose
Compare queue time with execution time per warehouse in the query history and warehouse monitoring views.
- High queue time -> raise max clusters.
- High execution time with spill -> bigger size, or fix the query/table layout.
- Low utilisation -> smaller size, lower min clusters.

## Separation
Separate warehouses for BI dashboards, ad-hoc analysts and ETL/dbt, so a heavy dbt run does not starve dashboards; tag for cost attribution.

## Verify
After changes, p95 query duration and queue time per warehouse improve without a proportional rise in DBUs.

## Checked

- 2026-10-28: confirmed on the warehouse types page (serverless start 2 to 6 seconds, pro and classic about 4 minutes, feature table) and the create page (auto stop defaults and minimums, one cluster per 10 concurrent queries).
- Removed: the `system.query.history` query and `system.billing.usage` (column and table names not in the fetched pages).

Method: documentation only; no commands were run.
