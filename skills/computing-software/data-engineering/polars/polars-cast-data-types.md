---
id: computing-software.data-engineering.polars.polars-cast-data-types
name: polars-cast-data-types
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-casting, cast, strict, downcast, overflow, string-to-number, boolean, datetime-format]
level: practitioner
status: docs-checked
description: "Cast Polars columns with cast and strict, downcast numerics safely, convert strings, booleans and temporal types, and format or parse dates."
sources:
  - https://docs.pola.rs/user-guide/expressions/casting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Casting columns in Polars

Goal: change dtype with `cast`, and control what happens to values that do not convert.

## strict

`expr.cast(dtype, strict=True)`. With the default `strict=True` an unconvertible value raises an error naming the values that failed (`InvalidOperationError`). With `strict=False` those values quietly become `null`.

## Numeric

```python
df.select(
    pl.col("integers").cast(pl.Float32).alias("integers_as_floats"),
    pl.col("floats").cast(pl.Int32).alias("floats_as_integers"),
)
```

Floats are truncated when cast to an integer type.

Downcast to cut memory (`df.estimated_size()` shows the effect):

```python
df.with_columns(pl.col("integers").cast(pl.Int16), pl.col("floats").cast(pl.Float32))
```

The target must hold the column's largest and smallest values: `Int32` covers -2147483648 to 2147483647 and an 8-bit signed integer only -128 to 127. Casting `10000002` to `Int8` raises an error; with `strict=False` the overflowing values become `null`:

```python
df.select(pl.col("big_integers").cast(pl.Int8, strict=False))
```

## Strings

```python
df.select(
    pl.col("integers_as_strings").cast(pl.Int32),
    pl.col("floats_as_strings").cast(pl.Float64),
    pl.col("floats").cast(pl.String),
)
```

A non-numerical or badly formatted string (the example uses `"- 6 . 3"`) raises an error with details; `strict=False` gives `null` instead.

## Booleans

Numbers cast to `Boolean`: 0 becomes `False`, everything else `True` (the example includes -1, which is `True`). Booleans cast to numbers as 1 and 0 (example: `cast(pl.Int8)`).

## Temporal

Temporal types are stored as units since the epoch: `Date` as days, `Datetime` in microseconds, `Time` in nanoseconds. Casting to `Int64` exposes this:

```python
pl.col("date").cast(pl.Int64).alias("days_since_epoch")
pl.col("datetime").cast(pl.Int64).alias("us_since_epoch")
pl.col("time").cast(pl.Int64).alias("ns_since_midnight")
```

Format and parse with chrono format syntax:

```python
pl.col("date").dt.to_string("%Y-%m-%d")
pl.col("string").str.to_datetime("%Y-%m-%d")
```

`str.to_datetime` has extra options for timezones; see the API reference.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
