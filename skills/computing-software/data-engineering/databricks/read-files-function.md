---
id: computing-software.data-engineering.databricks.read-files-function
name: read-files-function
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, autoloader, read-files, databricks-sql, schema-inference, streaming-tables, ad-hoc-ingestion, uc-volumes]
level: practitioner
status: docs-checked
description: "Query and ingest files with Databricks read_files(): format options, schema inference and hints, rescued data, using it in CTAS and STREAM read_files for streaming tables."
sources:
  - https://docs.databricks.com/en/sql/language-manual/functions/read_files.html
  - https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# read_files()

**Goal:** explore and load files from cloud storage or UC volumes with pure SQL, in SQL warehouses, notebooks and pipelines.

## Query files ad hoc
```sql
SELECT * FROM read_files(
  '/Volumes/raw/landing/vendor_x/2026/10/',
  format => 'csv',
  header => true,
  delimiter => ';',
  schemaHints => 'amount DECIMAL(18,2), order_date DATE',
  rescuedDataColumn => '_rescued_data'
) LIMIT 100;
```
- `format`: `csv`, `json`, `xml`, `parquet`, `avro`, `orc`, `text`, `binaryFile` (inferred from extension if omitted).
- Schema is inferred from a sample (`schemaEvolutionMode` etc. apply only in streaming). Use `schema => 'col1 INT, col2 STRING'` to fix it, or `schemaHints` to override a few columns.
- `_metadata` column available: `SELECT _metadata.file_path, * FROM read_files(...)`.
- Glob patterns in path: `.../2026/10/*/orders_*.json`.

## Batch load (CTAS / INSERT)
```sql
CREATE OR REPLACE TABLE bronze.vendor_x_orders AS
SELECT *, _metadata.file_path AS src_file, current_timestamp() AS ingested_at
FROM read_files('/Volumes/raw/landing/vendor_x/', format => 'csv', header => true);
```
Batch read_files re-reads everything each time; for incremental loads use COPY INTO or streaming.

## Incremental with streaming tables
```sql
CREATE OR REFRESH STREAMING TABLE bronze.vendor_x_orders AS
SELECT *, _metadata.file_path AS src_file
FROM STREAM read_files('/Volumes/raw/landing/vendor_x/', format => 'csv', header => true);
```
`STREAM read_files` uses Auto Loader under the hood: only new files are processed, with schema evolution and checkpoints managed by the pipeline/streaming table. Works in Lakeflow declarative pipelines and DBSQL streaming tables.

## Useful options
- JSON: `multiLine => true`; see the `read_files` page for the option list per format.
- CSV: `mode => 'PERMISSIVE'|'DROPMALFORMED'|'FAILFAST'`, `encoding`, `escape`, `nullValue`.
- `ignoreCorruptFiles`, `pathGlobFilter`, `modifiedAfter`.

## Gotchas
- Inference samples files, so columns that appear only in later files may not be in the inferred schema. Pin schemas for production.
- Requires permission on the path: `READ VOLUME` on a volume, or `READ FILES` on an external location.
- Many small files: listing cost dominates; prefer file notification mode for streaming at scale.

## Verify
- [ ] Row counts and `count(distinct src_file)` match the landing listing.
- [ ] `_rescued_data` is null for all rows (or monitored).

## Checked

2026-10-28. Confirmed: rescuedDataColumn and read_files usage on the JSON format page. Removed: an unconfirmed option and an unconfirmed batch-versus-streaming rescue claim.

Method: documentation only; no commands were run.
