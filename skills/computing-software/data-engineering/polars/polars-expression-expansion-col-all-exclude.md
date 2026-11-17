---
id: computing-software.data-engineering.polars.polars-expression-expansion-col-all-exclude
name: polars-expression-expansion-col-all-exclude
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-expression-expansion, col, regex-columns, dtype-expansion, all, exclude, with-columns]
level: practitioner
status: docs-checked
description: "Apply one Polars expression to many columns by name, dtype or regex using col, all and exclude, and avoid the mixed-argument TypeError."
sources:
  - https://docs.pola.rs/user-guide/expressions/expression-expansion/
  - https://docs.pola.rs/user-guide/concepts/expressions-and-contexts/
  - https://docs.pola.rs/user-guide/concepts/lazy-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expression expansion with col, all and exclude

Goal: write one expression that expands to many, instead of repeating it per column.

## By name

```python
eur_usd_rate = 1.09
result = df.with_columns(
    (pl.col("price", "day_high", "day_low", "year_high", "year_low") / eur_usd_rate).round(2)
)
```

This expands to five independent expressions, equivalent to a list `[(pl.col("price") / eur_usd_rate).round(2), ...]` passed to `with_columns` (the page confirms with `result.equals(result2)`).

## By dtype

```python
df.with_columns((pl.col(pl.Float64) / eur_usd_rate).round(2))
df.with_columns((pl.col(pl.Float32, pl.Float64) / eur_usd_rate).round(2))
```

Passing dtypes expands to every column matching one of them. You cannot know beforehand how many columns it expands to; you need the schema of the input dataframe.

## By regex

Regular expressions start with `^` and end with `$` (this distinguishes them from plain names) and must match the whole column name. They mix with plain names:

```python
df.select(pl.col("ticker", "^.*_high$", "^.*_low$"))
```

## No mixed argument types (Python)

`col` takes any number of strings (names or regexes) or any number of dtypes, never both:

```python
try:
    df.select(pl.col("ticker", pl.Float64))
except TypeError as err:
    print("TypeError:", err)
```

## All and exclude

- `pl.all()` selects all columns; it is sugar for `col("*")`, and `all` is preferred because it reads like English.
- `exclude` takes the same argument types as `col`, and works after `all` or `col`:

```python
df.select(pl.all().exclude("^day_.*$"))
df.select(pl.col(pl.Float64).exclude("^day_.*$"))
```

## Previewing

Build a `pl.LazyFrame(schema=schema)`, apply the expression and call `explain()` to see how it expands against that schema. An expression such as `(pl.col(pl.Float64) * 1.1).name.suffix("*1.1")` expands to 0 columns when no column is `Float64`.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/expressions/expression-expansion/; https://docs.pola.rs/user-guide/concepts/expressions-and-contexts/; https://docs.pola.rs/user-guide/concepts/lazy-api/. Corrected: Reworded the Previewing sentence to match the lazy-api page and added that page to sources. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
