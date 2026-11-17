---
id: computing-software.database-administration.duckdb.duckdb-tune-workloads
name: duckdb-tune-workloads
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, performance, out-of-core, spilling, threads, remote-files, prepared-statements]
level: advanced
status: docs-checked
description: "Tune DuckDB workloads: OOM fixes, row-group parallelism, larger-than-memory limits, remote file IO and caching, connection reuse, compressed in-memory tables."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/guides/performance/how_to_tune_workloads.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: diagnose and fix memory, parallelism and IO problems in DuckDB workloads.

Out-of-memory on big import or export (CSV or Parquet larger than RAM): `SET preserve_insertion_order = false;` lets the engine reorder results without ORDER BY and can cut memory.

Parallelism is per row group (default 122,880 rows in DuckDB's own format). A query needs at least k x 122,880 rows to use k threads. Set row group size on attach: `ATTACH '/tmp/somefile.db' AS db (ROW_GROUP_SIZE 16384);`. If hyper-threading launches too many threads and slows things down, `SET threads = X;`.

Larger-than-memory: works by spilling to `<database_file_name>.tmp` (persistent) or `.tmp` (in-memory); relocate with `SET temp_directory = '/path/to/temp_dir.tmp/';`. Blocking operators (GROUP BY, JOIN, ORDER BY, window functions) all support spilling. Limits: several blocking operators in one query can still OOM; `list()` and `string_agg()` cannot offload; aggregates with ORDER BY are holistic and may OOM; `PIVOT` uses `list()` internally so shares that limit.

Profiling: `EXPLAIN` shows the plan; `EXPLAIN ANALYZE` runs it and shows per-step CPU time (summed thread time exceeds wall time). Look for nested loop joins (prefer hash joins), scans lacking filter pushdown, and join orders that explode cardinality.

Prepared statements help mostly for repeated small queries (under about 100 ms) with changing parameters; many tiny concurrent queries are not a design goal.

Remote files: IO is synchronous, one HTTP request per thread at a time, so for many small requests raise `threads` to roughly 2-5 times the CPU cores. Avoid `SELECT *`, filter remote Parquet, and sort or partition by commonly filtered columns. `EXPLAIN ANALYZE` reports total requests and bytes transferred. Since 1.3.0 remote data is cached; inspect with `FROM duckdb_external_file_cache();`.

Connections: reuse one connection (or a pool); closing the last connection drops cached data and metadata. Extra connections can process more operations concurrently, most helpful when DuckDB is bottlenecked by another resource such as network speed rather than CPU.

Compression: by default only persistent databases are compressed. TPC-H Q1 at SF30: in-memory uncompressed 4.22 s, in-memory compressed 0.55 s (`ATTACH ':memory:' AS db (COMPRESS); USE db;`), persistent 0.56 s.

## Checked

2026-11-07. Read the DuckDB 1.4 docs page guides/performance/how_to_tune_workloads.md in full. Confirmed: `preserve_insertion_order`, row group size 122,880 and the k-threads rule, ATTACH ROW_GROUP_SIZE example, too-many-threads advice, spilling directories and `temp_directory`, blocking operators and their limitations, EXPLAIN versus EXPLAIN ANALYZE and the three plan hints, prepared statements (under 100 ms), remote-file threads (2-5 times cores) and data-reduction tips, caching since 1.3.0 and `duckdb_external_file_cache()`, connection advice, TPC-H Q1 SF30 timings. Changed: reworded the multiple-connections sentence to the page's softer claim; removed the invented Verify step.

Method: documentation only; no commands were run.
