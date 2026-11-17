---
id: computing-software.data-engineering.polars.polars-create-and-inspect-dataframes
name: polars-create-and-inspect-dataframes
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-data-structures, polars-inspecting, series, dataframe, schema, schema-overrides, head-tail-sample, describe]
level: practitioner
status: docs-checked
description: "Create Series and DataFrames, override schema inference with schema or schema_overrides, and inspect data with head, tail, glimpse, sample, describe."
sources:
  - https://docs.pola.rs/user-guide/concepts/data-types-and-structures/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create and inspect Series and DataFrames

Goal: build the two core structures with the dtypes you want, then look at them quickly.

## Structures

- Series: 1-dimensional, homogeneous (one dtype). Dataframe: 2-dimensional, heterogeneous, with uniquely named series.
- Polars infers the dtype from the values; override it with `dtype=`.

```python
s1 = pl.Series("ints", [1, 2, 3, 4, 5])
s2 = pl.Series("uints", [1, 2, 3, 4, 5], dtype=pl.UInt64)
print(s1.dtype, s2.dtype)

df = pl.DataFrame({"name": ["Alice Archer", "Ben Brown"], "weight": [57.9, 72.5]})
```

## Schema

The schema maps column names to dtypes; read it with `df.schema`. Inference can be overridden in Python two ways:

```python
# explicit schema: None keeps inference for that column
pl.DataFrame({"name": ["Alice", "Ben"], "age": [27, 39]},
             schema={"name": None, "age": pl.UInt8})

# schema_overrides: omit the columns you do not want to override
pl.DataFrame({"name": ["Alice", "Ben"], "age": [27, 39]},
             schema_overrides={"age": pl.UInt8})
```

`schema_overrides` is more convenient when only some columns need overriding.

## Inspecting

| Call | Behaviour |
| --- | --- |
| `df.head(3)` | first rows; default 5 |
| `df.tail(3)` | last rows; default 5 |
| `df.glimpse(return_type="string")` | one line per column, easier for wide frames; Python only |
| `df.sample(2)` | random rows, not necessarily in original order; the example calls `pl.set_random_seed(42)` first for reproducibility |
| `df.describe()` | summary statistics for all columns |

## Notes

- Polars uses the Arrow Columnar Format, so data moves to and from other Arrow tools with little to no overhead.
- Most performance comes from the query engine, plan optimizations and parallel expression execution.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
