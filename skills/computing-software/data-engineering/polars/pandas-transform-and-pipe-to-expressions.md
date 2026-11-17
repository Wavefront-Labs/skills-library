---
id: computing-software.data-engineering.polars.pandas-transform-and-pipe-to-expressions
name: pandas-transform-and-pipe-to-expressions
category: computing-software
field: data-engineering
product: polars
tags: [polars-migration-pandas, window-functions, over, transform, pipe, expression-functions, with-columns, missing-data]
level: practitioner
status: docs-checked
description: "Replace pandas groupby transform with over() window expressions and replace chained pipe functions with functions returning expressions so Polars runs them in parallel."
sources:
  - https://docs.pola.rs/user-guide/migration/pandas/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# groupby-transform and pipe in Polars

## transform becomes a window expression
pandas:
```python
df["size"] = df.groupby("c")["type"].transform(len)
```
Polars:
```python
df.with_columns(
    pl.col("type").count().over("c").alias("size")
)
```
For `c=[1,1,1,2,2,2,2]` this yields size 3,3,3,4,4,4,4 (dtype `u32`). Several window expressions with different groups can sit in one `with_columns`:
```python
df.with_columns(
    pl.col("c").count().over("c").alias("size"),
    pl.col("c").sum().over("type").alias("sum"),
    pl.col("type").reverse().over("c").alias("reverse_type")
)
```
Polars caches window expressions applied over the same group, so putting them in a single `with_columns` is convenient and optimal.

## Avoid "pipe littering"
Copying the pandas style `df.pipe(add_foo).pipe(add_bar).pipe(add_ham)` creates three `with_columns` contexts, so Polars runs them sequentially with zero parallelism.

Instead write functions that return expressions and use one context:
```python
def get_foo(input_column: str) -> pl.Expr:
    return pl.col(input_column).some_computation().alias("foo")

df.with_columns(
    get_ham("col_a"),
    get_bar("col_b"),
    get_foo("col_c"),
)
```
All three expressions run in parallel. These functions are composable: expressions can be chained and partially applied.

## When the schema is needed
Use a single `pipe` to get hold of the LazyFrame schema, then pass `lf.schema` to the expression builders:
```python
lf.pipe(lambda lf: lf.with_columns(
    get_ham("col_a"),
    get_bar("col_b", lf.schema),
    get_foo("col_c", lf.schema),
))
```
(`get_bar`/`get_foo` take `schema: OrderedDict` and branch on e.g. `"some_col" in schema`.)

## Missing data note
In pandas an integer column with missing values becomes float with `NaN` (unless nullable dtypes are used). In Polars it stays integer with `null`; float `NaN` is a distinct special value.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
