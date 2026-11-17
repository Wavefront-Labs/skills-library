---
id: computing-software.data-engineering.dbt.base-models-in-staging
name: base-models-in-staging
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, base-models, staging-layer, project-structure, union-sources]
level: practitioner
status: docs-checked
description: "Use base models under dbt staging to clean tables that must be joined or unioned before the staging model, e.g. deleted-record tables or per-region copies."
sources:
  - https://docs.getdbt.com/best-practices/how-we-structure/2-staging
  - https://docs.getdbt.com/reference/dbt-jinja-functions/ref
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Base models within staging

**Goal:** keep the one-staging-model-per-source-table rule even when a source entity is spread over several raw tables.

## When to use
- Source keeps deletes in a separate table (`customers` + `deleted_customers`).
- Same table replicated per region/shard (`shop_us.orders`, `shop_eu.orders`) needing a union.
- A raw table needs light cleaning before a join that defines the staging grain.

## Layout
```
models/staging/shop/
  base/
    base_shop__customers.sql
    base_shop__deleted_customers.sql
  stg_shop__customers.sql
```
```sql
-- base/base_shop__customers.sql
select id as customer_id, email, updated_at from {{ source('shop', 'customers') }}

-- stg_shop__customers.sql
select c.*, d.deleted_at is not null as is_deleted
from {{ ref('base_shop__customers') }} c
left join {{ ref('base_shop__deleted_customers') }} d using (customer_id)
```
Union variant: one base model per symmetrical source (for example per region), unioned in the staging model.

## Config
```yaml
models:
  my_project:
    staging:
      +materialized: view
      shop:
        base:
          +materialized: view
```

## Rules
- Base models source the raw data directly and do the non-joining transformations (renames, casts); the staging model joins them.
- Base models live in a sub-directory of the source system folder under staging.
- Use base models only when joins are needed to stage a concept (for example delete tables or unioning symmetrical sources); otherwise keep one staging model per source table.

## Verify
`dbt ls --select base_shop__customers+` shows only the staging model (and its descendants) as consumers.

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: dbt guidance on base models: a sub-directory of the source system folder under staging, base models source raw data and do the non-joining transformations, staging models join them, typical cases are separate delete tables or unioning symmetrical sources; staging directory is materialized as views. Removed unconfirmed claims about `dbt_utils.union_relations` output columns, ephemeral base models and reference restrictions.

Method: documentation only; no commands were run.
