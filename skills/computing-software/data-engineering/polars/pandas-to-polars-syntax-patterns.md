---
id: computing-software.data-engineering.polars.pandas-to-polars-syntax-patterns
name: pandas-to-polars-syntax-patterns
category: computing-software
field: data-engineering
product: polars
tags: [polars-migration-pandas, select, filter, with-columns, when-then-otherwise, lazy-scan, assign, query]
level: practitioner
status: docs-checked
description: "Rewrite common pandas selection, filtering, assign, mask and lazy-read idioms into idiomatic parallel Polars expressions."
sources:
  - https://docs.pola.rs/user-guide/migration/pandas/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rewrite pandas idioms as Polars expressions

Goal: translate typical pandas code so Polars can parallelise and optimise it.

## Selecting
pandas `df["a"]` / `df.loc[:,"a"]` becomes `df.select("a")`. Row selection by value becomes
`df.filter(pl.col("a") < 10)`. `select` and `filter` run operations in parallel and the optimizer sees all selection criteria.

## Be lazy
pandas:
```python
df = pd.read_csv(csv_file, usecols=["id1","v1"])
grouped_df = df.loc[:,["id1","v1"]].groupby("id1").sum()
```
Polars lazy:
```python
df = pl.scan_csv(csv_file)
grouped_df = df.group_by("id1").agg(pl.col("v1").sum()).collect()
```
The optimizer finds only `id1` and `v1` are needed and reads just those columns. For eager, replace `scan_csv` with `read_csv`. Lazy mode is entered through an implicitly lazy function like `scan_csv` or explicitly via `.lazy()`.

## Column assignment
pandas `df.assign(tenXValue=lambda df_: df_.value * 10, ...)` runs sequentially. Polars:
```python
df.with_columns(
    tenXValue=pl.col("value") * 10,
    hundredXValue=pl.col("value") * 100,
)
```
These assignments run in parallel.

## Assignment based on a predicate
pandas `df_["a"].mask(df_["c"] == 2, df_["b"])` becomes:
```python
df.with_columns(
    pl.when(pl.col("c") == 2)
    .then(pl.col("b"))
    .otherwise(pl.col("a")).alias("a")
)
```
Every branch of the when/then/otherwise can be computed in parallel, valuable when branches are expensive.

## Filtering
pandas `df.query("m2_living > 2500 and price < 300000")` or a boolean mask becomes:
```python
df.filter((pl.col("m2_living") > 2500) & (pl.col("price") < 300000))
```
The optimizer merges multiple separately written filters into one in the optimized plan.

Related: pandas-transform-and-pipe-to-expressions, pandas-to-polars-concepts.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
