---
id: computing-software.data-engineering.etl-pipeline-design.incremental-aggregates-and-rollups
name: incremental-aggregates-and-rollups
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, incremental-aggregation, rollups, late-data, partition-overwrite]
level: advanced
status: draft
description: "Maintain aggregates incrementally: recompute affected partitions, merge deltas for additive measures, sketches for distinct counts, and handling late or corrected data."
sources:
  - https://docs.getdbt.com/docs/build/incremental-strategy
  - https://docs.snowflake.com/en/sql-reference/functions/hll
  - https://datasketches.apache.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incremental aggregates and rollups

**Goal:** keep daily/hourly aggregates current without rescanning all history, and still correct when data arrives late.

## Strategy 1: recompute affected partitions (default choice)
```sql
-- dbt incremental, insert_overwrite / delete+insert by day
{{ config(materialized='incremental', incremental_strategy='delete+insert', unique_key='event_date') }}
select event_date, country, count(*) events, sum(revenue) revenue
from {{ ref('fct_events') }}
{% if is_incremental() %}
where event_date in (select distinct event_date from {{ ref('fct_events') }}
                     where _loaded_at > (select max(_agg_loaded_at) from {{ this }}))
{% endif %}
group by 1, 2
```
Find which days received new rows (by load timestamp), recompute those days fully. Correct for any measure, including distinct counts.

## Strategy 2: delta merge (additive measures only)
Aggregate only new rows and add them: `merge ... when matched then update set events = t.events + s.events`. Fast, but breaks on reprocessing (double counting) and cannot handle updates/deletes of facts. Use only with exactly-once inputs.

## Distinct counts
Not additive across partitions. Store sketches:
```sql
select event_date, hll_export(hll_accumulate(user_id)) users_hll from events group by 1;   -- Snowflake
-- combine: hll_estimate(hll_combine(hll_import(users_hll)))
```
BigQuery: `HLL_COUNT.INIT/MERGE`; Databricks: `hll_sketch_agg` / `hll_union_agg`. Approximate (around 1-2% error).

## Late data window
Also recompute the last N days on every run (e.g. 3) as a safety net, and support an explicit backfill range variable.

## Gotchas
- Using event time to choose partitions misses late rows; drive by load time, recompute by event time.
- Aggregates over SCD2 dimensions: decide current vs historical attributes; changing current attributes requires recomputing all history.

## Verify
Weekly test: full recompute of a sample month equals the incrementally maintained values.
