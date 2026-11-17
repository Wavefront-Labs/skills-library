---
id: computing-software.data-engineering.polars.polars-udf-map-elements-and-map-batches
name: polars-udf-map-elements-and-map-batches
category: computing-software
field: data-engineering
product: polars
tags: [polars-udf, map-elements, map-batches, return-dtype, is-elementwise, user-defined-function, expressions]
level: practitioner
status: docs-checked
description: "Apply custom Python functions in Polars with map_elements or map_batches, set return_dtype, and use is_elementwise for streaming."
sources:
  - https://docs.pola.rs/user-guide/expressions/user-defined-python-functions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run your own Python function on Polars data, knowing the trade-offs.

Before writing a UDF, the page advises considering Polars plugins (expression plugins, I/O plugins) for better performance and integration. Expressions are flexible enough that custom functions are rarely needed.

**Two APIs**
- `map_elements`: calls the function separately on each value (slow: per-item call overhead, and limited to individual items).
- `map_batches`: always passes the full `Series`; works in `select` or per group in `group_by().agg()`.

```python
def my_log(value):
    return math.log(value)

df.select(pl.col("values").map_elements(my_log, return_dtype=pl.Float64))
```

```python
def diff_from_mean(series):
    total = 0
    for value in series:
        total += value
    mean = total / len(series)
    return pl.Series([value - mean for value in series])

df.select(pl.col("values").map_batches(diff_from_mean, return_dtype=pl.Float64))
df.group_by("keys").agg(
    pl.col("values").map_batches(diff_from_mean, return_dtype=pl.Float64)
)
```

Pure-Python code is slow; minimise the Python you call.

**Streaming.** Passing the full Series can use a lot of memory (copied into a NumPy array). `map_batches(..., is_elementwise=True)` streams results into the function, so it may not get all values at once. It can give incorrect results if set wrongly: only use it for truly element-by-element functions (log of each value); `diff_from_mean` is NOT one.

**Return types** are inferred from the first non-null value returned. Python mapping: `int` -> `Int64`, `float` -> `Float64`, `bool` -> `Boolean`, `str` -> `String`, `list[tp]` -> `List[tp]`, `dict[str, [tp]]` -> `struct`, `Any` -> `object` (avoid). Rust: `i32`/`i64` -> `Int64`, `f32`/`f64` -> `Float64`, `bool`, `String`/`str` -> `String`, `Vec<tp>` -> `List[tp]`. Pass `return_dtype` to override.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/expressions/user-defined-python-functions/. No claims needed correcting. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
