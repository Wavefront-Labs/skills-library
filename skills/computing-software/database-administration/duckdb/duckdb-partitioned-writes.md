---
id: computing-software.database-administration.duckdb.duckdb-partitioned-writes
name: duckdb-partitioned-writes
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, partition-by, copy, hive-partitioning, overwrite, append]
level: practitioner
status: docs-checked
description: "Write Hive-partitioned datasets with COPY PARTITION_BY in DuckDB: filename patterns, overwrite and append options, open-file limit, sizing advice."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/partitioning/partitioned_writes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: export a table or query to a `key=value` directory tree of Parquet or CSV files.

```sql
COPY orders TO 'orders' (FORMAT parquet, PARTITION_BY (year, month));
COPY orders TO 'orders' (FORMAT csv, PARTITION_BY (year, month), OVERWRITE_OR_IGNORE);
COPY orders TO 'orders' (FORMAT csv, PARTITION_BY (year, month),
                         COMPRESSION gzip, FILE_EXTENSION 'csv.gz');
```
The target is the root directory name. One file per thread is written to each partition directory (`orders/year=2021/month=1/data_1.parquet`, ...). Partition values are extracted from the data automatically.

Filenames: default `data_0.parquet` or `data_0.csv`. `FILENAME_PATTERN` accepts `{i}` (index) and `{uuid}` (128-bit UUID):

```sql
COPY orders TO 'orders' (FORMAT parquet, PARTITION_BY (year, month),
                         OVERWRITE_OR_IGNORE, FILENAME_PATTERN 'orders_{i}');
COPY orders TO 'orders' (FORMAT parquet, PARTITION_BY (year, month),
                         OVERWRITE_OR_IGNORE, FILENAME_PATTERN 'file_{uuid}');
```

Overwrite: by default writing into an existing directory is refused. On a local file system `OVERWRITE` and `OVERWRITE_OR_IGNORE` remove existing directories; on remote file systems overwriting is not supported.

Append: `APPEND` adds files to an existing hierarchy. It behaves like `OVERWRITE_OR_IGNORE, FILENAME_PATTERN '{uuid}'` but DuckDB also checks whether the file exists and regenerates the UUID on the rare clash.

Memory and file count: the number of files kept open before flushing is capped by `SET partitioned_write_max_open_files = 10;` (default 100). Many small partitions are expensive; the docs recommend at least 100 MB of data per partition, and the ideal partition count depends on dataset size.

Slashes in columns: the page says to use percent-encoding via the `url_encode` text function.

Read it back with duckdb-hive-partitioning-read.

## Checked

2026-11-07. Read the DuckDB 1.4 docs page data/partitioning/partitioned_writes.md in full. Confirmed: all example statements, root-directory target, one file per thread per directory, automatic partition values, `partitioned_write_max_open_files` (default 100), the 100 MB per partition best practice, `FILENAME_PATTERN` with `{i}` and `{uuid}` and default `data_0.*` names, overwrite behaviour (local only), `APPEND` semantics, `url_encode`. Removed: the claim that PARTITION_BY accepts columns but not expressions (not on the page), the "slashes in partition values" wording (page says column names), and the invented Verify step.

Method: documentation only; no commands were run.
