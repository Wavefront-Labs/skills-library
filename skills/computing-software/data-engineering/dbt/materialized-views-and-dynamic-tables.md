---
id: computing-software.data-engineering.dbt.materialized-views-and-dynamic-tables
name: materialized-views-and-dynamic-tables
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-materializations, dbt-materialized-view, dbt-dynamic-table, target-lag, on-configuration-change, snowflake, bigquery, databricks, postgres]
level: advanced
status: docs-checked
description: "Use dbt materialized_view and Snowflake dynamic_table materializations: adapter support, target_lag and refresh configs, on_configuration_change, and vs incremental."
sources:
  - https://docs.getdbt.com/docs/build/materializations#materialized-view
  - https://docs.getdbt.com/reference/resource-configs/snowflake-configs#dynamic-tables
  - https://docs.getdbt.com/reference/resource-configs/on_configuration_change
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Materialized views and dynamic tables in dbt

**Goal:** let the warehouse keep a model fresh continuously (or on a lag target) instead of dbt rebuilding it on a schedule.

## Support
dbt's built-in materializations include `materialized_view`. Snowflake uses `dynamic_table`, configured with `target_lag`, `snowflake_warehouse` and `refresh_mode`. For the refresh options of other adapters, read that adapter's configs page; this skill does not restate them.

## Snowflake example
```sql
{{ config(
    materialized='dynamic_table',
    snowflake_warehouse='transforming_xs',
    target_lag='15 minutes',
    refresh_mode='INCREMENTAL',              -- AUTO / FULL / INCREMENTAL
    on_configuration_change='apply'
) }}
select o.order_id, o.amount, c.segment
from {{ ref('stg_orders') }} o join {{ ref('stg_customers') }} c using (customer_id)
```
Set upstream intermediate dynamic tables to `target_lag='downstream'` so they refresh only as needed by consumers.

## on_configuration_change
When the config (e.g. lag, refresh interval) changes but SQL does not:
- `apply` (default): attempt to update the existing object if possible, avoiding a complete rebuild.
- `continue` and `fail` are the other settings; read the on_configuration_change page for their exact behaviour (`fail` is the usual choice for prod change control).

## When to choose these vs incremental
- **Yes:** simple-to-moderate SQL, freshness needs of minutes, platform can incrementally maintain it (check the platform's restrictions on incremental maintenance).
- **No:** complex logic with unsupported constructs, need for dbt-controlled backfills, cross-database sources, or models where you need exact refresh timing tied to upstream jobs.

## Gotchas
- dbt tests run when dbt runs, not when the platform refreshes; freshness-sensitive tests may see stale data.
- Snowflake: `refresh_mode` can be AUTO, FULL or INCREMENTAL; check in Snowflake which mode was actually chosen, since a full refresh can cost much more.
- Cost moves from dbt jobs to the warehouse's background refresh: monitor separately.

## Verify
- [ ] Object exists with the expected type and lag/refresh settings (check in the warehouse).
- [ ] Refresh history shows refreshes meeting the lag target.

## Checked

2026-10-28. Confirmed against: dbt materializations page, Snowflake configs page (dynamic_table, target_lag incl. downstream and minutes format, snowflake_warehouse, refresh_mode AUTO|FULL|INCREMENTAL), on_configuration_change page (apply default; apply|continue|fail). Removed (not confirmable in the fetched pages): adapter support table (BigQuery, Databricks, Postgres, Redshift options), dbt 1.6 gate, SQL-change rebuild claim, SHOW/INFORMATION_SCHEMA names, incremental restriction list.

Method: documentation only; no commands were run.
