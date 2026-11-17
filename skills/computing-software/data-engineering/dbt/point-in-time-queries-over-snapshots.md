---
id: computing-software.data-engineering.dbt.point-in-time-queries-over-snapshots
name: point-in-time-queries-over-snapshots
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-snapshots, snapshot-point-in-time, scd-type-2, as-of-join, dbt-valid-from, dbt-valid-to, history]
level: practitioner
status: docs-checked
description: "Query dbt snapshots correctly: as-of joins of facts to dimension history, current-row filters, building SCD2 dims on top of snapshots, and boundary conventions."
sources:
  - https://docs.getdbt.com/docs/build/snapshots
  - https://docs.getdbt.com/reference/resource-configs/snapshot_meta_column_names
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Point-in-time queries over snapshots

**Goal:** answer "what did the customer record look like when this order was placed" from snapshot tables, with no gaps or double matches.

## Snapshot columns
- `dbt_valid_from`: when this version became current (source `updated_at` for the timestamp strategy; for the check strategy, `updated_at` if configured, else the current timestamp).
- `dbt_valid_to`: when it was superseded; `null` for current rows (or a far-future date with `dbt_valid_to_current` config in 1.9+).
- `dbt_scd_id`, `dbt_updated_at`.

## Current state
```sql
select * from {{ ref('snap_customers') }}
where dbt_valid_to is null           -- or = to_date('9999-12-31') with dbt_valid_to_current
```

## As-of join (fact to dimension version)
```sql
select o.order_id, o.ordered_at, c.segment, c.country
from {{ ref('fct_orders') }} o
left join {{ ref('snap_customers') }} c
  on o.customer_id = c.customer_id
 and o.ordered_at >= c.dbt_valid_from
 and o.ordered_at <  coalesce(c.dbt_valid_to, '9999-12-31'::timestamp)
```
Half-open interval `[valid_from, valid_to)`: dbt sets the next version's `valid_from` equal to the previous `valid_to`, so `<=` on both ends would double-match at the boundary.

## Facts earlier than the first version
Orders placed before the first snapshot run have no matching version (snapshot history starts when you started snapshotting). Options: use the earliest version for anything before it:
```sql
and o.ordered_at < coalesce(c.dbt_valid_to, '9999-12-31')
and (o.ordered_at >= c.dbt_valid_from or c.is_first_version)
```
(where `is_first_version` is computed with `row_number() over (partition by customer_id order by dbt_valid_from) = 1` in a dim model).

## Build a clean SCD2 dim on top
```sql
-- models/marts/dim_customers_history.sql
-- generate_surrogate_key is a dbt_utils macro: see the dbt_utils docs for its arguments
select
  {{ dbt_utils.generate_surrogate_key(['customer_id', 'dbt_valid_from']) }} as customer_sk,
  customer_id, segment, country,
  dbt_valid_from as valid_from,
  coalesce(dbt_valid_to, '9999-12-31'::timestamp) as valid_to,
  dbt_valid_to is null as is_current
from {{ ref('snap_customers') }}
```
Facts can then store `customer_sk` resolved at load time (faster joins than range joins).

## Gotchas
- Check strategy without `updated_at`: `valid_from` is the current timestamp of the snapshot run, not when the change happened in the source. Snapshot frequency limits accuracy.
- Hard deletes: with `hard_deletes: new_record` (1.9+), a deletion version with `dbt_is_deleted = true` appears; exclude it in as-of joins if appropriate.
- Range joins are slow on big tables; precompute surrogate keys where it matters.
- Timezone consistency between `ordered_at` and `updated_at` matters.

## Verify
- [ ] Test: no order matches more than one version (`unique` test on order_id in the joined model).
- [ ] Spot-check a customer with known history.

## Checked

2026-11-02

- Confirmed: dbt snapshots page and snapshot_meta_column_names page: dbt_valid_from, dbt_valid_to, dbt_scd_id, dbt_updated_at, dbt_is_deleted, dbt_valid_to_current (1.9+), hard_deletes new_record (1.9+), check strategy defaulting to the current timestamp, and next-version valid_from equal to previous valid_to.
- Removed or changed: Removed the Snowflake/Databricks clustering claim; reworded the check-strategy timestamp claim; deferred generate_surrogate_key to dbt_utils docs.

Method: documentation only; no commands were run.
