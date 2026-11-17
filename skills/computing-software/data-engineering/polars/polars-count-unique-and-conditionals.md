---
id: computing-software.data-engineering.polars.polars-count-unique-and-conditionals
name: polars-count-unique-and-conditionals
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-conditionals, n-unique, approx-n-unique, value-counts, unique-counts, when-then-otherwise, hyperloglog]
level: practitioner
status: docs-checked
description: "Count distinct values in Polars with n_unique, approx_n_unique, value_counts and unique_counts, and write if/elif logic with when, then and otherwise."
sources:
  - https://docs.pola.rs/user-guide/expressions/basic-operations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Count unique values and write conditionals

Goal: summarise distinct values cheaply and replace values by condition.

## Counting unique values

- `n_unique()`: exact number of unique values; can be quite slow on very large data.
- `approx_n_unique()`: estimate using the HyperLogLog++ algorithm; use when an approximation is good enough. The page's example (100,000 random integers below 100,000) shows an estimate wrong by 0.9%.

```python
long_df.select(
    pl.col("numbers").n_unique().alias("n_unique"),
    pl.col("numbers").approx_n_unique().alias("approx_n_unique"),
)
```

- `value_counts()`: unique values with their counts; returns the results in structs.

```python
df.select(pl.col("names").value_counts().alias("value_counts"))
```

- `unique()` and `unique_counts()`: separate series of the values and of the counts.

```python
df.select(
    pl.col("names").unique(maintain_order=True).alias("unique"),
    pl.col("names").unique_counts().alias("unique_counts"),
)
```

Gotcha: pass `maintain_order=True` to `unique` so its order is consistent with the order of `unique_counts`.

## Conditionals with when/then/otherwise

`pl.when(predicate).then(expr).otherwise(expr)` is akin to a ternary operator. Values where the predicate is `True` take the `then` expression; `False` values take `otherwise`, or `null` if `otherwise` is omitted.

One Collatz step on column `nrs`:

```python
pl.when(pl.col("nrs") % 2 == 1)      # is the number odd?
  .then(3 * pl.col("nrs") + 1)       # multiply by 3 and add 1
  .otherwise(pl.col("nrs") // 2)     # otherwise halve it
  .alias("Collatz")
```

Chain further `.when(...).then(...)` blocks to emulate `elif`. For each value, a deeper replacement expression is only considered if all previous predicates failed for that value.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
