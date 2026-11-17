---
id: computing-software.data-engineering.apache-spark.kryo-and-small-file-compaction
name: kryo-and-small-file-compaction
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-tuning, kryo-serialization, small-file-compaction, small-file-problem, maxrecordsperfile, coalesce-hint, rebalance-hint, file-sizing, spark-sql-files-maxpartitionbytes]
level: practitioner
status: docs-checked
description: "Two Spark tuning-guide fixes: Kryo serialization for RDD/shuffle-heavy code, and avoiding/compacting small files with REBALANCE hints, maxRecordsPerFile and compaction jobs."
sources:
  - https://spark.apache.org/docs/latest/tuning.html#data-serialization
  - https://spark.apache.org/docs/latest/sql-performance-tuning.html#coalesce-hints-for-sql-queries
  - https://spark.apache.org/docs/latest/sql-performance-tuning.html#other-configuration-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kryo serialization and small-file compaction

## Part 1: Kryo
DataFrame/SQL code uses Tungsten's binary format internally, so the serializer matters mainly for **RDD code, cached RDDs, shuffled JVM objects, and broadcast of objects**.
```properties
spark.serializer=org.apache.spark.serializer.KryoSerializer
spark.kryo.registrationRequired=false       # true in tests to catch unregistered classes
spark.kryo.classesToRegister=com.acme.Event,com.acme.Order
spark.kryoserializer.buffer.max=256m         # default 64m; must exceed your largest object and stay below 2048m
```
Unregistered classes still work but Kryo writes the class name with each object, which can cost significant performance. PySpark RDDs pickle on the Python side; Kryo does not help Python objects.

## Part 2: small files
**Symptoms:** thousands of KB-sized files per partition; slow listing on S3/ADLS; reads with tens of thousands of tiny tasks; downstream engines (Trino, Athena) slow.
**Causes:** writing straight after a 200-partition shuffle with `partitionBy` (each task writes a file per partition value it holds -> up to tasks x partitions files); frequent micro-batches; `append` every few minutes.

### Prevent at write time
```python
# group rows of each output partition into the same tasks before writing
df.repartition("event_date").write.partitionBy("event_date").parquet(path)        # 1 file per date
df.repartition(64, "event_date", "bucket").write...                              # more files for big dates
```
```sql
INSERT OVERWRITE TABLE t SELECT /*+ REBALANCE(event_date) */ * FROM src   -- AQE splits skewed, merges small
SELECT /*+ COALESCE(16) */ ...                                            -- reduce partitions without shuffle
```
- `spark.sql.adaptive.coalescePartitions.enabled` (default true when AQE is on) coalesces to the target size from `spark.sql.adaptive.advisoryPartitionSizeInBytes` (64 MB by default); raise it for bigger post-shuffle partitions.
- `maxRecordsPerFile` caps file size when one partition value is huge.
- `coalesce(n)` before write avoids a shuffle but also reduces upstream parallelism (the whole last stage runs on n tasks); `repartition` costs a shuffle but keeps upstream parallel.

### Compact after the fact
Plain Parquet: a scheduled job reads a partition and rewrites it with fewer files to a new location, then swaps (not atomic; readers may see gaps). Table formats (Delta, Iceberg) ship compaction commands; use theirs, per their own docs.

### Reading many small files
`spark.sql.files.maxPartitionBytes` (128 MB) and `spark.sql.files.openCostInBytes` (4 MB) control how files are packed into read partitions; the docs say it is better to over-estimate the open cost.

## Verify
- [ ] Average output file size per partition >= ~128 MB (check with `aws s3 ls --summarize` or table `DESCRIBE DETAIL`).
- [ ] File count per partition is stable run to run.
- [ ] Kryo enabled for RDD-heavy jobs and no Kryo buffer-limit errors in logs.

## Checked
2026-10-31. Confirmed against the Spark configuration and SQL performance tuning pages: Kryo registration and buffer settings and defaults, AQE coalesce and advisory-size defaults, REBALANCE and COALESCE hints, `maxPartitionBytes` and `openCostInBytes` defaults. Removed unconfirmed Delta and Iceberg compaction commands and the openCostInBytes direction claim.
Method: documentation only; no commands were run.
