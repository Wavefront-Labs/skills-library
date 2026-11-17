---
id: computing-software.data-engineering.data-modelling.junk-mini-and-role-playing-dimensions
name: junk-mini-and-role-playing-dimensions
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, dimensional-modelling, junk-dimension, mini-dimension, role-playing-dimension, outrigger, rapidly-changing-attributes, kimball, star-schema]
level: practitioner
status: gated
description: "Apply Kimball's specialised dimensions: junk dimensions for flags, mini-dimensions for rapidly changing attributes, and role-playing dimensions for one entity in several roles."
sources:
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/junk-dimension/
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/role-playing-dimension/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Junk, mini and role-playing dimensions

**Goal:** keep fact tables narrow and dimensions manageable when you have many low-cardinality flags, fast-changing customer attributes, or the same dimension used several times by one fact.

## 1. Junk dimension (flags and indicators)
Problem: a fact has 6 flags/codes (`is_gift`, `payment_type`, `channel`, `is_promo`, ...). Six tiny dimensions clutter the model; putting them in the fact widens it and BI users see cryptic Y/N columns.
Solution: one dimension with one row per **combination that occurs**:
```sql
CREATE TABLE dim_order_profile AS
SELECT ROW_NUMBER() OVER (ORDER BY is_gift, payment_type, channel, is_promo) AS order_profile_key,
       is_gift, payment_type, channel, is_promo,
       CASE WHEN is_gift THEN 'Gift' ELSE 'Not gift' END AS gift_label   -- readable labels
FROM (SELECT DISTINCT is_gift, payment_type, channel, is_promo FROM stg_orders);
```
- Either pre-generate the full Cartesian product (if small: 2×4×3×2 = 48 rows) or add new combinations incrementally. Hash key alternative: `md5(concat_ws('|', ...))` avoids a lookup.
- Don't junk high-cardinality or unrelated-to-analysis attributes (free text → degenerate dimension or nowhere).

(Junk-dimension SQL run on DuckDB 1.5: 3 staged rows with 2 distinct combinations gave 2 dimension rows with keys 1 and 2; the full product 2x4x3x2 is 48; the `md5(concat_ws('|', ...))` hash key drops NULL parts, so coalesce first.) The role-playing view also ran.
## 2. Mini-dimension (rapidly changing attributes)
Problem: customer `age_band`, `income_band`, `credit_score_band`, `loyalty_tier` change monthly; SCD2 on a 50M-row customer dimension explodes it.
Solution: move those attributes into a separate small dimension of **banded** values, keyed independently:
```
dim_customer_demographics (demographics_key, age_band, income_band, score_band, loyalty_tier)   -- a few thousand rows
fact_sales (..., customer_key, demographics_key, ...)    -- profile at time of the sale
```
- The fact captures the profile in effect at transaction time; history is preserved without versioning the big dimension.
- Optionally keep `current_demographics_key` on `dim_customer` (type 1 outrigger) for "current profile" analysis.
- Band the values (e.g. ages 25-34) so cardinality stays small; exact values belong elsewhere.

## 3. Role-playing dimension
One physical dimension referenced by multiple foreign keys in the same fact: `order_date_key`, `ship_date_key`, `delivery_date_key` → `dim_date`; `origin_airport_key`, `destination_airport_key` → `dim_airport`.
Expose each role with distinct names so BI tools don't confuse them:
```sql
CREATE VIEW dim_ship_date AS
SELECT date_key AS ship_date_key, full_date AS ship_date, month_name AS ship_month, fiscal_quarter AS ship_fiscal_quarter
FROM dim_date;
```
- In Power BI, create inactive relationships + `USERELATIONSHIP` or separate role tables; in LookML, join the same view twice with different aliases (gated: unconfirmed, source is paywalled or blocked).
- Column prefixes per role prevent "which date is this month?" ambiguity in reports.

## 4. Choosing quickly
| Situation | Pattern |
|---|---|
| Many low-cardinality flags on a fact | junk dimension |
| Dimension attributes that change often, big dimension | mini-dimension |
| Same entity in several roles on one fact | role-playing views |
| Transaction ID / invoice number with no attributes | degenerate dimension (stays in the fact) |

## Verify
- [ ] Junk dimension row count equals distinct combinations (no duplicates per combination).
- [ ] Customer dimension size stays stable while demographics change.
- [ ] Each role-playing view has uniquely named columns.
