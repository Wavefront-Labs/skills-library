---
id: computing-software.data-engineering.apache-spark.save-modes-and-dynamic-partition-overwrite
name: save-modes-and-dynamic-partition-overwrite
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-data-sources, save-modes, dynamic-partition-overwrite, partitionby, insert-overwrite, partitionoverwritemode, saveastable, insertinto, idempotency]
level: practitioner
status: docs-checked
description: "Write Spark output idempotently: save modes, partitionBy, dynamic vs static partition overwrite, insertInto column-order trap, and replaceWhere for table formats."
sources:
  - https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html#save-modes
  - https://github.com/apache/spark/blob/master/sql/catalyst/src/main/scala/org/apache/spark/sql/internal/SQLConf.scala
  - https://github.com/apache/spark/blob/master/python/pyspark/sql/readwriter.py
  - https://github.com/apache/iceberg/blob/main/docs/docs/spark-writes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Save modes and dynamic partition overwrite

**Goal:** rerunning a day's job replaces that day's data exactly, never wiping other days and never duplicating.

## Save modes
| mode | Effect |
|---|---|
| `errorifexists` or `error` (default) | Fails if target exists |
| `append` | Adds files; rerun = duplicates |
| `overwrite` | Replaces target (see partition mode below) |
| `ignore` | No-op if exists |

## The overwrite trap
```python
df_day.write.mode("overwrite").partitionBy("event_date").parquet("s3://lake/events/")
```
With the default `spark.sql.sources.partitionOverwriteMode=static`, Spark deletes existing partitions ahead of writing, and save modes use no locking and are not atomic (with `overwrite` the data is deleted before the new data is written), so a rerun can remove other days' data. Fix:
```python
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
# or per write:
df_day.write.option("partitionOverwriteMode", "dynamic").mode("overwrite") \
      .partitionBy("event_date").parquet("s3://lake/events/")
```
In dynamic mode Spark does not delete partitions ahead and only overwrites partitions that have data written into them at runtime. The writer option `partitionOverwriteMode` takes precedence over the session setting. Check what an empty input day should do, since a partition with no written data is not overwritten.

## Tables
- `saveAsTable` uses column names to find positions.
- `insertInto("db.t")` ignores column names and uses position-based resolution: a reordered DataFrame writes values into the wrong columns. Select the table's columns in order first, or use SQL `INSERT OVERWRITE TABLE t PARTITION (event_date) SELECT ...` with explicit columns.
- `spark.sql.sources.partitionOverwriteMode` does not affect Hive serde tables: they are always overwritten in dynamic mode.

## Table formats
Iceberg tables use the DataFrameWriterV2 API: `df.writeTo("t").overwritePartitions()`. The Iceberg docs recommend `MERGE INTO` over `INSERT OVERWRITE` because only affected data files are replaced and the data a dynamic overwrite replaces can change if the table's partitioning changes. For Delta Lake overwrite options, see the Delta documentation.

## Partitioning choice
- `partitionBy` suits low-cardinality columns; `bucketBy` is for a fixed number of buckets when the number of unique values is unbounded (documented in the load/save guide).
- Control files per partition: `df.repartition("event_date")` before writing gives one file per date (possibly huge); `repartition(N, "event_date")` or `spark.sql.files.maxRecordsPerFile` (default 0, no limit) splits them.

## Plain-file atomicity
Spark's file save modes are not atomic and take no locks, so a failed overwrite can leave data deleted but not rewritten. Use a table format with transactional commits for data that readers query while you write.

## Verify
- [ ] Rerun the same day twice: row count for that day unchanged, other days unchanged.
- [ ] Session or write option sets dynamic overwrite wherever `overwrite` + `partitionBy` appear.
- [ ] No `insertInto` without an explicit, ordered column projection.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/, SQLConf.scala and python/pyspark/sql/readwriter.py on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed: save mode names, default errorifexists, and the not-atomic / delete-before-write warning (load/save guide); partitionOverwriteMode static vs dynamic semantics, writer-option precedence and the Hive serde exception (SQLConf.scala); insertInto position-based vs saveAsTable name-based resolution (readwriter.py docstrings); maxRecordsPerFile default 0; bucketBy guidance (load/save guide); Iceberg writeTo().overwritePartitions() and MERGE INTO recommendation (Iceberg docs). Wrong claim fixed: Hive tables do not honour the setting, they are always dynamic. Removed unverified Delta replaceWhere example and a claim that static mode deletes every partition on DataFrame writes.

Method: documentation only; no commands were run.
