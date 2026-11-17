---
id: computing-software.data-engineering.polars.polars-choose-list-or-array-dtype
name: polars-choose-list-or-array-dtype
category: computing-software
field: data-engineering
product: polars
tags: [polars-lists-arrays, list, array, dtype, numpy, nested-data]
level: practitioner
status: docs-checked
description: "Choose between the Polars List and Array data types, build Array columns, and use the arr namespace functions."
sources:
  - https://docs.pola.rs/user-guide/expressions/lists-and-arrays/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick `List` or `Array` for a nested column and build it correctly.

**Rule of thumb.** Prefer `Array` over `List`: it is more memory efficient and more performant. Use `List` when values in a column do not have a fixed shape, or when you need functions only available in the list API.

- `List`: homogeneous 1D containers of varying lengths. It differs from Python's `list`; true Python lists can only be stored with the `Object` dtype, which has none of the list manipulation features.
- `Array`: homogeneous containers of arbitrary dimension with a known, fixed shape.

**Creating an Array column.** Polars does not infer `Array` for performance reasons and defaults to `List`. Specify it in the schema (or cast explicitly):

```python
df = pl.DataFrame(
    {"bit_flags": [[True, True, True, True, False], [False, True, True, True, True]]},
    schema={"bit_flags": pl.Array(pl.Boolean, 5)},
)
# multi-dimensional: pl.Array(pl.String, (3, 3))
```

Exception: building a column from a NumPy array. NumPy guarantees equal subarray shapes, so an array of n + 1 dimensions gives a column of n-dimensional arrays:

```python
array = np.arange(0, 120).reshape((5, 2, 3, 4))  # 4D array
print(pl.Series(array).dtype)  # Column with the 3D subarrays
```

**Namespaces.** List operations live in `list`; `arr` is the namespace for the `Array` dtype. In older Polars versions list operations used `arr`, so StackOverflow answers using `arr` for lists may be outdated.

The `Array` type is described as recent and nascent in features. Example functions from the page:

```python
df.select(
    pl.col("first_last").arr.join(" ").alias("name"),  # Array(String, 2)
    pl.col("fav_numbers").arr.sort(),                  # Array(Int32, 3)
    pl.col("fav_numbers").arr.max().alias("largest_fav"),
    pl.col("fav_numbers").arr.sum().alias("summed"),
    pl.col("fav_numbers").arr.contains(3).alias("likes_3"),
)
```

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
