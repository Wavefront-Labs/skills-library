---
id: computing-software.data-engineering.dbt.migrating-legacy-snapshots-to-yaml
name: migrating-legacy-snapshots-to-yaml
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, snapshot-migration, snapshots, yaml-snapshots, dbt-1-9]
level: advanced
status: docs-checked
description: "Migrate legacy {% snapshot %} SQL blocks to dbt 1.9+ YAML snapshots without losing history: keep relation names, target schema behaviour, and verify continuity."
sources:
  - https://docs.getdbt.com/docs/build/snapshots
  - https://docs.getdbt.com/reference/resource-configs/target_schema
  - https://docs.getdbt.com/docs/dbt-versions/core-upgrade/upgrading-to-v1.9
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating legacy snapshot blocks to YAML

**Goal:** move to YAML-defined snapshots (1.9+) and keep writing into the same existing snapshot table.

## Before
```sql
-- snapshots/orders_snapshot.sql
{% snapshot orders_snapshot %}
{{ config(target_schema='snapshots', unique_key='id', strategy='timestamp', updated_at='updated_at') }}
select * from {{ source('shop', 'orders') }}
{% endsnapshot %}
```

## After
```yaml
# snapshots/orders_snapshot.yml
snapshots:
  - name: orders_snapshot             # SAME name -> same table
    relation: source('shop', 'orders')
    config:
      schema: snapshots
      unique_key: id
      strategy: timestamp
      updated_at: updated_at
```
Delete the `.sql` block in the same commit.

## The schema trap
- Legacy `target_schema` is absolute: always `snapshots`, in every environment.
- YAML `schema` goes through the `generate_schema_name` macro, so the prod schema depends on your macro.
- To keep writing to the old table: keep `target_schema: snapshots` in the YAML config (still supported) or ensure `generate_schema_name` yields exactly the old schema in prod. Check the compiled relation before running in prod.

## Transformations in the old block
YAML snapshots take a `relation`, not SQL. Move any SQL into an ephemeral model and use `relation: ref('orders_for_snapshot')`.

## Procedure
1. Change in a branch; run `dbt compile` and compare the relation to the existing table name.
2. Run in a dev clone of the snapshot table; confirm it updates, not recreates (row count grows only by changes).
3. Deploy; first prod run should insert/close only changed rows.

## Verify
After the first run: no duplicate current rows per key, and the earliest `dbt_valid_from` is unchanged.

## Checked

2026-10-28. Confirmed against: snapshots page (v1.9 YAML form with relation and config.schema, target_schema optional since 1.9 and still settable, generate_schema_name use), upgrading-to-v1.9 page. Removed (not confirmable in the fetched pages): dbt ls --output-keys, default-macro schema naming, duplicate-definition error claim.

Method: documentation only; no commands were run.
