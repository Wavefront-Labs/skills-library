---
id: computing-software.data-engineering.polars.polars-list-eval-agg-and-rowwise
name: polars-list-eval-agg-and-rowwise
category: computing-software
field: data-engineering
product: polars
tags: [polars-list-eval, list, eval, agg, concat-list, explode, expressions]
level: practitioner
status: docs-checked
description: "Operate on Polars List columns: str.split, explode, head/tail/slice, list.eval with pl.element, list.agg, and concat_list for row-wise work."
sources:
  - https://docs.pola.rs/user-guide/expressions/lists-and-arrays/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: compute on the elements inside a `List` column without exploding it.

**Create and explode lists.** Split a string column into lists, then explode if you need one row per element (often unnecessary):

```python
weather = weather.with_columns(pl.col("temperatures").str.split(" "))
result = weather.explode("temperatures")
```

**Slicing.** `list.head`, `list.tail`, `list.slice`:

```python
pl.col("temperatures").list.head(3).alias("head"),
pl.col("temperatures").list.tail(3).alias("tail"),
pl.col("temperatures").list.slice(-3, 2).alias("two_next_to_last"),
```

**Element-wise with `list.eval`.** `eval` is the entry point; inside it `pl.element()` refers to each single element and any expression works. Count unparseable values per row:

```python
pl.col("temperatures")
  .list.eval(pl.element().cast(pl.Int64, strict=False).is_null())
  .list.sum()
  .alias("errors")
```

A regex alternative: `pl.element().str.contains("(?i)[a-z]")` (the page shows `result.equals(result2)` comparing both approaches).

**`eval` vs `agg`.** `eval` always returns a list. `list.agg` unwraps: if the evaluated expression is statically determined to return only one value, `agg` explodes the resulting list into the inner values (like `group_by(...).agg(...)`). Use `agg` to get `min_age` as a scalar:

```python
pl.col("children").list.agg(pl.element().struct.field("age").min()).alias("min_age")
```

Sorting inside lists: `pl.element().sort_by(pl.element().struct.field("age"), descending=True).struct.field("name")` within `list.eval`.

Some aggregations such as `.list.sum()` exist directly in the `list` namespace; more exotic ones like `entropy` are reachable only through `agg`/`eval`: `pl.col("children").list.agg(pl.element().struct.field("age").entropy())`.

**Row-wise across columns.** Combine `pl.concat_list(pl.all().exclude("station"))` with `list.eval` to build custom row-wise expressions, e.g. percentage rank:

```python
rank_pct = (pl.element().rank(descending=True) / pl.element().count()).round(2)
pl.col("all_temps").list.eval(rank_pct, parallel=True).alias("temps_rank")
```

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/expressions/lists-and-arrays/. No claims needed correcting. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
