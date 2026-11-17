---
id: computing-software.data-engineering.dbt.adapter-specific-table-configs
name: adapter-specific-table-configs
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, adapter-specific-configs, cluster-by, partition-by, transient, file-format, liquid-clustering, dbt-snowflake, dbt-bigquery, dbt-databricks]
level: practitioner
status: docs-checked
description: "Set warehouse-specific physical configs in dbt: Snowflake cluster_by/transient/warehouse, BigQuery partition_by/cluster_by/expiration, Databricks file_format/liquid_clustered_by."
sources:
  - https://docs.getdbt.com/reference/resource-configs/snowflake-configs
  - https://docs.getdbt.com/reference/resource-configs/bigquery-configs
  - https://docs.getdbt.com/reference/resource-configs/databricks-configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Adapter-specific table configs

**Goal:** dbt-built tables get the right physical layout and cost settings for the warehouse they live in.

## Snowflake
```sql
{{ config(
    materialized='table',
    cluster_by=['order_date', 'region'],      -- adds CLUSTER BY and an ORDER BY on build
    transient=false,                         -- default true for tables: no Fail-safe, cheaper
    snowflake_warehouse='TRANSFORM_L',       -- per-model warehouse
    query_tag='dbt_fct_orders',
    copy_grants=true                         -- keep grants on create or replace
) }}
```
- dbt-snowflake tables are **transient by default**: no Fail-safe. Set `+transient: false` for critical marts.
- `snowflake_warehouse` overrides the virtual warehouse for that model (see Configuring virtual warehouses).

## BigQuery
```sql
{{ config(
    materialized='incremental',
    incremental_strategy='insert_overwrite',
    partition_by={'field': 'event_date', 'data_type': 'date', 'granularity': 'day'},
    cluster_by=['customer_id'],
    require_partition_filter=true,
    partition_expiration_days=400,
    labels={'team': 'growth'},
    kms_key_name='projects/p/locations/eu/keyRings/r/cryptoKeys/k'
) }}
```
- `partition_by` on a `timestamp` or `datetime` column supports `granularity` hour, day, month or year (a `date` column: day, month, year); integer range partitioning uses `data_type: int64` plus `range: {start, end, interval}`.
- `require_partition_filter: true` makes any query on the model fail unless it filters on the partition column.

## Databricks
```sql
{{ config(
    materialized='incremental',
    file_format='delta',
    liquid_clustered_by=['event_date', 'user_id'],   -- or partition_by=['event_date'] (+ zorder)
    incremental_strategy='merge',
    tblproperties={'delta.enableChangeDataFeed': 'true'},
    location_root='s3://lake/gold'                    -- external tables when needed
) }}
```
- `liquid_clustered_by` uses Delta Liquid Clustering; `partition_by` is the alternative.
- `incremental_strategy: replace_where` with `incremental_predicates` replaces matching rows atomically.

## Setting defaults per folder
```yaml
models:
  my_project:
    marts:
      +transient: false
      +cluster_by: ['report_date']      # careful: applies to every model in folder
```

## Gotchas
- Snowflake `automatic_clustering` has no effect except on accounts that still have the deprecated manual clustering enabled; automatic clustering is on by default in Snowflake.
- Databricks: when `liquid_clustered_by` is set, dbt-databricks runs `OPTIMIZE` after each run (set `DATABRICKS_SKIP_OPTIMIZE=true` to skip it), and `liquid_clustered_by` must not be combined with `auto_liquid_cluster` on one model.

## Verify
- [ ] Inspect created table DDL (`show create table`, `INFORMATION_SCHEMA`) for clustering/partitioning.
- [ ] Query profile of a typical consumer query shows pruning.

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: Snowflake: tables built by dbt are transient by default, `cluster_by` orders the table and adds clustering keys, `automatic_clustering` is effectively a no-op except on accounts with manual clustering, `copy_grants` default false, `snowflake_warehouse` and `query_tag` exist. BigQuery: `partition_by` granularity values and `range` form, `require_partition_filter`, `partition_expiration_days`, `labels`, `kms_key_name`. Databricks: `liquid_clustered_by`, `location_root`, `tblproperties`, `file_format` values, `replace_where` with `incremental_predicates`, OPTIMIZE behaviour and the `auto_liquid_cluster` restriction. Removed unconfirmed claims about silently ignored keys, immutable BigQuery partition specs, reclustering cost advice and a DBR 13.3 gate.

Method: documentation only; no commands were run.
