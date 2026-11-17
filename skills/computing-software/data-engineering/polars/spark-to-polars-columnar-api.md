---
id: computing-software.data-engineering.polars.spark-to-polars-columnar-api
name: spark-to-polars-columnar-api
category: computing-software
field: data-engineering
product: polars
tags: [polars-migration-spark, pyspark, column-based, window-functions, over, rolling-mean, shift, expressions]
level: practitioner
status: docs-checked
description: "Port PySpark row-based logic to Polars column-based expressions: independent head/sum columns and composable shift plus rolling_mean over a window."
sources:
  - https://docs.pola.rs/user-guide/migration/spark/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Coming from Apache Spark

Key idea: a Spark `DataFrame` is a collection of rows; a Polars `DataFrame` is closer to a collection of columns. Columns can be combined in ways Spark does not allow because Spark preserves the relationship of the data in each row.

Sample data: `df = pl.DataFrame({"foo": ["a","b","c","d","d"], "bar": [1,2,3,4,5]})`.

## Independent column expressions
```python
df.select(
    pl.col("foo").sort().head(2),
    pl.col("bar").filter(pl.col("foo") == "d").sum()
)
```
Result is two rows, `foo` = a, b and `bar` = 9, 9. The two expressions are independent; the scalar sum is repeated for each value of the other expression. In Spark you must compute the sum separately (`groupBy().agg(sum(...)).take(1)[0][0]`) and add it with `withColumn("bar", lit(bar_sum))`.

## Two heads combined
```python
df.select(
    pl.col("foo").sort().head(2),
    pl.col("bar").sort(descending=True).head(2),
)
```
Gives (a, 5) and (b, 4); the pairing results purely from juxtaposing two output columns, provided both return the same number of values. Spark needs an artificial key: `row_number().over(Window.orderBy(...))` on each side, then a join on `rownum`.

## Expression composability
Rolling mean of a lagged variable in one expression:
```python
df.with_columns(
    feature=pl.col('price').shift(7).rolling_mean(7).over('store', order_by='date')
)
```
PySpark allows `F.mean(F.abs("price")).over(window)` because `abs` is elementwise, but not `F.mean(F.lag("price", 7)).over(window)` because `lag` is a window function. The PySpark equivalent needs `F.lag` and `F.mean` each over its own window (`Window().partitionBy("store").orderBy("date")` with `rowsBetween(-6, 0)`), and `F.when(F.count("lagged_price").over(rolling_window) >= 7, F.mean(...))`.

## Takeaway
Per the page, Polars composes expressions liberally in a single expression, where PySpark needs separate windows or helper columns.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/migration/spark/. Corrected: Reworded the takeaway as the page's claim rather than a general statement. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
