---
id: computing-software.data-engineering.streaming-architecture.streaming-into-lakehouse-tables
name: streaming-into-lakehouse-tables
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, streaming-ingestion-lakehouse, kafka-to-iceberg, kafka-to-delta, small-file-problem, commit-interval, compaction, upserts]
level: advanced
status: draft
description: "Land Kafka streams into Iceberg or Delta tables: tool choice (Spark, Flink, Kafka Connect sinks), commit intervals vs small files, upserts/CDC, compaction and exactly-once."
sources:
  - https://iceberg.apache.org/docs/latest/flink-writes/
  - https://docs.delta.io/latest/delta-streaming.html
  - https://iceberg.apache.org/docs/latest/kafka-connect/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Streaming into lakehouse tables

**Goal:** near-real-time tables in Iceberg/Delta fed from Kafka, without drowning in small files or duplicates.

## Tool options
| Tool | Strengths | Notes |
|---|---|---|
| Spark Structured Streaming | Delta and Iceberg sinks, `foreachBatch` MERGE for upserts | micro-batch latency (seconds-minutes) |
| Flink | Iceberg sink with exactly-once via checkpoints, upsert mode, Paimon | lowest latency; commits per checkpoint |
| Kafka Connect Iceberg sink (Apache Iceberg) | no stream processor to run, multi-table routing | exactly-once via coordinator; limited transforms |
| Managed (Confluent Tableflow, Snowpipe Streaming to Iceberg, Databricks streaming tables, Firehose to Iceberg) | least ops | vendor-specific |

## Commit interval vs file size
Every commit creates at least one file per written partition per writer task. A 10-second commit with 50 tasks and 20 partitions = up to 1000 files per commit.
- Commit every 1-5 minutes unless latency demands less.
- Reduce writers per partition: `distribution-mode=hash` (Iceberg Flink/Spark `write.distribution-mode=hash`) so each partition is written by one task.
- Partition coarsely (day, not minute); use clustering/sort for finer pruning.
- Schedule **compaction** (Iceberg `rewrite_data_files`, Delta `OPTIMIZE` / auto-compaction / predictive optimization) and snapshot expiry.

## Exactly-once
- Flink Iceberg sink: files committed on checkpoint completion; replays after failure do not duplicate.
- Spark: checkpoint + idempotent table commits (Delta `txnAppId`/`txnVersion` inside foreachBatch, or MERGE).
- Connect Iceberg sink: central coordinator commits offsets with table snapshots.

## Upserts / CDC
```python
def upsert(batch_df, batch_id):
    latest = batch_df.withColumn("rn", F.row_number().over(
        Window.partitionBy("id").orderBy(F.col("source_ts").desc()))).filter("rn = 1").drop("rn")
    (DeltaTable.forName(spark, "silver.customers").alias("t")
       .merge(latest.alias("s"), "t.id = s.id")
       .whenMatchedDelete(condition="s.op = 'd'")
       .whenMatchedUpdateAll(condition="s.source_ts > t.source_ts")
       .whenNotMatchedInsertAll(condition="s.op != 'd'")
       .execute())
stream.writeStream.foreachBatch(upsert).option("checkpointLocation", chk).start()
```
Iceberg: Flink upsert mode (`'write.upsert.enabled'='true'` with identifier fields) writes equality deletes; merge-on-read requires regular compaction to keep reads fast.

## Gotchas
- High-frequency MERGE on large tables: each merge rewrites touched files; use deletion vectors (Delta) / merge-on-read (Iceberg) and partition-pruning predicates.
- Schema evolution from Kafka: decide whether new fields auto-add (mergeSchema / Iceberg schema evolution in sink config).
- Readers of near-real-time tables: snapshot count grows quickly; expire snapshots, keep metadata small.

## Verify
- [ ] Average file size per partition after compaction within 128-512 MB target; files per commit bounded.
- [ ] Kill/restart test produces no duplicates (count by key vs source).
