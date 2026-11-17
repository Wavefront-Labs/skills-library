---
id: computing-software.data-engineering.dbt.snapshot-yaml-config-and-meta-columns
name: snapshot-yaml-config-and-meta-columns
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-snapshots, snapshot-meta-columns, snapshot-yaml, dbt-valid-from, dbt-valid-to, dbt-valid-to-current, dbt-scd-id, target-schema]
level: practitioner
status: gated
description: "Configure dbt snapshots in YAML (1.9+): relation, schema/database, snapshot_meta_column_names, dbt_valid_to_current, and querying current and as-of versions correctly."
sources:
  - https://docs.getdbt.com/docs/build/snapshots
  - https://docs.getdbt.com/reference/resource-configs/snapshot_meta_column_names
  - https://docs.getdbt.com/reference/resource-configs/dbt_valid_to_current
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot YAML config and meta columns

**Goal:** define snapshots declaratively and give consumers easy, correct history queries.

## YAML-defined snapshot (1.9+)
```yaml
# snapshots/crm.yml
snapshots:
  - name: customers_snapshot
    relation: source('crm', 'customers')        # or ref('stg_crm__customers_for_snapshot')
    config:
      schema: snapshots                          # uses generate_schema_name in 1.9+ (target_schema = legacy, absolute)
      database: analytics
      unique_key: customer_id
      strategy: timestamp
      updated_at: updated_at
      dbt_valid_to_current: "to_date('9999-12-31')"   # instead of NULL for open rows; static SQL, no Jinja; to_date() is Snowflake syntax, `date '9999-12-31'` ran on DuckDB
      snapshot_meta_column_names:
        dbt_valid_from: valid_from
        dbt_valid_to: valid_to
        dbt_scd_id: customer_version_id
        dbt_updated_at: snapshot_updated_at
        dbt_is_deleted: is_deleted
```
Legacy `{% snapshot %}` SQL blocks still ran on dbt 1.12.6 (with `target_schema` taken literally); new projects should use YAML. Transformations belong in an upstream ephemeral/view model referenced by `relation`.

## Meta columns
| Column | Meaning |
|---|---|
| `dbt_valid_from` | When this version became current (from `updated_at` or snapshot time for check strategy) |
| `dbt_valid_to` | When it was superseded; NULL (or `dbt_valid_to_current`) for current |
| `dbt_scd_id` | Unique id per version (a hash of the unique key and the timestamp: `updated_at`, or the snapshot time for the check strategy; per the strategy macros) |
| `dbt_updated_at` | The `updated_at` value used |
| `dbt_is_deleted` | With `hard_deletes: new_record` |

## Querying
```sql
-- current
select * from {{ ref('customers_snapshot') }} where valid_to = '9999-12-31'
-- as of a point in time
select * from {{ ref('customers_snapshot') }}
where valid_from <= '2026-06-30' and valid_to > '2026-06-30'
-- join facts to the version valid at event time
from fct_orders o join customers_snapshot c
  on o.customer_id = c.customer_id and o.ordered_at >= c.valid_from and o.ordered_at < c.valid_to
```
Using a far-future `dbt_valid_to_current` makes the half-open range join work without `coalesce`.

## Gotchas
- Changing `dbt_valid_to_current` on an existing snapshot: existing current rows keep NULL, only newly inserted rows get the new value; the snapshot then shows in `state:modified` with a warning, and you update old rows manually (dbt docs). Renaming meta columns on an existing table: migrate manually (gated: unconfirmed, source is paywalled or blocked).
- Snapshots are never dropped by `--full-refresh` (by design): history is irreplaceable. Back them up.
- Build a typed, documented dimension model on top (`dim_customers_history`) rather than exposing raw snapshot tables.

## Verify
- [ ] Exactly one current row per key (test with `dbt_utils.unique_combination_of_columns` on key + valid_to filter).
- [ ] As-of join returns one row per fact.
