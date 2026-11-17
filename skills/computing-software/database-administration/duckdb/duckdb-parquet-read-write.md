---
id: computing-software.database-administration.duckdb.duckdb-parquet-read-write
name: duckdb-parquet-read-write
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, parquet, read-parquet, copy, compression, schema-evolution]
level: practitioner
status: docs-checked
description: "Read and write Parquet in DuckDB: read_parquet parameters, schema parameter with field IDs, pushdown, views over files, COPY compression and KV metadata."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/parquet/overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: query Parquet in place or load it, and write it with the right codec and options.

Read:

```sql
SELECT * FROM 'test.parquet';
DESCRIBE SELECT * FROM 'test.parquet';
SELECT *, filename FROM read_parquet('test/*.parquet');         -- filename is a virtual column since 1.3.0
SELECT * FROM read_parquet(['folder1/*.parquet','folder2/*.parquet']);
SELECT * FROM read_parquet('https://some.url/some_file.parquet');
CREATE VIEW people AS SELECT * FROM read_parquet('test.parquet');  -- keep data in the file
```
`read_parquet` (alias `parquet_scan`) is needed only when the name does not end in `.parquet`. Parameters: `binary_as_string` (false; set true for legacy writers whose strings load as BLOB), `file_row_number` (false), `filename`, `hive_partitioning` (auto), `union_by_name` (false), `encryption_config`, `schema`.

Pushdown: only the needed columns are read, and filters use row-group zonemaps (min/max) to skip data when the file has them.

`schema` parameter (MAP keyed by field id) renames, adds, reorders or casts columns on read; it requires field IDs and cannot be combined with `union_by_name=true`:

```sql
COPY (SELECT 42::INTEGER i) TO 'integers.parquet' (FIELD_IDS {i: 0});
SELECT * FROM read_parquet('integers.parquet', schema = MAP {
  0: {name:'renamed_i', type:'BIGINT', default_value:NULL},
  1: {name:'new_column', type:'UTINYINT', default_value:43}});
```

Write with COPY (default codec is Snappy):

```sql
COPY (SELECT * FROM tbl) TO 'out.parquet' (FORMAT parquet);
COPY tbl TO 'z.parquet' (FORMAT parquet, COMPRESSION zstd, COMPRESSION_LEVEL 1, ROW_GROUP_SIZE 100_000);
COPY (SELECT 42 AS number) TO 'kv.parquet' (FORMAT parquet, KV_METADATA {number: 'Answer'});
EXPORT DATABASE 'target_directory' (FORMAT parquet);
```
Codecs shown: `uncompressed`, `snappy`, `zstd`, `lz4` (= `lz4_raw`), `brotli`. `STRING_DICTIONARY_PAGE_SIZE_LIMIT` defaults to 1 MB. Single quotes inside KV values must be doubled.

Load into a table with `INSERT INTO t SELECT * FROM read_parquet(...)` or `CREATE TABLE ... AS`. The `parquet` extension is bundled with almost all clients; otherwise `INSTALL parquet;`. See duckdb-parquet-tips for row-group sizing, duckdb-parquet-metadata-functions, duckdb-parquet-encryption.

## Checked

2026-11-07. Read the DuckDB 1.4 docs page data/parquet/overview.md in full. Confirmed: all read and write examples, `read_parquet`/`parquet_scan` alias, the parameter table (`binary_as_string`, `encryption_config`, `filename`, `file_row_number`, `hive_partitioning`, `union_by_name`, `schema` with defaults), the schema/FIELD_IDS example, projection and filter pushdown with zonemaps, views, Snappy default, zstd/lz4/lz4_raw/brotli/uncompressed, `STRING_DICTIONARY_PAGE_SIZE_LIMIT` default 1 MB, KV_METADATA quote escaping, EXPORT DATABASE, bundled `parquet` extension. Removed the invented Verify step. The page says `schema` supports renaming, adding, deleting, reordering and casting; the skill's shorter list is a subset.

Method: documentation only; no commands were run.
