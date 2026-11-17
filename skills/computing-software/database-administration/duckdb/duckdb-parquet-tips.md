---
id: computing-software.database-administration.duckdb.duckdb-parquet-tips
name: duckdb-parquet-tips
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, parquet, row-group-size, per-thread-output, performance]
level: advanced
status: docs-checked
description: "Tune Parquet writes in DuckDB: ROW_GROUP_SIZE trade-offs, ROW_GROUPS_PER_FILE, PER_THREAD_OUTPUT, and union_by_name for mixed schemas."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/parquet/tips.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose write options so later Parquet reads are fast and writes use all threads.

`ROW_GROUP_SIZE`: the minimum rows per row group. Minimum value is DuckDB's vector size, 2,048; default 122,880.
- Larger groups compress better (compression is applied per row group) but each writer thread buffers more rows before flushing when streaming.
- Smaller groups let DuckDB read groups in parallel even inside one file and skip groups by predicate pushdown (metadata ranges vs the WHERE clause), at the cost of metadata overhead per group.
- Rule of thumb: at least as many row groups per file as CPU threads that will query it. More groups help highly selective queries but slow full scans such as aggregations.

```sql
COPY (FROM generate_series(100_000)) TO 'row-groups.parquet'
  (FORMAT parquet, ROW_GROUP_SIZE 100_000);
```

`ROW_GROUPS_PER_FILE n` starts a new file when the current one holds n row groups (writes to a directory):

```sql
COPY (FROM generate_series(100_000)) TO 'output-directory'
  (FORMAT parquet, ROW_GROUP_SIZE 20_000, ROW_GROUPS_PER_FILE 2);
```
With several writer threads a file may slightly exceed the count (to limit locking, same as `FILE_SIZE_BYTES`); with `PER_THREAD_OUTPUT` only one thread writes each file, so the count becomes exact.

`PER_THREAD_OUTPUT`: when the number of output files does not matter, writing one file per thread can speed up the write significantly:

```sql
COPY (FROM generate_series(10_000_000)) TO 'test.parquet' (FORMAT parquet, PER_THREAD_OUTPUT);
```

Mixed schemas on read: `read_parquet('flights*.parquet', union_by_name = true)` fills columns missing from some files with NULL.

Multiple files are best handled transparently with a glob on read or with Hive partitioning (duckdb-hive-partitioning-read, duckdb-partitioned-writes). For file sizes see duckdb-perf-file-formats.

## Checked

2026-11-07. Read the DuckDB 1.4 docs page data/parquet/tips.md in full. Confirmed: `union_by_name` with NULL fill, `PER_THREAD_OUTPUT`, `ROW_GROUP_SIZE` meaning (minimum rows, minimum 2,048, default 122,880), compression-per-row-group and memory trade-offs, parallel reads and predicate pushdown, the rule of thumb, `ROW_GROUPS_PER_FILE` semantics and the FILE_SIZE_BYTES-like overshoot with multiple threads, accurate again with `PER_THREAD_OUTPUT`, glob/Hive advice. Removed: the claim that the target of `PER_THREAD_OUTPUT` becomes a directory (the page does not say so) and the invented Verify step.

Method: documentation only; no commands were run.
