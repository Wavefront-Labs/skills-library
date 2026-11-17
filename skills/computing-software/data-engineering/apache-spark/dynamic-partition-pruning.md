---
id: computing-software.data-engineering.apache-spark.dynamic-partition-pruning
name: dynamic-partition-pruning
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark-sql, dynamic-partition-pruning, dpp, partition-pruning, star-schema, spark-performance]
level: advanced
status: docs-checked
description: "Make Spark prune fact-table partitions at runtime from a filtered dimension join (DPP): prerequisites, config, and how to confirm it in the plan."
sources:
  - https://spark.apache.org/docs/latest/sql-performance-tuning.html
  - https://github.com/apache/spark/blob/master/sql/catalyst/src/main/scala/org/apache/spark/sql/internal/SQLConf.scala
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic partition pruning (DPP)

**Problem:** `fact JOIN dim ON fact.date_key = dim.date_key WHERE dim.year = 2026` reads every fact partition, because the filter is on the dimension, not on the partition column.

**DPP (since Spark 3.0, `spark.sql.optimizer.dynamicPartitionPruning.enabled` defaults to true):** Spark generates a predicate on the partition column when it is used as a join key, and injects the qualifying keys from the dimension side as a partition filter into the fact scan.

## Prerequisites
- The fact table is **partitioned by the join key** (Hive-style partition directory or a Delta/Iceberg partition column). DPP prunes partitions, not files within a partition.
- The dimension side has a selective filter.
- With `spark.sql.optimizer.dynamicPartitionPruning.reuseBroadcastOnly=true` (internal, default), DPP applies only when the broadcast exchange of a broadcast hash join can be reused as the pruning filter, so the dimension side must be broadcast.

```properties
spark.sql.optimizer.dynamicPartitionPruning.enabled=true          # default true
spark.sql.optimizer.dynamicPartitionPruning.reuseBroadcastOnly=true          # internal, default true
spark.sql.autoBroadcastJoinThreshold=10MB                          # default; raise so the dim broadcasts, or hint /*+ BROADCAST(dim) */
```

## Confirm
```python
df.explain("formatted")
```
Look for a dynamic pruning expression among the `PartitionFilters` of the fact scan. In the SQL tab, the scan's partitions-read metric drops.

## Why it does not fire
- Fact table not partitioned on the join column, or the join key is wrapped in a function/cast (`CAST(f.date_key AS STRING) = d.key`). Align types in the table design.
- The dimension side is not broadcast (with the default `reuseBroadcastOnly=true`).
- The filter is on the fact side already (static pruning does the work).

## Verify
- [ ] Input size / files read on the fact scan drops by the expected ratio when the dim filter changes.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in SQLConf.scala: dynamicPartitionPruning.enabled (since 3.0.0, default true), reuseBroadcastOnly (internal, default true, DPP only when the broadcast exchange can be reused), autoBroadcastJoinThreshold 10MB. Removed unconfirmed join-type rules, exact explain text and Databricks file pruning.

Method: documentation only; no commands were run.
