---
id: computing-software.data-engineering.polars.arrow-zero-copy-interchange
name: arrow-zero-copy-interchange
category: computing-software
field: data-engineering
product: polars
tags: [polars-arrow-interop, arrow, pyarrow, pycapsule, zero-copy, to-arrow, compat-level, from-arrow]
level: practitioner
status: docs-checked
description: "Move Polars data to and from pyarrow zero-copy using to_arrow, CompatLevel, the Arrow PyCapsule Interface (v1.3+) and the Arrow C Data Interface."
sources:
  - https://docs.pola.rs/user-guide/misc/arrow/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exchange Arrow data with Polars

Goal: hand DataFrames and Series to other Arrow libraries (and back) without copying.

## Via pyarrow
```python
df = pl.DataFrame({"foo": [1, 2, 3], "bar": ["ham", "spam", "jam"]})
arrow_table = df.to_arrow()
```
Default output types: `foo: int64`, `bar: large_string`. To ensure zero-copy output use the newest compat level:
```python
arrow_table_zero_copy = df.to_arrow(compat_level=pl.CompatLevel.newest())
```
`bar` then comes out as `string_view`. Import from pyarrow with `pl.from_arrow`.

## Arrow PyCapsule Interface (Polars v1.3 and higher)
A protocol for sharing Arrow data across Python libraries.

Export (pyarrow v15 or higher required for `pa.table`):
```python
import pyarrow as pa
arrow_table = pa.table(df)                       # DataFrame -> pyarrow.Table
arrow_chunked_array = pa.chunked_array(df["foo"])  # Series -> ChunkedArray
arrow_array = pa.array(df["foo"])                # contiguous Array
```
`pa.array(series)` is not zero-copy if the Series has multiple chunks.

Import back:
```python
polars_df = pl.DataFrame(arrow_table)
polars_series = pl.Series(arrow_chunked_array)   # ChunkedArray or Array
```
Any library supporting the PyCapsule Interface works automatically with Polars `Series` and `DataFrame`.

## Library maintainers
Implement the PyCapsule Interface yourself: zero-copy exchange for Series and DataFrame, no required pyarrow dependency, no direct Polars dependency, harder to leak memory than raw-integer pointers, and automatic integration with other PyCapsule libraries.

## Arrow C Data Interface directly
For libraries without PyCapsule support that want interop without pyarrow: export `ArrowArray` C structs with `Series._export_arrow_to_c`; import with `Series._import_arrow_from_c`.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
