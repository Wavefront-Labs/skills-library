---
id: computing-software.data-engineering.data-modelling.backfilling-new-columns
name: backfilling-new-columns
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, schema-migration, column-backfill, batched-updates, on-schema-change, incremental-backfill, historical-recompute, lock-avoidance, default-values]
level: advanced
status: gated
description: "Backfill a new column across history: default vs recompute, batched UPDATEs in OLTP, partition-wise rewrites in warehouses, dbt on_schema_change backfills, and checks."
sources:
  - https://www.postgresql.org/docs/current/sql-altertable.html
  - https://docs.getdbt.com/docs/build/incremental-models#what-if-the-columns-of-my-incremental-model-change
  - https://docs.delta.io/latest/delta-update.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backfilling new columns

**Goal:** a new column holds correct values for all historical rows (or an explicit, documented "unknown"), without locking production or blowing the compute budget.

## Decide what history should contain
- **Recomputable** from data you still have (derived from other columns or source history): recompute.
- **Not recomputable** (new upstream field only exists going forward): leave NULL or a sentinel, and document the start date in the column description (`populated from 2026-10-16`). Do not invent values.

## OLTP databases (Postgres example)
```sql
alter table orders add column channel text;                        -- metadata-only, fast
-- Postgres 11+: ADD COLUMN ... DEFAULT 'web' is also metadata-only (no rewrite) for non-volatile defaults; a volatile default such as clock_timestamp() rewrites the table (current ALTER TABLE docs; the 11 version number is unconfirmed)
-- batched backfill to avoid long locks and WAL spikes
do $$
declare n int;
begin
  loop
    update orders set channel = derive_channel(source_code)
    where order_id in (select order_id from orders where channel is null limit 10000);
    get diagnostics n = row_count;
    exit when n = 0;
    commit;
    perform pg_sleep(0.2);
  end loop;
end $$;
```
The PostgreSQL docs confirm COMMIT inside an anonymous DO block ends the transaction and starts a new one; the batched loop itself was not run (no PostgreSQL available) (gated: unconfirmed, source is paywalled or blocked). Add `NOT NULL` afterwards (Postgres 12+ (version unconfirmed): add a `CHECK (channel is not null) NOT VALID`, `VALIDATE CONSTRAINT`, then `SET NOT NULL` to avoid a long exclusive scan).

## Warehouses and lakes
- Rewrite per partition: `insert overwrite ... partition (dt)` / Delta `MERGE` or `UPDATE ... WHERE dt BETWEEN ...` (Delta not run (gated: unconfirmed, source is paywalled or blocked)) in date chunks; track progress in a control table so it is resumable.
- Columnar formats rewrite whole files for UPDATEs: chunk by partition to keep each job bounded.
- dbt incremental models: `on_schema_change='append_new_columns'` adds the column for new rows only (tested on dbt 1.12.6/DuckDB: old row stayed NULL, new row got the value); history needs either `--full-refresh` (expensive) or a one-off backfill run with a var widening the incremental window (`dbt run -s model --vars '{backfill_start: 2024-01-01}'`) in batches.

## Verify
- [ ] `select count(*) where new_col is null` is zero (or equals the documented pre-availability rows).
- [ ] Spot-check recomputed values against an independent calculation for a few partitions.
- [ ] No lock waits / replication lag alerts during the OLTP backfill.
