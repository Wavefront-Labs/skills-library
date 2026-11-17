---
id: computing-software.data-engineering.polars.polars-null-versus-nan-missing-data
name: polars-null-versus-nan-missing-data
category: computing-software
field: data-engineering
product: polars
tags: [polars-missing-data, null-values, nan, null-count, is-null, fill-nan, validity-bitmap]
level: practitioner
status: docs-checked
description: "Understand how Polars represents missing data as null versus NaN, count and detect nulls cheaply, and neutralise NaN in aggregations."
sources:
  - https://docs.pola.rs/user-guide/expressions/missing-data/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: handle missing values correctly and avoid confusing `null` with `NaN`.

**Missing data is always `null`**, for every dtype including numeric. (In pandas the marker depends on the dtype.) `NaN` is a valid floating point value and is not missing data.

```python
df = pl.DataFrame({"value": [1, None]})
```

**Cheap metadata.** Polars keeps a validity bitmap per series (n / 8 bytes for length n), so these are cheap because the result is already known:

- `null_count()` on a DataFrame, a column, or a Series: `df.null_count()`
- `is_null()` on a column or Series: `df.select(pl.col("value").is_null())`

**NaN.** Create it directly (`np.nan`, `float("nan")`) or by computation, e.g. `pl.col("dividend") / pl.col("divisor")` with `0 / 0`. In pandas a NaN in an integer column casts the column to float; in Polars an exception is raised instead.

NaN is not counted by `null_count`, and is filled by `fill_nan` but not by `fill_null`. `is_nan` and `fill_nan` work like `is_null` and `fill_null`, but Polars holds no metadata about NaN, so `is_nan` entails actual computation.

**Aggregations.** Numerical aggregations such as `mean` and `sum` skip `null` but consider `NaN`, which typically propagates into the result. To avoid that, replace NaN with `null`:

```python
mean_nan_df = nan_df.with_columns(
    pl.col("value").fill_nan(None).alias("replaced"),
).select(
    pl.all().mean().name.suffix("_mean"),
    pl.all().sum().name.suffix("_sum"),
)
```

More on NaN: the floating point numbers section of the data types concept page.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/expressions/missing-data/. No claims needed correcting. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
