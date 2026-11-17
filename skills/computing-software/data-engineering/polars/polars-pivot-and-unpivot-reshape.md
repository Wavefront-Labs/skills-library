---
id: computing-software.data-engineering.polars.polars-pivot-and-unpivot-reshape
name: polars-pivot-and-unpivot-reshape
category: computing-software
field: data-engineering
product: polars
tags: [polars-pivot, polars-unpivot, pivot, unpivot, reshape, wide-to-long, on-columns, lazyframe]
level: practitioner
status: docs-checked
description: "Reshape Polars data with pivot (long to wide, eager or lazy with on_columns) and unpivot (wide to long)."
sources:
  - https://docs.pola.rs/user-guide/transformations/pivot/
  - https://docs.pola.rs/user-guide/transformations/unpivot/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: convert between long and wide layouts.

**Pivot** groups by one or more columns (the new y-axis), pivots a column (the new x-axis) and applies an aggregation. Listed aggregations: first, last, sum, min, max, mean, median, len.

```python
df = pl.DataFrame({
    "foo": ["A", "A", "B", "B", "C"],
    "N": [1, 2, 2, 4, 2],
    "bar": ["k", "l", "m", "n", "o"],
})
out = df.pivot("bar", index="foo", values="N", aggregate_function="first")
```

**Lazy pivot.** A `LazyFrame` must know its schema statically before collecting, but a pivot's output schema depends on the data. Polars deliberately does not hide this cost. Two options:

1. Collect before pivoting (lose lazy benefits):

```python
q = (
    df.lazy().collect()
    .pivot(index="foo", on="bar", values="N", aggregate_function="first")
    .lazy()
)
```

2. Declare the output columns up front with `on_columns`:

```python
q = df.lazy().pivot(
    index="foo",
    on="bar",
    on_columns=["k", "l", "m", "n", "o"],
    values="N",
    aggregate_function="first",
)
out = q.collect()
```

**Unpivot** turns wide into long. Eager and lazy share the same API:

```python
df = pl.DataFrame({"A": ["a", "b", "a"], "B": [1, 3, 5], "C": [10, 11, 12], "D": [2, 4, 6]})
out = df.unpivot(["C", "D"], index=["A", "B"])
```

In this example `C` and `D` are unpivoted and `A` and `B` (`index`) stay as columns; the output has 6 rows with new `variable` (column name) and `value` columns.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/transformations/pivot/; https://docs.pola.rs/user-guide/transformations/unpivot/. Corrected: Reworded the unpivot sentence to match the page's example output. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
