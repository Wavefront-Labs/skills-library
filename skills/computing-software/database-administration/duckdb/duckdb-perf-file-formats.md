---
id: computing-software.database-administration.duckdb.duckdb-perf-file-formats
name: duckdb-perf-file-formats
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, performance, parquet, csv, row-group, file-size, sniffer]
level: advanced
status: docs-checked
description: "Decide between querying Parquet in place or loading it into DuckDB, with row-group and file-size targets, gzip CSV loading and sniffer-off bulk CSV reads."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/guides/performance/file_formats.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/parquet/tips.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose file layouts and load strategy that maximize DuckDB scan speed.

Query Parquet directly when: filters, projections and aggregations dominate (zonemap statistics enable pushdown), or disk space is tight (loading takes about the same space as the Parquet).

Load into a DuckDB table when: queries are join-heavy (the native format keeps HyperLogLog statistics for better cardinality estimates and join orders; if a join order on Parquet is poor, load the files), many queries will run on the same data, or files use heavy compression like gzip (Snappy, LZ4, zstd decompress faster). Check codecs with `parquet_metadata`. TPC-H ran about 1.1-5.0x slower on Parquet than on a DuckDB database.

Row group size: aim for 100K-1M rows per row group. DuckDB parallelizes over row groups, so one giant group means one thread. Benchmark of an aggregation: 960 rows per group took 8.77 s; 122,880 took 0.87 s; above 100,000 the spread was about 10%. Under 5,000 rows is 5-10x worse; 5,000-20,000 is 1.5-2.5x off. Set with `COPY ... (FORMAT parquet, ROW_GROUP_SIZE n)`.

File size: have at least as many row groups across all files as CPU threads (10 files with 1 group or 1 file with 10 groups both saturate 10 threads). Ideal individual file size is 100 MB to 10 GB.

Hive partitioning on the columns used in filters lets DuckDB read only matching folders, especially useful for remote files (duckdb-hive-partitioning-read).

CSV: gzip CSV can be read directly and was faster to load than decompressing first (107.1 s vs 121.3 s in the docs example).

Many small CSV files: the sniffer runs on every file. If all share one dialect and schema, copy the options from `sniff_csv` once and disable it:

```sql
.mode line
SELECT Prompt FROM sniff_csv('part-0001.csv');
FROM read_csv('part-*.csv', auto_detect=false, delim=',', quote='"', escape='"',
  new_line='\n', skip=0, header=true, columns={'hello': 'BIGINT', 'world': 'VARCHAR'});
```

Related: duckdb-parquet-tips, duckdb-parquet-metadata-functions, duckdb-csv-sniffer-auto-detection.

## Checked

2026-11-07. Read the DuckDB 1.4 docs page guides/performance/file_formats.md in full, plus data/parquet/tips.md for the `ROW_GROUP_SIZE` COPY option. Confirmed: reasons to query or load Parquet, the TPC-H 1.1-5.0x figure, 100K-1M rows per row group, the row-group benchmark table and its summary (5-10x, 1.5-2.5x, about 10%), row groups across files versus threads, 100 MB to 10 GB file size, Hive partitioning advice, gzip CSV load times (107.1 s vs 121.3 s), the sniffer-off procedure with `sniff_csv` and its read_csv options. Removed the invented Verify step.

Method: documentation only; no commands were run.
