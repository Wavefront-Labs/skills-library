---
id: computing-software.data-engineering.data-modelling.dimensional-modelling-and-scd
name: dimensional-modelling-and-scd
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, data-modeling, dimensional-modelling, kimball, star-schema, snowflake-schema, fact-table, dimension-table, grain, surrogate-keys, conformed-dimensions, slowly-changing-dimensions, scd-type-1, scd-type-2, scd-type-3, valid-from, valid-to, is-current, dbt-snapshots, one-big-table, obt, bus-matrix, data-warehouse]
level: practitioner
status: verified
description: "Design star schemas the Kimball way: declare grain, choose fact types, build conformed dimensions with surrogate keys, and implement SCD types 1, 2 and 3 with valid_from/valid_to."
sources:
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/
  - https://docs.getdbt.com/docs/build/snapshots
  - https://en.wikipedia.org/wiki/Slowly_changing_dimension
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dimensional modelling and SCDs — star schemas people can query correctly

**Goal:** a model where analysts get the right number without knowing the joins' hidden traps, and history is preserved exactly as the business needs.

## 1. Kimball's four steps, in order
1. **Pick the business process** (orders placed, shipments, payments) — not a department or a report.
2. **Declare the grain** in one sentence: "one row per order line per order", "one row per account per day". Write it in the model's docs. Every later decision is checked against it.
3. **Identify dimensions** — the who/what/where/when that describe a row at that grain (customer, product, store, date).
4. **Identify facts** — numeric measurements true at that grain (quantity, net_amount).
**Gotcha:** mixing grains in one fact (order header shipping cost on every line) double-counts when summed. Either allocate it to lines or keep a separate header-grain fact.

## 2. Fact table types
- **Transaction:** one row per event; most flexible; fully additive measures.
- **Periodic snapshot:** one row per entity per period (daily account balance). Balances are **semi-additive**: sum across accounts, never across days (use end-of-period or average).
- **Accumulating snapshot:** one row per process instance with milestone dates updated in place (order → shipped → delivered), good for lag metrics.
- **Factless:** events with no measure (attendance, eligibility); count rows.
Store ratios and percentages as their additive components (numerator, denominator), not as precomputed ratios.

## 3. Dimensions and keys
- Give each dimension a **surrogate key** (integer sequence or a deterministic hash, e.g. `dbt_utils.generate_surrogate_key` (a dbt_utils package macro, not dbt core; ran with dbt_utils 1.4.1) over natural key + valid_from). Keep the natural/business key as an attribute.
- Facts reference the surrogate key of the dimension version valid at event time.
- Add an explicit "unknown" member (key `-1` or a hash of `'unknown'`) so facts with missing references still join under inner joins.
- **Conformed dimensions:** one shared `dim_customer`, `dim_date`, `dim_product` used by every fact, with identical keys and attribute names. A bus matrix (processes × dimensions) shows which are shared. Without conformance, "customers" differs between finance and marketing dashboards.
- Prefer a flat (denormalized) dimension over snowflaking unless a sub-dimension is huge or shared.

## 4. Slowly changing dimensions
- **Type 1 — overwrite.** History lost; use for corrections and attributes nobody reports historically (typo in name).
- **Type 2 — new row per change.** Columns: `valid_from`, `valid_to`, `is_current`, plus the surrogate key per version.
- **Type 3 — previous-value column** (`region`, `previous_region`). Only one level of history; for planned re-orgs where "before vs after" is the question.
Mix per attribute: Type 2 on `segment`, Type 1 on `email`.

Type 2 conventions:
```sql
-- current row: valid_to = '9999-12-31' (or NULL), is_current = true
select f.net_amount, d.segment
from fct_orders f
join dim_customer d
  on f.customer_id = d.customer_id
 and f.order_ts >= d.valid_from and f.order_ts < d.valid_to;  -- half-open interval
```
- Use **half-open** intervals `[valid_from, valid_to)` so a timestamp matches exactly one version. Using `BETWEEN` creates double matches on boundaries.
- Prefer a far-future sentinel over NULL `valid_to` so range joins don't need `coalesce`.
- In dbt, `snapshot` with `strategy='timestamp'` (on `updated_at`) or `'check'` (on listed columns) produces `dbt_valid_from`/`dbt_valid_to`; newer versions can set a `dbt_valid_to_current` sentinel (tested on dbt 1.12.6: a YAML snapshot with `dbt_valid_to_current: "cast('9999-12-31' as timestamp)"` closed the old row at the new `updated_at` and left the current row at 9999-12-31). Snapshots only capture changes that exist when they run — changes between runs are invisible, so snapshot raw sources frequently.
- **Gotcha:** if attributes flap (a field toggling every load due to whitespace or case), Type 2 explodes in row count. Normalize before hashing/comparing.

## 5. One Big Table (OBT) trade-offs
Wide, pre-joined tables are fast for BI tools and columnar engines and easy for casual users. Costs: duplicated dimension attributes, painful Type 2 restatements (rebuild everything), and one table per grain anyway. Practical compromise: keep the star schema as the source of truth and publish OBTs as thin marts on top. See computing-software.data-engineering.data-warehouse-architecture.medallion-layering.

## Verify
- [ ] Each fact has a written one-sentence grain and a uniqueness test on the grain's columns.
- [ ] `sum(measure)` in the fact equals the source system total for a sample day.
- [ ] No fact row joins to zero or to two rows of a Type 2 dimension (test both counts).
- [ ] Each Type 2 natural key has exactly one `is_current = true` row and non-overlapping intervals.
- [ ] Shared dimensions are referenced by the same table in every mart.
