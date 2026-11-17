---
id: computing-software.data-engineering.data-modelling.scd-types-1-3-and-6
name: scd-types-1-3-and-6
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, slowly-changing-dimensions, scd-type-6, scd-type-1, scd-type-3, hybrid-scd, current-value-columns, dimension-design]
level: practitioner
status: verified
description: "Choose and implement SCD types beyond type 2: type 1 overwrite, type 3 previous-value columns, and type 6 hybrid (type 2 rows plus current-value columns), per attribute."
sources:
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-6/
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-3/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCD types 1, 3 and 6

**Goal:** each dimension attribute has a deliberate change-handling rule matching how the business wants to report history.

## Decide per attribute, not per table
| Attribute | Business need | Type |
|---|---|---|
| customer email, typo fixes | always current, no history | 1 |
| sales region | report historical sales under the region at time of sale | 2 |
| sales region (some reports) | also "restate all history under today's region" | 6 |
| product category after one-time reorg | compare old vs new classification side by side | 3 |

## Type 1: overwrite
```sql
update dim_customer set email = s.email from stg_customer s
where dim_customer.customer_id = s.customer_id and dim_customer.email <> s.email;
```
In a type 2 dimension, type 1 attributes must be updated on **all** rows of the entity, or reports mix old and new values.

## Type 3: previous value column
```sql
alter table dim_product add column prior_category varchar, add column category_changed_at date;
update dim_product set prior_category = dim_product.category, category = s.category, category_changed_at = current_date
from stg_product s where dim_product.product_id = s.product_id and dim_product.category <> s.category;
```
Qualify `dim_product.category` on the right-hand side: the unqualified column is ambiguous because `stg_product` also has `category` (DuckDB raised a binder error). DuckDB also allows only one action per `alter table`, so add the two columns in two statements there. Types 1, 3 and 6 SQL was run on DuckDB 1.5 and gave the expected rows (type 6 set `current_region` = West on both history rows). Only one prior value is kept. Suited to planned reorganisations ("as-was vs as-is" for one change).

## Type 6: type 2 rows + current columns
Each row keeps the historical value; a `current_*` column on every row of the entity holds today's value.
```
customer_sk | customer_id | region (historic) | current_region | valid_from | valid_to   | is_current
101         | C9          | North             | West           | 2024-01-01 | 2025-06-01 | false
102         | C9          | West              | West           | 2025-06-01 | 9999-12-31 | true
```
Facts join on `customer_sk`; report by `region` for as-was, by `current_region` for as-is, no extra join.
Load step after the normal type 2 merge:
```sql
update dim_customer d set current_region = c.region
from dim_customer c
where c.customer_id = d.customer_id and c.is_current and d.current_region is distinct from c.region;
```
In dbt: build the type 2 history from a snapshot, then a model that joins current rows back:
```sql
select h.*, cur.region as current_region
from {{ ref('dim_customer_history') }} h
join {{ ref('dim_customer_history') }} cur on cur.customer_id = h.customer_id and cur.is_current
```

## Gotchas
- Type 6 current columns turn every change into an update of all historical rows of that entity: cheap in a rebuilt dbt model, costly in in-place merges on huge dims.
- Mixing types in one dimension needs documentation in the data dictionary per column.
- Type 2 on noisy attributes (last_login) explodes row counts: make them type 1 or move to a fact/mini-dimension.

## Verify
- [ ] As-was and as-is reports both reconcile to total sales.
- [ ] Every entity has exactly one `is_current` row; `current_*` identical across its rows.
