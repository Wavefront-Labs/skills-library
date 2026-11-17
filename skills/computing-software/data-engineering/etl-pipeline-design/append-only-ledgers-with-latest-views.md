---
id: computing-software.data-engineering.etl-pipeline-design.append-only-ledgers-with-latest-views
name: append-only-ledgers-with-latest-views
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, append-only-ledger, latest-row-view, immutable-data, deduplication]
level: advanced
status: gated
description: "Store changing source data as an append-only ledger and expose current state with latest-row views: schema, dedup with QUALIFY, deletes, compaction and costs."
sources:
  - https://docs.snowflake.com/en/sql-reference/constructs/qualify
  - https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#qualify_clause
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Append-only ledgers with latest-row views

**Goal:** never update or lose raw history: every extracted version is appended; current state is a view.

## Ledger table
```sql
create table raw.customers_ledger (
  customer_id     bigint,
  payload         variant,          -- or typed columns
  source_updated_at timestamp_ntz,
  op              varchar,          -- 'I','U','D' if known
  _extracted_at   timestamp_ntz,
  _batch_id       varchar
) cluster by (to_date(_extracted_at));
```
Loads are pure appends (cheap, idempotent per batch id: delete-by-batch then insert if a batch is rerun).

Run here on DuckDB 1.5.6 (the `row_number()` view with `* exclude (rn)`, the `qualify` form and the `lead` query all executed): a deleted key (op `D`) dropped out, a NULL `op` was kept, and ties on `source_updated_at` were resolved by `_extracted_at`. The Snowflake DDL above (`variant`, `cluster by`) is Snowflake syntax and was not run (gated: unconfirmed, source is paywalled or blocked).

## Latest view
```sql
create or replace view core.customers_current as
select * exclude (rn) from (
  select *, row_number() over (partition by customer_id
                               order by source_updated_at desc, _extracted_at desc) rn
  from raw.customers_ledger)
where rn = 1 and coalesce(op, 'U') <> 'D';
-- Snowflake/BigQuery/Databricks: same with QUALIFY row_number() over (...) = 1
```
Tie-break on extraction time so the order is deterministic.

## History for free
- As-of queries: filter `source_updated_at <= :as_of` before ranking.
- SCD2 dimension: `lead(source_updated_at) over (partition by customer_id order by source_updated_at)` as `valid_to`.

## Performance
- The view scans the full ledger. For large ledgers materialise the current state incrementally (dbt incremental merge on key with the latest rows of new batches) and keep the view for audits.
- Cluster/partition by extraction date; prune old partitions by moving them to cheaper storage if retention allows.

## Deletes
Full-extract sources: detect deletes by comparing the latest full snapshot to the current set and append tombstone rows (`op = 'D'`).

## Verify
Count of rows in the current view equals distinct keys in the source; rerunning a batch does not change counts.
