---
id: computing-software.data-engineering.databricks.auto-loader-schema-inference-and-evolution
name: auto-loader-schema-inference-and-evolution
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, autoloader, auto-loader, cloudfiles, schema-hints, schema-evolution, schema-inference, schemalocation, incremental-ingestion, structured-streaming]
level: practitioner
status: docs-checked
description: "Configure Auto Loader (cloudFiles): schema location and inference, schema hints, evolution modes, availableNow triggers, production options."
sources:
  - https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/
  - https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/schema
  - https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/production
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auto Loader: options, schema inference and evolution

**Goal:** ingest new files from cloud storage exactly once into a bronze Delta table, surviving new columns and bad types without manual babysitting.

## 1. Baseline stream
```python
(spark.readStream.format("cloudFiles")
   .option("cloudFiles.format", "json")                      # json, csv, parquet, avro, orc, text, binaryFile, xml
   .option("cloudFiles.schemaLocation", "/Volumes/prod/bronze/_meta/orders_schema")
   .option("cloudFiles.inferColumnTypes", "true")            # infer column types for JSON, CSV and XML
   .option("cloudFiles.schemaHints", "order_id BIGINT, amount DECIMAL(18,2), ts TIMESTAMP")
   .load("/Volumes/prod/landing/orders/")
 .withColumn("_ingest_file", F.col("_metadata.file_path"))
 .withColumn("_ingest_ts", F.current_timestamp())
 .writeStream
   .option("checkpointLocation", "/Volumes/prod/bronze/_meta/orders_ckpt")
   .option("mergeSchema", "true")
   .trigger(availableNow=True)                               # incremental batch; drop for continuous
   .toTable("prod.bronze.orders"))
```
- File state (which files were discovered) is persisted in a key-value store (RocksDB) in the **checkpoint** location. Losing or sharing the checkpoint = re-ingest or skipped files. One checkpoint per stream.
- The inferred schema is stored under `schemaLocation` (`_schemas`); inference samples the first 50 GB or 1000 files discovered, whichever limit is crossed first; change it with the SQL configs `spark.databricks.cloudFiles.schemaInference.sampleSize.numBytes` and `spark.databricks.cloudFiles.schemaInference.sampleSize.numFiles`.

## 2. Schema hints
Use hints for columns where inference picks the wrong type, for nested fields, maps and arrays, or for a column you want fixed regardless of data. Hints override inference only for the named columns, and Auto Loader uses them only if you do not provide a schema.

## 3. Evolution modes (`cloudFiles.schemaEvolutionMode`)
| Mode | New column appears | Use |
|---|---|---|
| `addNewColumns` (default when no schema is provided; `none` is the default when you provide one) | stream **fails** once with `UnknownFieldException` after the schema is updated; restart continues with the column | most bronze tables — run under a job that restarts |
| `addNewColumnsWithTypeWidening` | as `addNewColumns`, and supported type widenings (such as int to long) are applied | when upstream types widen |
| `rescue` | schema never changes; new columns are recorded in the rescued data column | strict schemas, contracts |
| `failOnNewColumns` | stream fails and does not restart until you update the provided schema or remove the offending file | regulated feeds |
| `none` | new columns ignored and not rescued unless `rescuedDataColumn` is set | rarely |
With `addNewColumns`, Databricks recommends configuring the stream with Lakeflow Jobs so the expected stop-and-restart is automatic. Existing columns do not evolve data types in `addNewColumns`. `addNewColumns` is not allowed when you provide a schema, but works if you provide it as a schema hint. The rescued data column is added as `_rescued_data` when Auto Loader infers the schema.

## 4. Other production options
- `modifiedAfter` / `pathGlobFilter` — limit which files are considered.
- `cloudFiles.cleanSource` (`MOVE` or `DELETE`, with `cloudFiles.cleanSource.retentionDuration`) — archive or delete processed source files to lower directory-listing cost; with `DELETE` Databricks recommends enabling bucket versioning.
- Partition columns are inferred from `key=value` directory names; set `cloudFiles.partitionColumns` (comma-separated) to capture new partition columns.
- Directory listing vs file notification: see the file-notification skill.

## Verify
- [ ] Re-running the job with no new files writes 0 rows.
- [ ] Adding a file with a new column results in one failed attempt then success with the column added.
- [ ] Hinted columns have the intended types in `DESCRIBE TABLE`.
- [ ] Checkpoint and schema locations are unique to this stream.

## Checked

2026-11-09. Confirmed on the Auto Loader overview, schema inference and evolution, and production pages: supported file formats, RocksDB file state in the checkpoint, 50 GB or 1000 file sample and its SQL configs, inferColumnTypes, schemaHints behaviour, evolution modes and defaults, UnknownFieldException, _rescued_data, cleanSource MOVE or DELETE with retentionDuration, partitionColumns. Removed: includeExistingFiles default, maxBytesPerTrigger and maxFilesPerTrigger lines (the Auto Loader options reference was not read), decimal and leading-zero hint examples, and the unlimited retries remark.

Method: documentation only; no commands were run.

