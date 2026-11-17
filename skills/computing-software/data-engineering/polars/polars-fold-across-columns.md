---
id: computing-software.data-engineering.polars.polars-fold-across-columns
name: polars-fold-across-columns
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-folds, fold, horizontal, accumulator, sum-horizontal, concat-str, all-columns-predicate]
level: practitioner
status: docs-checked
description: "Compute custom row-wise reductions across Polars columns with pl.fold, pick the right initial accumulator, apply a predicate to all columns, and use concat_str for strings."
sources:
  - https://docs.pola.rs/user-guide/expressions/folds/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Folds across columns

Goal: compute a custom horizontal (across-column) reduction when `sum_horizontal`, `mean_horizontal` or `min_horizontal` do not fit. Those are special cases of a general fold.

Folds with `pl.fold` operate on full columns for maximum speed, using the data layout efficiently and often with vectorized execution.

## Signature in use

`pl.fold(acc=..., function=..., exprs=...)`. The function takes two arguments: the accumulated result (initialised to `acc`) and the successive values of the expressions in `exprs`.

```python
import operator
df.select(
    pl.fold(acc=pl.lit(0), function=operator.add, exprs=pl.col("a", "b")).alias("sum_fold"),
    pl.sum_horizontal(pl.col("a", "b")).alias("sum_horz"),
)
```

Explicitly this equals `f(f(acc, pl.col("a")), pl.col("b"))` with `f = operator.add`. Polars `fold` is very similar to Python `functools.reduce`.

## Choose the initial value acc

Typically, but not always, the identity element of the operation. Multiplying with `acc=pl.lit(0)` gives the wrong result; use `acc=pl.lit(1)`:

```python
pl.fold(acc=pl.lit(1), function=operator.mul, exprs=pl.col("a", "b")).alias("prod")
```

## Predicate across all columns

A concise way to require a condition on every column; this filters rows where all columns are greater than 1:

```python
df.filter(
    pl.fold(acc=pl.lit(True), function=lambda acc, x: acc & x, exprs=pl.all() > 1)
)
```

## Strings

Folds can concatenate strings, but intermediate columns are materialized, giving squared complexity. Use `concat_str` instead:

```python
df.select(pl.concat_str(["a", "b"]))
```

## Gotcha

A wrong `acc` silently changes the answer (zero with multiplication); the docs show this case explicitly.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/expressions/folds/. No claims needed correcting. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
