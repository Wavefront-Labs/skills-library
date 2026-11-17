---
id: computing-software.data-engineering.polars.polars-rename-and-generate-expressions
name: polars-rename-and-generate-expressions
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-expression-expansion, column-renaming, alias, name-prefix, name-suffix, name-map, duplicate-error, generate-expressions]
level: practitioner
status: docs-checked
description: "Rename expanded Polars columns with alias and the name namespace, fix DuplicateError, and build expression lists programmatically instead of looping with_columns."
sources:
  - https://docs.pola.rs/user-guide/expressions/expression-expansion/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rename expanded columns and generate expressions programmatically

Goal: keep result column names correct and give Polars all expressions in one context call.

## Default naming and DuplicateError

An expression keeps the name of the original column. Two results both named `price` raise `DuplicateError`:

```python
df.select(pl.col("price") / gbp_usd_rate, pl.col("price") / eur_usd_rate)  # DuplicateError
```

## alias for one column

```python
df.select(
    (pl.col("price") / gbp_usd_rate).alias("price (GBP)"),
    (pl.col("price") / eur_usd_rate).alias("price (EUR)"),
)
```

`alias` renames a single column, so you cannot use it with expression expansion.

## prefix and suffix

For a static prefix or suffix use the `name` namespace:

```python
df.select(
    (pl.col("^year_.*$") / eur_usd_rate).name.prefix("in_eur_"),
    (pl.col("day_high", "day_low") / gbp_usd_rate).name.suffix("_gbp"),
)
```

## Dynamic names

`name.map` takes a callable from old name to new name:

```python
df.select(pl.all().name.map(str.upper))
```

The page notes `.name.to_uppercase` also exists, so this example is only illustrative. See the API reference for the full `name` namespace.

## Generate expressions, do not loop

Expansion cannot compute things like day and year amplitude (high minus low per period). Do not do this:

```python
result = df
for tp in ["day", "year"]:
    result = result.with_columns(
        (pl.col(f"{tp}_high") - pl.col(f"{tp}_low")).alias(f"{tp}_amplitude"))
```

Instead generate the expressions and use them once in a context:

```python
def amplitude_expressions(time_periods):
    for tp in time_periods:
        yield (pl.col(f"{tp}_high") - pl.col(f"{tp}_low")).alias(f"{tp}_amplitude")

result = df.with_columns(amplitude_expressions(["day", "year"]))
```

The result is the same, and specifying everything in one go lets Polars optimise the query better and parallelise the computations.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/expressions/expression-expansion/. No claims needed correcting. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
