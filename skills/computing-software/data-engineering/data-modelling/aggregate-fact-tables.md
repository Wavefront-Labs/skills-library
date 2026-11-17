---
id: computing-software.data-engineering.data-modelling.aggregate-fact-tables
name: aggregate-fact-tables
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, aggregate-fact-tables, dimensional-modelling, rollups, performance]
level: advanced
status: gated
description: "Design aggregate fact tables over atomic facts: choosing grain and shrunken dimensions, keeping aggregates consistent, incremental refresh, and query routing."
sources:
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/aggregate-fact-table-cube/
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/shrunken-rollup-dimension/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Aggregate fact tables

**Goal:** fast dashboards over billions of atomic rows, without different numbers at different grains.

## Design
- Keep the **atomic** fact table as the source of truth; aggregates are derived, never loaded from a different source.
- Choose aggregate grain from real query patterns: e.g. `day x store x product_category` instead of `order_line`.
- Use **shrunken (rolled-up) dimensions** for the coarser grain (`dim_month`, `dim_product_category`) that are conformed subsets of the base dimensions (same attribute names and values).
- Only additive measures aggregate safely (sum, count). For non-additive measures (ratios, distinct counts) store components (numerator/denominator) or sketches (HLL) instead of the result.

```sql
create table agg_sales_day_store_category as
select d.date_key, s.store_key, p.category_key,
       sum(f.sales_amount) sales_amount, sum(f.quantity) quantity,
       count(*) line_count, hll_accumulate(f.customer_key) customer_hll   -- Snowflake HLL state (gated: unconfirmed, source is paywalled or blocked; not run)
from fct_sales f join dim_product p using (product_key)
join dim_date d using (date_key) join dim_store s using (store_key)
group by 1, 2, 3;
```

## Refresh
- Incremental by date partition: recompute affected days (including late-arriving facts) rather than appending.
- dbt incremental with `insert_overwrite`/merge on the date key; or materialized views / dynamic tables where the platform supports aggregation incrementally.

## Routing queries to aggregates
- BI semantic layers (Looker aggregate awareness, Power BI aggregations, Cube pre-aggregations, AtScale (gated: unconfirmed, source is paywalled or blocked)) route automatically.
- Otherwise expose aggregates as separate explores/datasets with clear names.

## Consistency checks
```sql
select (select sum(sales_amount) from fct_sales where date_key between 20261001 and 20261007)
     - (select sum(sales_amount) from agg_sales_day_store_category where date_key between 20261001 and 20261007) as diff;
```
Should be 0; run as a test after every refresh.

## Gotchas
- Distinct counts summed across days double-count; use sketches or recompute.
- Dimension attribute changes (SCD2) affect which bucket history falls in; define whether aggregates use current or historical attributes.

## Verify
Reconciliation test returns 0 difference; dashboard queries hit the aggregate (check query history).
