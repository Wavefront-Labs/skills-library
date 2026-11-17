---
id: computing-software.data-engineering.apache-spark.structured-streaming-checkpointing
name: structured-streaming-checkpointing
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, structured-streaming, checkpointing, watermark, trigger-availablenow, foreachbatch, write-ahead-log, state-store, rocksdb-state-store, micro-batch, continuous-processing, stream-stream-join, checkpoint-recovery]
level: practitioner
status: docs-checked
description: "Operate Spark Structured Streaming checkpoints, triggers and watermarks safely, including recovery and upgrade pitfalls."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html#recovering-from-failures-with-checkpointing
  - https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html#recovery-semantics-after-changes-in-a-streaming-query
  - https://github.com/apache/spark/blob/master/sql/catalyst/src/main/scala/org/apache/spark/sql/internal/SQLConf.scala
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structured Streaming checkpoints, triggers and safe recovery

**Goal:** a streaming job that survives restarts, code upgrades and cluster migrations without reprocessing from scratch or silently dropping state.

## 1. What's actually in the checkpoint directory
A checkpoint location (`checkpointLocation` option) holds: the progress information (the range of offsets processed in each trigger) and the **state store** (aggregation/join state). The default provider is `HDFSBackedStateStoreProvider` (state kept in executor JVM memory, checkpointed to storage); a RocksDB state store provider has been available since Spark 3.2 for large state, and `spark.sql.streaming.stateStore.providerClass` cannot be changed between restarts from the same checkpoint. Losing or corrupting this directory means losing exactly where the stream was — treat it with the same durability expectations as the data itself (replicated storage, not local disk on an ephemeral node).

## 2. Triggers
- **Default (fixed micro-batch)**: runs the next batch immediately after the previous completes.
- **`Trigger.ProcessingTime("1 minute")`**: fixed-interval micro-batches — predictable cadence, the common production choice for cost control.
- **`Trigger.AvailableNow()`**: processes all data available at start, possibly in several micro-batches based on source options, then stops — a scheduled batch-like run. Watermark advances per batch and a no-data batch runs before termination if the last batch advanced the watermark. It falls back to a one-time micro-batch if a source does not support it. The one-time trigger (`Trigger.Once`) is deprecated in its favour.
- **Continuous** (`trigger(continuous="1 second")`): a separate execution mode; `foreachBatch` does not work with it (use `foreach`). See the continuous-mode skill and the guide for supported operations.

## 3. Watermarks and state cleanup
`withWatermark("eventTime", "10 minutes")` lets the engine drop old aggregation and join state. Data less than the delay behind the latest processed event time is guaranteed to be aggregated; older data may or may not be. A longer delay retains more state.
- **Stream-stream joins** need watermark delays on both inputs and an event-time constraint across them (a time-range join condition or a join on event-time windows) so the engine can clear old rows from state.

## 4. Code-change compatibility across restarts
Not every code change is safe to restore from an existing checkpoint:
Per the guide's "Recovery Semantics after Changes" section:
- Any change (addition, deletion or schema modification) to the stateful operations of a query is not allowed between restarts: streaming aggregation (grouping keys or aggregates), `dropDuplicates` columns, stream-stream join schema, equi-join columns and join type, and the state schema and timeout type of `mapGroupsWithState` / `flatMapGroupsWithState`. Plan a new checkpoint and reprocessing for these.
- Changes in the number or type of input sources are not allowed; adding, deleting or changing rate limits is allowed; changes to subscribed topics or files are generally not allowed.
- Adding or deleting filters is allowed; changes in `ForeachWriter` code are allowed but their semantics depend on the code; changing a file sink's output directory is not allowed.

## Verify
- [ ] Checkpoint location is on fault-tolerant storage (the guide cites HDFS, AWS S3 and Azure Blob storage).
- [ ] A kill-and-restart test of the running job resumes from the correct offset with no gap or duplicate in the sink (check against an idempotent sink write, see computing-software.data-engineering.etl-pipeline-design.idempotent-incremental-loads).
- [ ] Watermark delay was chosen against measured late-arrival data.
- [ ] Any change to a stateful operation went through a planned checkpoint reset, not a silent restart.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in the streaming guide and SQLConf.scala: checkpoint stores progress and running aggregates, stateStore.providerClass default HDFSBackedStateStoreProvider and not changeable across restarts, RocksDB provider added in 3.2, Available-now and deprecated one-time trigger semantics, foreachBatch unsupported in continuous mode, the full recovery-semantics rules for stateful operations, sources, sinks and filters, the watermark guarantee, stream-stream join watermark and time-constraint requirements. Wrong claim fixed: RocksDB is not the default state store provider. Removed the unsourced checkpoint-relocation, shuffle-partition-count and continuous-latency claims; the offset-log and commit-log names were replaced by the documented description.

Method: documentation only; no commands were run.
