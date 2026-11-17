---
id: computing-software.data-engineering.apache-spark.shuffle-and-skew-tuning
name: shuffle-and-skew-tuning
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, pyspark, spark-sql, shuffle, data-skew, skew-join, adaptive-query-execution, aqe, spark-sql-shuffle-partitions, broadcast-join, autobroadcastjointhreshold, salting, repartition, coalesce, spark-ui, stragglers, partition-sizing, spill, databricks, emr, dataproc, performance-tuning]
level: advanced
status: docs-checked
description: "Diagnose and fix slow Spark shuffles: size partitions, use AQE coalesce and skew-join handling, broadcast small tables, salt hot keys, and read stragglers in the Spark UI."
sources:
  - https://spark.apache.org/docs/latest/sql-performance-tuning.html#adaptive-query-execution
  - https://spark.apache.org/docs/latest/sql-performance-tuning.html#optimizing-skew-join
  - https://spark.apache.org/docs/latest/web-ui.html
  - https://github.com/apache/spark/blob/master/sql/catalyst/src/main/scala/org/apache/spark/sql/internal/SQLConf.scala
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spark shuffle and skew tuning — make the slow stage fast

**Goal:** find the stage that dominates runtime, decide whether it is under-partitioned, over-partitioned or skewed, and apply the smallest config or code change that fixes it.

## 1. Read the Spark UI before touching config
1. **Jobs → Stages**, sort by Duration. The slow stage is almost always one that reads or writes shuffle data (`Shuffle Read` / `Shuffle Write` columns).
2. Open it and look at **Summary Metrics for Completed Tasks**. Compare *Max* with *75th percentile* for Duration and Shuffle Read Size. A Max far above the median means **skew**; all tasks uniformly slow with huge sizes means **too few partitions**; thousands of tasks finishing in milliseconds means **too many**.
3. Check **Spill (Memory)/Spill (Disk)** — spill means partitions are too large for executor memory.
4. On the **SQL / DataFrame** tab, open the query plan: look for `SortMergeJoin` vs `BroadcastHashJoin`, `Exchange` nodes (shuffles), and `AQEShuffleRead` nodes (proof AQE acted).

## 2. Size shuffle partitions
- `spark.sql.shuffle.partitions` defaults to **200** regardless of data size. Size partitions from the observed shuffle bytes per task; the AQE advisory size (default 64 MB) is the documented target when coalescing.
- With AQE on (`spark.sql.adaptive.enabled` defaults to true), set a generous starting value and let it coalesce:
```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.advisoryPartitionSizeInBytes", "128m")  # default 64MB (falls back to the older targetPostShuffleInputSize)
spark.conf.set("spark.sql.shuffle.partitions", "2000")  # upper bound AQE coalesces down
```
- Input-side partitioning for file scans is governed separately by `spark.sql.files.maxPartitionBytes` (default 128 MB).

## 3. Avoid the shuffle: broadcast joins
- `spark.sql.autoBroadcastJoinThreshold` defaults to **10 MB** (estimated size; `-1` disables). Spark can only broadcast automatically when it has a size estimate under the threshold; otherwise force it with the `broadcast` hint:
```python
from pyspark.sql.functions import broadcast
facts.join(broadcast(dim_country), "country_id")
```
- **Gotcha:** the in-memory size of a table can far exceed its on-disk (for example Parquet) size, so broadcasting a large table can exhaust driver or executor memory. Keep forced broadcasts small and watch driver memory.
- AQE can convert a sort-merge join to broadcast at runtime once it sees real sizes.

## 4. Fix skew
**AQE skew join (try first):**
```text
spark.sql.adaptive.skewJoin.enabled=true                         # default true
spark.sql.adaptive.skewJoin.skewedPartitionFactor=5               # x median
spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes=256MB
```
A partition is treated as skewed only if it exceeds *both* factor × median partition size and the byte threshold (set the threshold larger than the advisory size). It handles skew in shuffled joins (sort-merge and shuffled hash); it does not cover aggregations or windows.

**Salting (when AQE can't help, e.g. skewed `groupBy`):**
```python
from pyspark.sql import functions as F
N = 16
salted = df.withColumn("salt", (F.rand() * N).cast("int"))
partial = salted.groupBy("key", "salt").agg(F.sum("amt").alias("amt"))
result = partial.groupBy("key").agg(F.sum("amt").alias("amt"))
```
For a skewed join, salt the big side randomly and explode the small side across all N salt values (`F.explode(F.array([F.lit(i) for i in range(N)]))`), then join on (key, salt). Salting only works for re-aggregatable operations (sum, count, max), not exact distinct counts without a second pass.

**Also check:** null or sentinel keys (`''`, `-1`, `'UNKNOWN'`) — a frequent source of one giant partition. Filter them out and handle separately.

## 5. repartition vs coalesce
- `repartition(n)` or `repartition("col")` triggers a full shuffle and produces evenly sized partitions — use before a heavy wide operation or to balance output files.
- `coalesce(n)` merges partitions **without** a shuffle — cheap, but it can collapse upstream parallelism too: `df.filter(...).coalesce(1)` may run the entire filter on one task. Use `repartition` when the upstream work is expensive.
- For writes, `df.repartition("date")` before `partitionBy("date")` prevents thousands of tiny files per partition.

## 6. Gotchas
- Caching a skewed DataFrame caches the skew.
- UDFs and `collect()` hide work from the UI's SQL plan; Python UDFs add serialization cost on top of shuffle.

## Verify
- [ ] The slow stage's max task duration is close to the median after the change.
- [ ] Query plan shows `BroadcastHashJoin` for small dimension joins, or `AQEShuffleRead` with skew/coalesced partitions.
- [ ] Spill (Disk) for the stage is zero or sharply reduced.
- [ ] Output files are not thousands of tiny files.
- [ ] Wall-clock time of the job is measured before and after, on the same input size.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in SQLConf.scala: spark.sql.shuffle.partitions 200, adaptive.enabled true, advisoryPartitionSizeInBytes falls back to the deprecated targetPostShuffleInputSize (64MB), autoBroadcastJoinThreshold 10MB (-1 disables), files.maxPartitionBytes 128MB, skewJoin.enabled true, skewedPartitionFactor 5.0, skewedPartitionThresholdInBytes 256MB and the both-conditions rule; skew join covers sort-merge and shuffled hash joins. Removed unsourced rules of thumb (100-200 MB per partition, 3-10x in-memory expansion, 5-10x skew ratio, output file sizes) and a Databricks cross-link.

Method: documentation only; no commands were run.
