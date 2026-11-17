---
id: computing-software.data-engineering.data-modelling.additive-semi-additive-and-non-additive-facts
name: additive-semi-additive-and-non-additive-facts
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, dimensional-modelling, semi-additive-facts, additive-facts, non-additive-facts, balances, ratios, periodic-snapshot]
level: practitioner
status: gated
description: "Classify facts as additive, semi-additive or non-additive and model them so BI sums correctly: balances over time, ratios stored as components, distinct counts."
sources:
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/additive-semi-additive-non-additive-fact/
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/periodic-snapshot-fact-table/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Additive, semi-additive and non-additive facts

**Goal:** every measure in a fact table can be aggregated correctly by any dimension a user picks, or is protected so it cannot be summed wrongly.

## Classes
| Class | Can SUM across | Examples |
|---|---|---|
| Additive | all dimensions | sales amount, quantity, cost, clicks |
| Semi-additive | some dimensions, not time | account balance, inventory on hand, headcount, open tickets |
| Non-additive | none | unit price, percentages, ratios, temperatures, distinct counts |

## Semi-additive: balances
Store in a **periodic snapshot** fact (one row per account per day/month). Summing balances across accounts on one date is valid; summing across dates is not.
Correct aggregations over time:
```sql
-- end-of-period balance per month (max_by is DuckDB/Spark/Snowflake spelling; ran on DuckDB 1.5)
select account_id, date_trunc('month', snapshot_date) m,
       max_by(balance, snapshot_date) as closing_balance       -- last value in period
from fct_account_daily group by 1, 2;

-- average daily balance
select account_id, date_trunc('month', snapshot_date) m, avg(balance) avg_balance
from fct_account_daily group by 1, 2;
```
dbt MetricFlow's `non_additive_dimension` with `window_choice: max|min` is documented on the dbt measures page. In the semantic layer, define the measure with a non-sum time aggregation (e.g. dbt MetricFlow `non_additive_dimension: {name: snapshot_date, window_choice: max}`, Power BI `LASTNONBLANK` (gated: unconfirmed, source is paywalled or blocked), LookML `type: sum` with a filter on last day, or `period_to_date` logic).

Alternative: store **transactions** (additive deltas) and compute balances as running sums; good for audit, heavy for queries over long histories.

## Non-additive: ratios and prices
Never store the ratio alone. Store additive components and compute the ratio after aggregation:
```sql
-- fact: revenue, cost (additive)   -> margin_pct = sum(revenue - cost) / sum(revenue)   (computed: weighted 0.138 vs 0.367 for the average of row percentages on a skewed sample)
select region, sum(revenue - cost) / nullif(sum(revenue), 0) as margin_pct from fct_sales group by 1;
```
Averaging stored percentages gives an unweighted mean, which is wrong whenever groups differ in size.
Unit price: store extended amount (qty x price) as the fact; derive average price = sum(amount)/sum(qty).

## Distinct counts
Distinct customers is non-additive (sum of daily distinct != monthly distinct). Options: compute from the transaction grain at query time, pre-aggregate per required grain, or store mergeable sketches (HyperLogLog: `hll_sketch` columns combined with `hll_union`) for approximate additive behaviour.

## Document it
Mark measure additivity in the data dictionary / semantic model (e.g. `agg: sum` vs `agg: average`/`max` with non-additive dimension) so BI tools default correctly.

## Verify
- [ ] Monthly balance report equals the balance on the last day, not the sum of days.
- [ ] Ratio measures computed from components; no stored percentage is summed or averaged in BI.
