---
id: computing-software.data-engineering.databricks.rescued-data-column
name: rescued-data-column
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, rescued-data, rescueddatacolumn, autoloader, schema-mismatch, bad-records, data-quality, bronze-layer]
level: practitioner
status: docs-checked
description: "Use the _rescued_data column to keep rows whose fields don't match the schema: what lands in it, enabling it for readers, alerting on it and repairing data from it."
sources:
  - https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/schema#what-is-the-rescued-data-column
  - https://docs.databricks.com/aws/en/query/formats/json
  - https://docs.databricks.com/aws/en/ingestion/bad-records
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The rescued data column

**Goal:** never silently drop data that doesn't fit the expected schema; capture it, alert on it, and recover it.

## 1. What goes into `_rescued_data`
A JSON blob per row containing fields that could not be parsed into the schema:
- fields that are **absent from the provided schema** (with Auto Loader this includes new columns when the evolution mode is `rescue`);
- fields that **don't match the data type** of the schema;
- fields whose name has a **case mismatch** with a schema column;
plus the source file path of the record (Databricks documents a setting to remove the path).

## 2. Enable it
- Auto Loader with inferred schema: added automatically to the schema as `_rescued_data`; with a provided schema, include it by setting the `rescuedDataColumn` option.
- Plain batch JSON readers: set the `rescuedDataColumn` option to a column name:
```python
df = (spark.read.format("json")
      .option("rescuedDataColumn", "_rescued_data")
      .load("/Volumes/prod/landing/orders/"))
```
```sql
SELECT * FROM read_files('/Volumes/prod/landing/orders/', format => 'json',
                         rescuedDataColumn => '_rescued_data');
```
- With `rescuedDataColumn` set, data type mismatches do not drop records in `DROPMALFORMED` mode or fail in `FAILFAST` mode, and they are not treated as bad records for `badRecordsPath`; only incomplete or malformed records are.

## 3. Watch it
```sql
SELECT date(_ingest_ts) AS d, count(*) AS rescued_rows
FROM prod.bronze.orders WHERE _rescued_data IS NOT NULL GROUP BY d ORDER BY d DESC;
```
- To see which fields are being rescued, inspect a sample of the non-null `_rescued_data` blobs.
- Add an expectation in silver, `CONSTRAINT no_rescued EXPECT (_rescued_data IS NULL)` (the `CONSTRAINT ... EXPECT (...)` clause is the documented expectation syntax), and alert when the count is non-zero.
- A sudden spike usually means a producer changed a type or field name.

## 4. Repair
- Fix the schema (for example a schema hint), then rebuild silver from bronze, parsing the rescued values out of the JSON blob.
- Bronze keeps the rescued value, so no re-ingestion from source is needed.

## Verify
- [ ] Every bronze table built with an explicit schema has a rescued data column.
- [ ] A row with a wrong-typed field lands with the field in `_rescued_data`, not dropped.
- [ ] Rescued-row counts are monitored with an alert threshold.

## Checked
2026-11-01. Confirmed against the Databricks pages on Auto Loader schema inference and evolution (rescued data column section), Read and write JSON files (enabling the column, parser modes, badRecordsPath) and Lakeflow pipeline expectations (CONSTRAINT EXPECT syntax). Removed: the CSV and Avro/Parquet batch-reader claim, the `_file_path` field name, `schema =>` in `read_files`, the `map_keys`, `from_json` and `try_cast` example SQL, and the opinion on `badRecordsPath`.
Method: documentation only; no commands were run.
