---
id: computing-software.database-administration.duckdb.duckdb-copy-to-file-options
name: duckdb-copy-to-file-options
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, copy, export, csv, parquet, json, partition-by]
level: practitioner
status: docs-checked
description: "Write tables or query results to CSV, Parquet, JSON or BLOB files with DuckDB COPY ... TO, including the key format, partitioning and return options."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/copy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: export data with `COPY ... TO` and choose the right options.

Source is a table name (whole table, or `tbl(col)` for a column subset) or a parenthesised query. `FORMAT` is inferred from the file extension (`.parquet` writes Parquet); an unknown extension means CSV. Options go in parentheses, optionally after `WITH`; booleans accept `true/ON/1`, `false/OFF/0`, or bare `(HEADER)` meaning true. Paths and options may be expressions in parentheses, e.g. `COPY (SELECT 1) TO (getvariable('target_file'))`, or a prepared parameter `TO $1`.

```sql
COPY lineitem TO 'lineitem.tbl' (DELIMITER '|');            -- CSV, header on by default
COPY lineitem TO 'lineitem.tsv' (DELIMITER '\t', HEADER false);
COPY (SELECT 42 AS a) TO 'q.parquet' (FORMAT parquet, COMPRESSION zstd);
COPY (SELECT 42 AS a) TO 'q.json' (FORMAT json, ARRAY true);  -- ARRAY false = newline-delimited
COPY (SELECT 'foo'::BLOB) TO 'x.blob' (FORMAT BLOB);          -- single BLOB column only
```

General options (with few exceptions, all formats): `USE_TMP_FILE` (write `target.csv.tmp` first), `PER_THREAD_OUTPUT` (one file per thread, default false), `FILE_SIZE_BYTES` (creates a directory, rolls to new files; `1000` or `1k`), `PARTITION_BY` (Hive layout), `RETURN_FILES` (adds `files VARCHAR[]` column), `RETURN_STATS` (file path, count, size, column statistics), `PRESERVE_ORDER`, `FILE_EXTENSION`. Only with `PARTITION_BY`: `OVERWRITE_OR_IGNORE`, `OVERWRITE` (removes existing files in target dirs, not on remote filesystems), `APPEND` (regenerates names that exist), `FILENAME_PATTERN` (`{uuid}`, `{uuidv4}`, `{uuidv7}`, `{i}`), `WRITE_PARTITION_COLUMNS` (default false).

CSV: `DELIM`/`SEP` (`,`), `QUOTE` and `ESCAPE` (`"`), `HEADER` (true), `NULLSTR` (empty), `FORCE_QUOTE` (column list), `DATEFORMAT`, `TIMESTAMPFORMAT`, `COMPRESSION` (`none/gzip/zstd`, detected from `.gz`/`.zst`), `PREFIX`/`SUFFIX` (must be used together and need `HEADER false`).

Parquet: `COMPRESSION` (`uncompressed, snappy` default, `gzip, zstd, brotli, lz4, lz4_raw`), `COMPRESSION_LEVEL` 1-22 (zstd only, default 3), `ROW_GROUP_SIZE` (default 122880), `ROW_GROUPS_PER_FILE`, `PARQUET_VERSION` (`V1` default, `V2`), `FIELD_IDS` (`'auto'` or `{i: 42}`; nested use `{my_struct: {__duckdb_field_id: 42, i: 43}}`). `ROW_GROUP_SIZE_BYTES` only applies after `SET preserve_insertion_order = false`.

Gotchas: `COPY` cannot copy table to table; use `INSERT INTO t2 FROM t1`. Postgres-style `WITH DELIMITER '|' CSV HEADER` is also accepted.

## Checked

2026-11-07. Read the COPY Statement page in full and confirmed the FORMAT inference and CSV fallback, boolean spellings, expression targets, the general options table (defaults, PARTITION_BY-only options, FILE_SIZE_BYTES, RETURN_FILES, RETURN_STATS), CSV, Parquet (compression list, level 1-22 for zstd, defaults, FIELD_IDS forms, ROW_GROUP_SIZE_BYTES condition), JSON ARRAY and BLOB options, and the table-to-table limitation. Reworded 'all formats' to match the page's 'with few exceptions' and removed the Verify step.

Method: documentation only; no commands were run.
