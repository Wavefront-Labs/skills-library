---
id: computing-software.data-engineering.polars.io-hive-partitioned-parquet
name: io-hive-partitioned-parquet
category: computing-software
field: data-engineering
product: polars
tags: [polars, io, hive, hive-partitioning, scan-parquet, write-parquet, partition-by, polars-io-hive]
level: practitioner
status: docs-checked
description: "Scan hive-partitioned Parquet/IPC with scan_parquet and hive_partitioning, handle mixed-file directories with globs, and write partition_by datasets."
sources:
  - https://docs.pola.rs/user-guide/io/hive/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read and write hive-partitioned datasets (paths like year=2024/month=01/data.parquet).

Scanning supports Parquet and IPC. Hive parsing is on by default only when `scan_parquet` receives a single directory path; otherwise off. Override with `hive_partitioning`.

Directory scan (parts in the path become columns)
```python
df = pl.scan_parquet("docs/assets/data/hive/").collect()
```

Mixed files in a directory
A directory containing e.g. `description.txt` fails (not a valid parquet file). Use a glob and set `hive_partitioning=True` explicitly:
```python
df = pl.scan_parquet(
    "docs/assets/data/hive_mixed/**/*.parquet",
    hive_partitioning=True,
).collect()
```

File path lists
Not enabled by default:
```python
paths = [
    "docs/assets/data/hive/year=2024/month=01/data.parquet",
    "docs/assets/data/hive/year=2024/month=02/data.parquet",
]
pl.scan_parquet(paths).collect()                          # no hive columns
pl.scan_parquet(paths, hive_partitioning=True).collect()  # with hive columns
```

Writing (unstable; may change; Parquet only for now)
```python
df = pl.DataFrame({"a": [1, 1, 2, 2, 3], "b": [1, 1, 1, 2, 2], "c": 1})
df.write_parquet("docs/assets/data/hive_write/", partition_by=["a", "b"])
```
This writes a hive-partitioned dataset partitioned by columns `a` and `b`.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). Removed or trimmed claims the cited page does not confirm.

Method: documentation only; no commands were run.
