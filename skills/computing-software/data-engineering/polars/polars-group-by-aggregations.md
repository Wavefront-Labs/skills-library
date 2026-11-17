---
id: computing-software.data-engineering.polars.polars-group-by-aggregations
name: polars-group-by-aggregations
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-aggregation, group-by, agg, conditional-aggregation, filter-in-agg, sort-by, nested-group-by, udf-parallelism]
level: practitioner
status: docs-checked
description: "Write Polars group_by aggregations: counts, conditional sums, filtered means, nested keys, in-group sorting with sort and sort_by, and avoiding lambdas."
sources:
  - https://docs.pola.rs/user-guide/expressions/aggregation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Polars group_by aggregations

Goal: compute many per-group results in one `group_by(...).agg(...)` without pre-filtering or pre-sorting the frame.

## Basics

List as many expressions in `agg` as you like; there is no upper bound.

```python
q = (
    dataset.lazy()
    .group_by("first_name")
    .agg(
        pl.len(),
        pl.col("gender"),           # no aggregate function: values combined into a list
        pl.first("last_name"),      # short for pl.col("last_name").first()
    )
    .sort("len", descending=True)
    .limit(5)
)
df = q.collect()
```

## Conditionals

Count matches without a `lambda`, by summing a Boolean expression:

```python
.group_by("state").agg(
    (pl.col("party") == "Anti-Administration").sum().alias("anti"),
    (pl.col("party") == "Pro-Administration").sum().alias("pro"))
```

## Filter inside the group

To average a subset without dropping rows needed by other aggregations, call `.filter` on the expression. Python helper functions returning expressions cost nothing at run time:

```python
def avg_age(gender: str) -> pl.Expr:
    return compute_age().filter(pl.col("gender") == gender).mean().alias(f"avg {gender} age")
```

## Nested grouping

List several keys: `group_by("state", "party")` with `pl.len().alias("count")`, then `.filter(...)`. Same information as the conditional version, different shape; pick the format that suits the use.

## Sorting in a group

Sorting the frame first and then taking `first()`/`last()` works, but you can also sort inside `agg` without touching the frame order:

```python
get_name().sort().first().alias("alphabetical_first")
pl.col("gender").sort_by(get_name()).first()
```

`sort_by` orders one column by another, also inside `group_by`.

## Do not kill parallelization (Python only)

Polars parallelises aggregating functions over groups. A `lambda` or custom Python function is bound by the GIL, so threads cannot run it concurrently. Stay inside the expression API where possible; in Rust, closures can and will run concurrently. For genuine UDFs see the user-defined functions section.

## Gotcha

The congress dataset example computes ages as if everyone were alive, so averages look nonsensical (historical data back to the 1800s).

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/expressions/aggregation/. No claims needed correcting. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
