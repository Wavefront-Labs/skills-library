---
id: computing-software.data-science-and-analytics.pandas-numpy.scale-beyond-memory
name: scale-beyond-memory
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [larger-than-memory, pyarrow-backend, dask-polars-options]
level: advanced
status: draft
description: "Pick the lightest option when data outgrows RAM: column selection, chunking, Arrow dtypes, then an out-of-core engine such as Dask or Polars."
sources:
  - https://pandas.pydata.org/docs/user_guide/scale.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scaling decision
1. Load fewer columns/rows (`usecols`, Parquet `columns=`, filters).
2. Smaller dtypes (category, downcast, `dtype_backend="pyarrow"` on read functions in pandas 2.x).
3. Chunked processing for associative aggregates.
4. Out-of-core: Dask DataFrame (partitioned pandas) or Polars lazy `scan_parquet` (separate libraries; see their docs).
## Gotchas
- Dask is lazy; `.compute()` pulls the full result into memory.
- Sorting and joins are the costly shuffles; filter first.
## Verify
- [ ] Peak memory observed (for example via `memory_usage` or an OS monitor) stays under the budget.
