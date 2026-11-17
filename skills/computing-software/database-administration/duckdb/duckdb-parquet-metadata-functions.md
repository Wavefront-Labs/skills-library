---
id: computing-software.database-administration.duckdb.duckdb-parquet-metadata-functions
name: duckdb-parquet-metadata-functions
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, parquet, parquet-metadata, parquet-schema, bloom-filter]
level: advanced
status: docs-checked
description: "Inspect Parquet files in DuckDB with parquet_metadata, parquet_schema, parquet_file_metadata, parquet_kv_metadata and parquet_bloom_probe."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/parquet/metadata.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/parquet/overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: see how a Parquet file is laid out (row groups, stats, codecs, encryption) to explain scan speed or skipping.

Functions (each takes a file path, as in the page examples):
- `parquet_metadata(f)`: file metadata including per-column statistics, useful for judging what skipping is possible. Columns include `file_name`, `row_group_id`, `row_group_num_rows`, `row_group_num_columns`, `row_group_bytes`, `column_id`, `file_offset`, `num_values`, `path_in_schema`, `type`, `stats_min`, `stats_max`, `stats_min_value`, `stats_max_value`, `stats_null_count`, `stats_distinct_count`, `compression`, `encodings`, `index_page_offset`, `dictionary_page_offset`, `data_page_offset`, `total_compressed_size`, `total_uncompressed_size`, `key_value_metadata` (MAP(BLOB, BLOB)), `bloom_filter_offset`, `bloom_filter_length`, `min_is_exact`, `max_is_exact`, `row_group_compressed_bytes`.
- `parquet_schema(f)`: the schema as contained in the file's metadata: `file_name`, `name`, `type`, `type_length`, `repetition_type`, `num_children`, `converted_type`, `scale`, `precision`, `field_id`, `logical_type`. For plain column names and types, `DESCRIBE SELECT * FROM 'f.parquet'` is easier.
- `parquet_file_metadata(f)`: file-level metadata: `file_name`, `created_by`, `num_rows`, `num_row_groups`, `format_version`, `encryption_algorithm`, `footer_signing_key_metadata`.
- `parquet_kv_metadata(f)`: custom key-value metadata, columns `file_name`, `key` and `value` (both BLOB); writing it uses the `KV_METADATA` COPY option (Parquet overview page).

```sql
SELECT path_in_schema, row_group_id, stats_min_value, stats_max_value, compression
FROM parquet_metadata('test.parquet') WHERE path_in_schema = 'ts';
```
Bloom filters are supported for pruning the row groups that need to be read to answer highly selective queries. Supported types: `TINYINT`, `UTINYINT`, `SMALLINT`, `USMALLINT`, `INTEGER`, `UINTEGER`, `BIGINT`, `UBIGINT`, `FLOAT`, `DOUBLE`, `VARCHAR`, `BLOB`. `parquet_bloom_probe(filename, column_name, value)` shows which row groups can be excluded for a value:

```sql
FROM parquet_bloom_probe('my_file.parquet', 'my_col', 500);
-- result columns: file_name, row_group_id, bloom_filter_excludes
```

## Checked

2026-11-07. Read the DuckDB 1.4 docs page data/parquet/metadata.md in full and data/parquet/overview.md. Confirmed: the four functions, every column list (completed to match the page tables, including `row_group_num_columns`, `file_offset`, `num_values`, `index_page_offset`, `file_name`), the DESCRIBE tip, bloom filter supported types and `parquet_bloom_probe` signature and result columns, the `KV_METADATA` COPY option. Removed: "each takes a glob" and "one row per row group per column chunk" (not stated), the advice on overlapping min/max and sorting, the claim that `true` means skippable beyond the page's "can be excluded" wording, and the invented Verify step. Added the Parquet overview page to sources.

Method: documentation only; no commands were run.
