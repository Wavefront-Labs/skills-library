---
id: computing-software.data-engineering.polars.polars-join-equi-strategies
name: polars-join-equi-strategies
category: computing-software
field: data-engineering
product: polars
tags: [polars-joins, join, inner-join, left-join, full-join, semi-join, anti-join, coalesce]
level: practitioner
status: docs-checked
description: "Choose a Polars equi join strategy (inner, left, right, full, semi, anti), join on key expressions, and control column coalescing."
sources:
  - https://docs.pola.rs/user-guide/transformations/joins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: combine DataFrames on matching keys with `DataFrame.join`.

```python
props_groups.join(props_prices, on="property_name")           # default how="inner"
```

**Strategies (`how=`)**

| how | Result |
| --- | --- |
| `"inner"` | rows matched on both sides (default) |
| `"left"` | all left rows plus matching right rows; unmatched left rows get `null` right columns |
| `"right"` | like left with arguments swapped; all right rows kept, left columns `null` when unmatched |
| `"full"` | all rows from either frame; non-matching rows have the other side `null` |
| `"semi"` | left rows that have a match on the right (no columns joined; acts as a row filter) |
| `"anti"` | left rows that have no match on the right |

`df1.join(df2, how="right", ...)` equals `df2.join(df1, how="left", ...)` up to column order.

**Join on expressions.** `left_on` and `right_on` accept arbitrary expressions, so keys can be computed dynamically, e.g. a differently named, differently cased column:

```python
props_groups2.join(
    props_prices2,
    left_on="property_name",
    right_on=pl.col("name").str.to_lowercase(),
)
```

When joining on an expression, Polars preserves the left `property_name` and the right `name` columns so the original values stay available.

**Coalescing.** In a full join on a same-named key you get `property_name` and `property_name_right` to show which side each row came from. Force a single column with `coalesce=True`:

```python
props_groups.join(props_prices, on="property_name", how="full", coalesce=True)
```

When `coalesce` is not set it is determined automatically from the strategy and the key(s); that is why inner, left and right joins behaved as if `coalesce=True`.

Rust note from the page: semi and anti joins need the `semi_anti_join` feature flag.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/transformations/joins/. No claims needed correcting. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
