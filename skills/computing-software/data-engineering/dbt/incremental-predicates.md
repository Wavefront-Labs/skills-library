---
id: computing-software.data-engineering.dbt.incremental-predicates
name: incremental-predicates
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, incremental-models, incremental-predicates, merge-performance, dbt-internal-dest, snowflake, bigquery, databricks, pruning]
level: advanced
status: gated
description: "Speed up dbt incremental MERGEs on large targets with incremental_predicates so the warehouse prunes the destination table, with per-adapter syntax and correctness traps."
sources:
  - https://docs.getdbt.com/docs/build/incremental-strategy#about-incremental_predicates
  - https://docs.getdbt.com/reference/resource-configs/snowflake-configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# incremental_predicates

**Goal:** an incremental `merge` into a multi-billion-row table scans only recent partitions of the target, not the whole thing.

## Problem
dbt's merge joins source (new rows) to the **entire** destination on `unique_key`. Filtering the source with `is_incremental()` does not limit the target scan. On large tables the merge cost grows with table size.

## Config
```sql
{{ config(
    materialized = 'incremental',
    incremental_strategy = 'merge',
    unique_key = 'event_id',
    cluster_by = ['event_date'],                       -- Snowflake: makes the predicate prune (gated: unconfirmed, source is paywalled or blocked)
    incremental_predicates = [
      "DBT_INTERNAL_DEST.event_date >= dateadd(day, -3, current_date)"
    ]
) }}

select * from {{ ref('stg_events') }}
{% if is_incremental() %}
  where event_date >= dateadd(day, -3, current_date)
{% endif %}
```
`DBT_INTERNAL_DEST` is the alias dbt uses for the target in merge SQL (and `DBT_INTERNAL_SOURCE` for new data). The predicates are ANDed into the `ON` clause (seen in the debug SQL of a dbt-duckdb merge run).

## Correctness rule
The target predicate window must be **at least as wide** as any row that could match. If a late event for 10 days ago arrives and the predicate only covers 3 days, the merge will not find the existing row and **inserts a duplicate**. Align with the source lookback and your late-data policy; add a uniqueness test.

## Adapter notes
- Snowflake: predicate on the clustering key (or date column with natural clustering) enables micro-partition pruning on the target (gated: unconfirmed, source is paywalled or blocked).
- BigQuery: prefer `insert_overwrite` with `partitions` for time-partitioned facts; `incremental_predicates` with `merge` should prune when filtering the partition column (gated: unconfirmed, source is paywalled or blocked).
- Databricks/Spark: predicates on partition or liquid clustering columns; `incremental_strategy: replace_where` is a Databricks option (gated: unconfirmed, source is paywalled or blocked).
- `delete+insert`: in dbt-core's default macro the predicates are ANDed onto the `delete from <target> as DBT_INTERNAL_DEST where (key) in (...)` statement, so `DBT_INTERNAL_DEST.` works there. The dbt-duckdb adapter overrides the macro without that alias and failed with `Referenced table "DBT_INTERNAL_DEST" not found`; check the compiled SQL on your adapter. The dbt docs describe the alias only for `merge`.

## Dynamic window via var
```sql
incremental_predicates = ["DBT_INTERNAL_DEST.event_date >= dateadd(day, -" ~ var('lookback_days', 3) ~ ", current_date)"]
```
Use the same var in the source filter so they stay in sync.

## Verify
- [ ] Query profile of the merge shows partitions/micro-partitions scanned on target << total.
- [ ] `unique` test on `event_id` passes after runs that include late-arriving rows.
