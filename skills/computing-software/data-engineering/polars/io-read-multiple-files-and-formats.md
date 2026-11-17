---
id: computing-software.data-engineering.polars.io-read-multiple-files-and-formats
name: io-read-multiple-files-and-formats
category: computing-software
field: data-engineering
product: polars
tags: [polars, io, csv, ndjson, parquet, glob, polars-io-files, collect-all, multiple-files]
level: practitioner
status: docs-checked
description: "Read, write and scan CSV, JSON, NDJSON and Parquet in Polars, and read many files via globs into one frame or in parallel with scan_csv plus collect_all."
sources:
  - https://docs.pola.rs/user-guide/io/csv/
  - https://docs.pola.rs/user-guide/io/json/
  - https://docs.pola.rs/user-guide/io/parquet/
  - https://docs.pola.rs/user-guide/io/multiple/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right read, write or scan call per file format, and handle many files.

Per-format calls (same shape for each)
- CSV: `pl.read_csv(path)`, `df.write_csv(path)`, `pl.scan_csv(path)`.
- Parquet: `pl.read_parquet`, `df.write_parquet`, `pl.scan_parquet`. Columnar, so better compression and faster access; loading and writing is fast because the in-memory layout mirrors the file layout in many respects.
- JSON: `pl.read_json`, `df.write_json`.
- NDJSON (newline-delimited JSON): `pl.read_ndjson`, `df.write_ndjson`, `pl.scan_ndjson`. NDJSON reads much more performantly than standard JSON.

`scan_*` delays parsing and returns a `LazyFrame`. Scanning a Parquet file in the cloud also gets predicate and projection pushdown (see io-cloud-storage-read-write).

```python
df = pl.DataFrame({"foo": [1, 2, 3], "bar": [None, "bak", "baz"]})
df.write_csv("docs/assets/data/path.csv")
lazy = pl.scan_csv("docs/assets/data/path.csv")
```

Many files into one DataFrame (glob)
```python
df = pl.read_csv("docs/assets/data/my_many_files_*.csv")
```
All files are read separately and concatenated; Polars tries to parallelize. Inspect with `pl.scan_csv(glob).show_graph(plan_stage="ir")` or `plan_stage="physical"`.

Many files, no single table: one query per file, run in parallel on the Polars thread pool (execution is embarrassingly parallel, no communication needed):
```python
import glob
queries = []
for file in glob.glob("docs/assets/data/my_many_files_*.csv"):
    q = pl.scan_csv(file).group_by("bar").agg(pl.len(), pl.sum("foo"))
    queries.append(q)
dataframes = pl.collect_all(queries)
```

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
