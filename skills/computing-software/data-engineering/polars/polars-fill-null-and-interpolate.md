---
id: computing-software.data-engineering.polars.polars-fill-null-and-interpolate
name: polars-fill-null-and-interpolate
category: computing-software
field: data-engineering
product: polars
tags: [polars-fill-null, fill-null, interpolate, forward-fill, backward-fill, missing-data, expressions]
level: practitioner
status: docs-checked
description: "Fill null values in Polars with a literal, another expression, a forward or backward strategy, or interpolation."
sources:
  - https://docs.pola.rs/user-guide/expressions/missing-data/
  - https://docs.pola.rs/user-guide/transformations/time-series/resampling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replace `null` values in a column using the right fill method.

Given:

```python
df = pl.DataFrame({"col1": [0.5, 1, 1.5, 2, 2.5], "col2": [1, None, 3, None, 5]})
```

**Literal** (replaces every `null`):

```python
df.with_columns(pl.col("col2").fill_null(3))
```

**Expression** (values taken from the matching rows of any expression):

```python
df.with_columns(pl.col("col2").fill_null((2 * pl.col("col1")).cast(pl.Int64)))
```

The literal case is a special case of the expression case.

**Strategy based on neighbouring values.** `strategy="forward"` and `strategy="backward"` take the first non-null value immediately before or after. Other strategies are listed in the API docs:

```python
df.with_columns(
    pl.col("col2").fill_null(strategy="forward").alias("forward"),
    pl.col("col2").fill_null(strategy="backward").alias("backward"),
)
```

**Interpolation.** Use `interpolate()` instead of `fill_null`:

```python
df.with_columns(pl.col("col2").interpolate())
```

With `interpolate`, nulls at the beginning and end of the series remain null.

**After upsampling.** `DataFrame.upsample` adds rows with nulls where there is no data; fill them with a strategy or interpolation:

```python
df.upsample(time_column="time", every="15m").fill_null(strategy="forward")
df.upsample(time_column="time", every="15m").interpolate().fill_null(strategy="forward")
```

(The second form interpolates linearly, then forward-fills what is left.)

NaN is not filled by `fill_null`; use `fill_nan` for that.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/expressions/missing-data/; https://docs.pola.rs/user-guide/transformations/time-series/resampling/. No claims needed correcting. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
