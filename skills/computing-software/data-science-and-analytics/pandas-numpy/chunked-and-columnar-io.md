---
id: computing-software.data-science-and-analytics.pandas-numpy.chunked-and-columnar-io
name: chunked-and-columnar-io
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [chunked-reading, parquet-io, read-parquet]
level: practitioner
status: docs-checked
description: "Process big files with read_csv chunksize and store intermediate data as Parquet for typed, compressed, column-selective reads."
sources:
  - https://pandas.pydata.org/docs/user_guide/io.html#parquet
  - https://pandas.pydata.org/docs/user_guide/scale.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chunked reads and Parquet
```python
parts = []
for chunk in pd.read_csv("big.csv", chunksize=500_000, usecols=["k","v"]):
    parts.append(chunk.groupby("k")["v"].sum())
total = pd.concat(parts).groupby(level=0).sum()

df.to_parquet("out.parquet", engine="pyarrow", index=False)
pd.read_parquet("out.parquet", columns=["k","v"])
```
## Gotchas
- Manual chunking suits simple workflows; operations such as `groupby` are much harder to do chunkwise, so reduce per chunk and then combine, and consider another tool when that is not enough.
- Parquet engine is `pyarrow`, `fastparquet` or `auto`; with `auto` pandas uses pyarrow when installed and falls back to fastparquet.
- Parquet preserves pandas dtypes including timezone-aware datetimes; duplicate and non-string column names are not supported, and a non-default index is written as extra column(s) unless you pass `index`.
- Reading with `columns=` loads only those columns, rather than loading everything and filtering afterwards.
## Verify
- [ ] Chunked total equals a full-load total on a sample file.

## Checked

Method: docs-checked 2026-11-09 against the pandas IO tools user guide (Parquet section) and the scaling to large datasets guide (chunking and column selection), read via text conversion. Dropped the snappy compression argument and the "mean needs sum and count" aside, which those pages do not state.
