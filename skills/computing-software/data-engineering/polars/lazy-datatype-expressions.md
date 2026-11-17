---
id: computing-software.data-engineering.polars.lazy-datatype-expressions
name: lazy-datatype-expressions
category: computing-software
field: data-engineering
product: polars
tags: [polars, lazy, dtype-of, datatype-expressions, map-batches, cast, polars-lazy-datatype-exprs, selectors]
level: practitioner
status: docs-checked
description: "Use pl.dtype_of datatype expressions in Polars to cast to another column's dtype, keep map_batches output dtype, and inspect dtypes at plan time."
sources:
  - https://docs.pola.rs/user-guide/lazy/datatype_exprs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write utility functions that reason about datatypes without hard-coding them.

DataType expressions are resolved during query planning and behave like static datatypes at runtime. They help when you do not control input data, compartmentalise code, or load from heterogeneous sources.

Basics
```python
import polars.selectors as cs
dtype_expr = pl.dtype_of("UserID")
schema = pl.Schema({'UserID': pl.UInt64, 'Name': pl.String})
dtype_expr.collect_dtype(schema)    # debugging: resolve in a given schema
```
Manipulate:
```python
dtype_expr.wrap_in_list().collect_dtype(schema)
dtype_expr.to_signed_integer().collect_dtype(schema)
```
Inspect for runtime use:
```python
df = schema.to_frame()
df.select(
    userid_dtype_name = pl.dtype_of('UserID').display(),
    userid_is_signed  = pl.dtype_of('UserID').matches(cs.signed_integer()),
)
```

Same dtype out as in for map_batches
```python
def inspect(expr: pl.Expr) -> pl.Expr:
    def print_and_return(s: pl.Series) -> pl.Series:
        print(s)
        return s
    return expr.map_batches(print_and_return, return_dtype=pl.dtype_of(expr))

df.select(inspect(pl.col('Name')))
```

Cast one column to another's dtype
```python
df.with_columns(pl.col('UserID').cast(pl.dtype_of('Name')))
```

Why use them: a helper that wraps `map_batches` can declare that its output dtype equals its input's, and a cast can follow another column's dtype, so code keeps working when the input data types change. `collect_dtype(schema)` resolves an expression against a `pl.Schema` for debugging, and `schema.to_frame()` turns a schema into a frame so `display()` and `matches()` can run inside `select`.

Methods shown on the page: `pl.dtype_of`, `collect_dtype(schema)`, `wrap_in_list()`, `to_signed_integer()`, `display()`, `matches(selector)`.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
