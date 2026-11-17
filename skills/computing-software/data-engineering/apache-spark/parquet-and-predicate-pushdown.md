---
id: computing-software.data-engineering.apache-spark.parquet-and-predicate-pushdown
name: parquet-and-predicate-pushdown
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-data-sources, parquet, predicate-pushdown, column-pruning, row-groups, mergeschema, parquet-statistics, partition-discovery, file-formats]
level: practitioner
status: docs-checked
description: "Read and write Parquet efficiently in Spark: column pruning, predicate pushdown via row-group stats, partition discovery, mergeSchema cost, and file/row-group sizing."
sources:
  - https://spark.apache.org/docs/latest/sql-data-sources-parquet.html
  - https://parquet.apache.org/docs/file-format/configurations/
  - https://spark.apache.org/docs/latest/sql-performance-tuning.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parquet in Spark: pruning, pushdown and layout

**Goal:** make Parquet scans read only the bytes a query needs.

## What gets skipped
1. **Partition pruning** (directory level): `.../event_date=2026-10-15/` folders are skipped when you filter on `event_date`. Shows as `PartitionFilters` in `explain`.
2. **Column pruning**: only selected columns are read (Parquet is columnar). `select *` reads every column.
3. **Predicate pushdown** (row-group level): Spark pushes filters down to the Parquet reader (`spark.sql.parquet.filterPushdown`, default true) so row groups whose statistics exclude the filter can be skipped. Shows as `PushedFilters`.

```python
df = spark.read.parquet("s3://lake/events/")
q = df.filter("event_date = '2026-10-15' AND customer_id = 42").select("event_type", "amount")
q.explain("formatted")   # look for PartitionFilters and PushedFilters: [IsNotNull(customer_id), EqualTo(customer_id,42)]
```

## Making pushdown work
- Min/max stats only help if data is **clustered** on the filter column. Random order -> every row group's range spans everything -> nothing skipped. Sort within partitions before writing: `df.repartition("event_date").sortWithinPartitions("customer_id").write...`
- Filters wrapped in functions or casts (`upper(col) = 'X'`, string column compared to int) often do not push down. Compare columns in their native type.

## Partition discovery
- Spark infers partition column types from folder names (`spark.sql.sources.partitionColumnTypeInference.enabled`); `id=007` becomes int 7. Supply a schema or disable inference for string IDs.
- Thousands of partitions -> slow file listing on object stores; prefer table formats (Delta/Iceberg) whose metadata avoids listing.

## Schema merging
`mergeSchema=true` merges schemas collected from all Parquet part-files, which costs more on large datasets. `spark.sql.parquet.mergeSchema` defaults to false; enable it only for the read that needs it, or use a table format with managed schema evolution.

## Write sizing
- Compression: `snappy` is the default of `spark.sql.parquet.compression.codec`; other accepted values include `zstd`, `gzip`, `lz4`, `brotli`.

## Verify
- [ ] `explain` shows the expected `PartitionFilters` and `PushedFilters`.
- [ ] Spark UI SQL tab: scan node "number of files read" and "size of files read" drop after adding the filter.
- [ ] Average output file size is reasonable for your storage layer (avoid many tiny files).

## Checked
2026-11-01. Confirmed against the Spark Parquet data source page: partition discovery and `spark.sql.sources.partitionColumnTypeInference.enabled` (default true; string when disabled), `spark.sql.parquet.mergeSchema` default false, `spark.sql.parquet.filterPushdown` default true, compression default snappy and the accepted codecs. Removed: bloom filter option and Parquet version gate, nested schema pruning default, `basePath`, row-group and file size figures, `maxRecordsPerFile`, zstd speed claim.
Method: documentation only; no commands were run.
