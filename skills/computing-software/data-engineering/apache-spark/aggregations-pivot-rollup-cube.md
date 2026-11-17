---
id: computing-software.data-engineering.apache-spark.aggregations-pivot-rollup-cube
name: aggregations-pivot-rollup-cube
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, pyspark, dataframe-api, spark-aggregations, pivot-rollup-cube, groupby, agg, pivot, rollup, cube, grouping-sets, approx-count-distinct, spark-sql]
level: practitioner
status: docs-checked
description: "Aggregate Spark DataFrames correctly and fast: groupBy/agg, count distinct vs approx, pivot with explicit values, rollup/cube/GROUPING SETS and the grouping() id."
sources:
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.GroupedData.html
  - https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-groupby.html
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Aggregations: groupBy, pivot, rollup, cube

**Goal:** produce correct grouped metrics, including subtotals and cross-tabs, without blowing up shuffles.

## groupBy / agg
```python
from pyspark.sql import functions as F
daily = (orders.groupBy("order_date", "country")
         .agg(F.count("*").alias("orders"),
              F.countDistinct("customer_id").alias("customers"),
              F.sum("amount").alias("revenue"),
              F.max_by("sku", "amount").alias("top_sku")))
```
- `count("col")` ignores nulls; `count("*")` / `count(F.lit(1))` counts rows.
- `sum` of an all-null group is null, not 0: wrap with `F.coalesce(F.sum(...), F.lit(0))` if consumers expect 0.
- Spark does partial (map-side) aggregation before the shuffle for algebraic aggregates (sum/count/min/max), so groupBy is far cheaper than it looks. `collect_list`/`collect_set` cannot shrink and can OOM on hot keys.

## Distinct counts at scale
Exact `countDistinct` on several columns causes expansion (Expand node, one row per distinct aggregate). For dashboards use `F.approx_count_distinct("customer_id", rsd=0.01)`, or HLL sketch functions (`hll_sketch_agg`, `hll_union_agg`) to store re-aggregatable sketches.

## Pivot
```python
wide = (sales.groupBy("store")
        .pivot("month", ["2026-01", "2026-02", "2026-03"])   # ALWAYS pass values
        .agg(F.sum("amount")))
```
Without the values list Spark runs an extra job to collect distinct values and caps at `spark.sql.pivotMaxValues` (10,000). Unpivot with `df.unpivot(ids, values, "month", "amount")` or `stack()` in SQL.

## Subtotals: rollup, cube, grouping sets
```python
r = (sales.rollup("region", "country")
     .agg(F.sum("amount").alias("amt"), F.grouping_id().alias("gid")))
```
- `rollup(a, b)` -> (a,b), (a), () : hierarchical subtotals.
- `cube(a, b)` -> all 2^n combinations.
- SQL `GROUP BY GROUPING SETS ((region, country), (channel), ())` for arbitrary sets.
- Subtotal rows have null in rolled-up columns; distinguish them from real nulls with `grouping("country")` (1 = aggregated) or `grouping_id()`. Never filter subtotals with `isNull()`.

## Gotchas
- Grouping by a high-cardinality skewed key (null, "unknown") -> one huge task; filter or salt (see shuffle-and-skew-tuning).
- Floating-point `sum` is not deterministic across runs (partition order); use `DECIMAL` for money.
- `groupBy().agg()` output column names like `sum(amount)` break downstream SQL; always alias.

## Verify
- [ ] Grand-total row from rollup equals a separate `agg(F.sum(...))` over the whole input.
- [ ] Pivot call lists explicit values (no extra distinct job in the UI).
- [ ] Subtotal rows identified via `grouping_id`, not null checks.

## Checked

2026-10-28. Confirmed: max_by, hll_sketch_agg, hll_union_agg in the PySpark functions list; unpivot on the Dataset page; spark.sql.pivotMaxValues 10000 on the configuration page. Removed: three version gates and an algorithm name not on the pages.

Method: documentation only; no commands were run.
