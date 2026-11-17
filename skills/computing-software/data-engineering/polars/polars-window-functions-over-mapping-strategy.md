---
id: computing-software.data-engineering.polars.polars-window-functions-over-mapping-strategy
name: polars-window-functions-over-mapping-strategy
category: computing-software
field: data-engineering
product: polars
tags: [polars-window-functions, over, mapping-strategy, window, group-to-rows, explode, join, expressions]
level: practitioner
status: docs-checked
description: "Use Polars window functions with over() to compute per-group ranks and aggregates, and pick mapping_strategy group_to_rows, explode or join."
sources:
  - https://docs.pola.rs/user-guide/expressions/window-functions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run an expression within groups while keeping results aligned with the original frame.

`over` performs the expression within each group, in the `select` context. It accepts an arbitrary number of expressions to specify the groups.

```python
pokemon.select(
    pl.col("Name", "Type 1"),
    pl.col("Speed").rank("dense", descending=True).over("Type 1").alias("Speed rank"),
)
```

Over two columns for finer groups: `.over("Type 1", "Type 2")`. Ranks are per group: on the page a Golbat with Speed 90 does not outrank Venusaur (Speed 80, rank 1) because they have different "Type 1" values.

**Equivalent to group_by + explode**, but rows come out in a different order. Typically `group_by` gives one row per group, `over` gives as many rows as the original (not always: see `explode` below).

**Scalar results** (e.g. `mean`) are broadcast across the rows of the group:

```python
pl.col("Speed").mean().over(pl.col("Type 1")).alias("Mean speed in group")
```

**`mapping_strategy` parameter**
- `"group_to_rows"` (default): the result must match the group's length and is mapped back to that group's rows. Row positions stay; only values within them are reordered.

```python
athletes.select(
    pl.col("athlete", "rank").sort_by(pl.col("rank")).over(pl.col("country")),
    pl.col("country"),
)
```

- `"explode"`: values of the same group are placed next to each other in a new frame, so row order across groups changes. Typically faster because positions need not be tracked, but you must take care since the other columns you keep must be reordered too:

```python
athletes.select(
    pl.all().sort_by(pl.col("rank")).over(pl.col("country"), mapping_strategy="explode"),
)
```

- `"join"`: aggregates resulting values in a list and repeats it over all rows of the group:

```python
athletes.with_columns(
    pl.col("rank").sort().over(pl.col("country"), mapping_strategy="join"),
)
```

Top-3 per group pattern: `pl.col("Name").sort_by(pl.col("Speed"), descending=True).head(3).over("Type 1", mapping_strategy="explode")`.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/expressions/window-functions/. Corrected: Reworded the over intro and the rank explanation to match the page's example. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
