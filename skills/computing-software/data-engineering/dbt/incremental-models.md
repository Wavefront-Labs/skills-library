---
id: computing-software.data-engineering.dbt.incremental-models
name: incremental-models
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-cloud, incremental-models, is-incremental, unique-key, incremental-strategy, merge, delete-insert, insert-overwrite, microbatch, on-schema-change, full-refresh, late-arriving-data, lookback, event-time, snowflake, bigquery, databricks, redshift, postgres, analytics-engineering, sql]
level: practitioner
status: gated
description: "Build dbt incremental models that stay correct: is_incremental() filters with lookback, unique_key, choosing merge/delete+insert/insert_overwrite/microbatch, schema changes and full refreshes."
sources:
  - https://docs.getdbt.com/docs/build/incremental-models
  - https://docs.getdbt.com/docs/build/incremental-strategy
  - https://docs.getdbt.com/docs/build/incremental-microbatch
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# dbt incremental models — fast builds without silent drift

**Goal:** turn an expensive table into an incremental model that processes only new or changed rows, handles late data, and can be rebuilt from scratch to prove it still matches.

## 1. Decide if it should be incremental at all
Stay with `table` until a full rebuild is too slow or costly (rule of thumb: many minutes, or the source is tens of millions of rows and growing). Incremental adds logic you must test. Good candidates: append-heavy event/fact tables with a reliable timestamp.

## 2. The basic pattern
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    on_schema_change='append_new_columns'
) }}

select order_id, customer_id, status, amount, updated_at
from {{ ref('stg_orders') }}
{% if is_incremental() %}
  where updated_at > (select dateadd(day, -3, max(updated_at)) from {{ this }})
{% endif %}
```
- `is_incremental()` is true only when the target exists, is a table, the model is incremental, and `--full-refresh` was not passed.
- `{{ this }}` is the existing target relation.
- **The 3-day lookback is deliberate:** filtering on `> max(updated_at)` alone drops late-arriving rows and rows committed out of order. The lookback re-processes a window; `unique_key` makes that safe. Size it to your observed lateness.
- Date function syntax is adapter-specific (`dateadd` on Snowflake/Redshift, `timestamp_sub` on BigQuery (gated: unconfirmed, source is paywalled or blocked)); the `dbt.dateadd()` cross-db macro worked on DuckDB.

## 3. Choose the strategy
| Strategy | What it does | Use when |
|---|---|---|
| `append` | inserts only | immutable events, no dedupe needed |
| `merge` | MERGE on `unique_key` | updates to existing rows; default strategy per adapter is on each adapter's page (gated: unconfirmed, source is paywalled or blocked) |
| `delete+insert` | delete matching keys, insert batch | merge is slow or unsupported on your adapter; batch replaces by key |
| `insert_overwrite` | replace whole partitions | partitioned tables on adapters that support it (BigQuery/Spark (gated: unconfirmed, source is paywalled or blocked)); late data lands in known partitions |
| `microbatch` | dbt splits work into `batch_size` time windows by `event_time` (dbt 1.9+) | large time-series; you want per-batch retries and easy backfills |

Supported strategies and defaults vary by adapter: the dbt incremental-strategy page lists only the five strategy names and per-adapter support, so check your adapter page.
- **Gotcha:** `unique_key` must be truly unique in the *new batch*. Duplicates in the source make MERGE fail ("duplicate row detected" on Snowflake/BigQuery (gated: unconfirmed, source is paywalled or blocked)), or multiply rows with delete+insert. Deduplicate in the model with `qualify row_number() over (partition by order_id order by updated_at desc) = 1`.
- Use `incremental_predicates` (e.g. restrict target scan to the last 7 days) to stop MERGE scanning the whole target.

Microbatch sketch (`event_time`, `begin`, `batch_size` are required; `lookback` defaults to 1; dbt-duckdb rejected `unique_key` with microbatch while dbt-postgres requires it, so it is adapter-dependent):
```sql
{{ config(materialized='incremental', incremental_strategy='microbatch',
          event_time='event_ts', batch_size='day', lookback=2, begin='2024-01-01') }}
select * from {{ ref('stg_events') }}   -- no is_incremental() block; dbt filters upstream refs that declare event_time
```
Backfill a range: `dbt run -s fct_events --event-time-start "2026-09-01" --event-time-end "2026-09-08"` (both flags must be given together; the end is exclusive: a 09-01 to 09-04 run built 3 daily batches, checked on DuckDB). Upstream refs without `event_time` are fully scanned on every batch.

## 4. Schema changes
`on_schema_change`: `ignore` (default; new columns silently missing, checked), `append_new_columns` (checked), `sync_all_columns` (added and dropped columns, checked), `fail` (the run errors with a compilation error when columns differ, checked). New columns are NULL for historical rows unless you full-refresh. Prefer `fail` for critical marts so a human decides.

## 5. Full refresh and protection
- `dbt run -s my_model --full-refresh` rebuilds from scratch.
- For huge tables where a rebuild is dangerous, set `full_refresh: false` in config so an accidental `--full-refresh` is ignored for that model (checked: the table was not rebuilt and kept its old columns).
- Schedule a periodic full rebuild (or compare against one in a dev schema) to detect drift from logic changes — changed SQL never reapplies to old rows on its own.

## 6. Tests
- `unique` and `not_null` on `unique_key`.
- A recency/freshness test on `updated_at`.
- Compare row counts and sums between incremental and a full-refresh build in CI (e.g. with `audit_helper`).
See computing-software.data-engineering.data-quality.data-tests-and-freshness-slas.

## Verify
- [ ] Running the model twice in a row with no new source data changes zero rows.
- [ ] `unique` test on the key passes after several incremental runs.
- [ ] A late row (timestamp inside the lookback) inserted at the source appears after the next run.
- [ ] A full-refresh build and the incremental table agree on row count and key aggregates.
- [ ] `on_schema_change` is set deliberately, not left as the silent default.
