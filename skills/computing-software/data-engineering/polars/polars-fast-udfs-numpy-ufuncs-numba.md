---
id: computing-software.data-engineering.polars.polars-fast-udfs-numpy-ufuncs-numba
name: polars-fast-udfs-numpy-ufuncs-numba
category: computing-software
field: data-engineering
product: polars
tags: [polars-numpy-functions, numpy, ufunc, numba, guvectorize, map-batches, udf]
level: practitioner
status: docs-checked
description: "Make Polars custom functions fast with NumPy ufuncs and Numba guvectorize, pass multiple columns via a struct, and avoid missing data errors."
sources:
  - https://docs.pola.rs/user-guide/expressions/user-defined-python-functions/
  - https://docs.pola.rs/user-guide/expressions/numpy-functions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep user-defined function work in compiled code and avoid missing-data pitfalls.

**NumPy ufuncs work directly in expressions** (see the NumPy ufunc list). Element-wise functions such as `np.exp`, `np.cos` run with almost zero overhead:

```python
df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
out = df.select(np.log(pl.all()).name.suffix("_log"))
```

With `map_batches`, a ufunc like `numpy.log` runs once on the whole array (a single Python call) rather than per item:

```python
df.select(pl.col("values").map_batches(np.log, return_dtype=pl.Float64))
```

SciPy also ships pre-written ufuncs. A ufunc runs on each item; a generalized ufunc takes a whole NumPy array.

**Numba `@guvectorize`** compiles a Python function into a generalized ufunc (compiled at import time, then fast). The Series is converted to a NumPy array first:

```python
@guvectorize([(int64[:], float64[:])], "(n)->(n)")
def diff_from_mean_numba(arr, result):
    total = 0
    for value in arr:
        total += value
    mean = total / len(arr)
    for i, value in enumerate(arr):
        result[i] = value - mean

df.select(pl.col("values").map_batches(diff_from_mean_numba, return_dtype=pl.Float64))
```

**Multiple columns.** Combine them in a `Struct`, then extract fields inside the function:

```python
@guvectorize([(int64[:], int64[:], float64[:])], "(n),(n)->(n)")
def add(arr, arr2, result):
    for i in range(len(arr)):
        result[i] = arr[i] + arr2[i]

pl.struct(["values_1", "values_2"]).map_batches(
    lambda combined: add(
        combined.struct.field("values_1"), combined.struct.field("values_2")
    ),
    return_dtype=pl.Float64,
).alias("add_columns")
```

**Missing data.** Polars tracks nulls in a separate bitmask that NumPy does not receive, so window functions or `np.convolve` can be flawed. Passing a Series with missing data to a generalized ufunc (such as a `@guvectorize` function) raises an error: either fill in the missing data or drop it first. Item-by-item ufuncs like `numpy.log` are unaffected. Convert with `to_numpy`; missing values become `np.nan`.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/expressions/user-defined-python-functions/; https://docs.pola.rs/user-guide/expressions/numpy-functions/. Corrected: Reworded the null-handling phrase to the page's wording (fill in or drop). Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
