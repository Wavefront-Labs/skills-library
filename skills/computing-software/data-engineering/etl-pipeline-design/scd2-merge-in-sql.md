---
id: computing-software.data-engineering.etl-pipeline-design.scd2-merge-in-sql
name: scd2-merge-in-sql
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, scd2-merge, scd-type-2, merge, incremental-load, change-detection, hash-diff, idempotency]
level: advanced
status: gated
description: "Implement SCD type 2 loads with a single MERGE (union-of-changes trick): hash-based change detection, idempotent reruns, deletes and multiple changes per batch."
sources:
  - https://docs.databricks.com/en/delta/merge.html#slowly-changing-data-scd-type-2-operation-into-delta-tables
  - https://docs.snowflake.com/en/sql-reference/sql/merge
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCD2 MERGE in SQL

**Goal:** apply a batch of source changes to a type 2 dimension: close the current row and insert the new version, atomically and rerunnable.

Run here on DuckDB 1.5.6 (MERGE INTO, same statement): a changed key (1) was closed and re-inserted, an unchanged key (2) untouched, a new key (3) inserted once, and a second run of the same batch changed 0 rows. Snowflake and Databricks syntax and semantics were not run (gated: unconfirmed, source is paywalled or blocked).

## Target shape
`dim_customer(customer_sk, customer_id, name, segment, row_hash, valid_from, valid_to, is_current)`

## Single MERGE with the union trick
A MERGE applies one action per matched source row (a changed key needs two effects, so it needs two source rows; multi-match behaviour is engine-specific (gated: unconfirmed, source is paywalled or blocked)); a change needs two (close old, insert new). Feed changed keys twice: once with the real key (to match and close) and once with a NULL merge key (forces insert).
```sql
merge into dim_customer t
using (
  -- rows to insert as new versions (merge_key null => never matches)
  select null as merge_key, s.* from stg_customer_changes s
  join dim_customer d on d.customer_id = s.customer_id and d.is_current
  where d.row_hash <> s.row_hash
  union all
  -- rows to match current versions (close) or insert brand-new keys
  select s.customer_id as merge_key, s.* from stg_customer_changes s
) src
on t.customer_id = src.merge_key and t.is_current
when matched and t.row_hash <> src.row_hash then update set
  valid_to = src.effective_at, is_current = false
when not matched then insert (customer_id, name, segment, row_hash, valid_from, valid_to, is_current)
  values (src.customer_id, src.name, src.segment, src.row_hash, src.effective_at, '9999-12-31', true);
```
Brand-new keys arrive only via the second branch (no current row to match) and are inserted once. Unchanged rows match with equal hashes and do nothing.

## Preparing the batch
- `row_hash = md5(concat_ws('||', coalesce(name,''), coalesce(segment,'')))` over tracked attributes.
- **One row per key per batch.** If the source has several changes for a key in one batch, either keep the latest (`qualify row_number() ... = 1`) and accept losing intermediate versions, or process changes sequentially (loop per sequence number) / build history with window functions:
```sql
select *, lead(effective_at) over (partition by customer_id order by effective_at) as next_effective_at
```
  then insert all intermediate versions with computed `valid_to`, and close the current row at the first change.
- Use a source effective timestamp (change time), not `current_timestamp`, so reruns produce identical results.

## Idempotency
Rerunning the same batch: hashes now equal the current rows -> no updates, no inserts. Make sure staging is deduplicated, or reruns may insert duplicate current rows.

## Deletes
Soft-close on source delete: add a branch `when matched and src.is_deleted then update set valid_to = src.effective_at, is_current = false` (and exclude deleted rows from the insert branch).

## Alternatives
dbt snapshots, Databricks AUTO CDC flows (Python `create_auto_cdc_flow` with `stored_as_scd_type=2`, which replaces `apply_changes()` per the Databricks docs), Snowflake streams + tasks. Use them unless you need custom logic.

## Verify
- [ ] Tests: exactly one `is_current` per key; no overlapping `[valid_from, valid_to)` per key.
- [ ] Rerun of the same batch changes 0 rows.
