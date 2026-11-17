---
id: computing-software.data-engineering.apache-spark.streaming-real-time-and-continuous-mode
name: streaming-real-time-and-continuous-mode
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, structured-streaming, spark-real-time-mode, continuous-processing, low-latency-streaming, trigger-continuous]
level: advanced
status: gated
description: "Get sub-second latency from Spark Structured Streaming: legacy continuous trigger limits, the newer real-time mode, and when micro-batch tuning is enough."
sources:
  - https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#continuous-processing
  - https://issues.apache.org/jira/browse/SPARK-52330
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Continuous processing and real-time mode

Micro-batch Structured Streaming typically gives 0.5-several seconds end-to-end latency. Before reaching for special modes, tune micro-batch: `trigger(processingTime="0 seconds")` (as fast as possible), fewer shuffle partitions for small streams, RocksDB state store with changelog checkpointing, and async progress tracking (`asyncProgressTrackingEnabled`, Kafka sink only) to take offset commits off the critical path. (gated: unconfirmed, source is paywalled or blocked)

## Legacy continuous processing (experimental since 2.3)
```python
q = (df.writeStream.format("kafka").option("topic", "out")
     .option("checkpointLocation", ckpt)
     .trigger(continuous="1 second")       # checkpoint interval, not batch interval
     .start())
```
Long-running tasks process records as they arrive (~1 ms latency) with **at-least-once** guarantees. Heavily restricted:
- Only map-like operations: `select`, `filter`, `map`, projections. **No aggregations, joins, dedup, or windows** (except a limited `current_timestamp`).
- Sources: Kafka, rate. Sinks: Kafka, memory, console.
- Needs as many cores as source partitions; tasks never finish, so a failure restarts the query from the last epoch.
- Effectively unmaintained; avoid for new work.

## Real-time mode (newer engines)
Spark is adding a real-time trigger (SPARK-52330, targeted at Spark 4.1; Databricks ships "real-time mode" in DBR 16.4+) that runs stages concurrently and streams shuffle data, supporting stateless and many stateful queries at ~100 ms latency. Check your exact release notes: supported operators, sinks and required cluster settings are still expanding, and it needs enough task slots for all stages at once.

## Choosing
| Need | Use |
|---|---|
| seconds latency, any query | micro-batch, tuned |
| 100s of ms with state | real-time mode if your version supports the operators, otherwise Flink |
| ms latency, stateless | Kafka Streams or Flink are better-supported than legacy continuous |

## Verify
- [ ] Measure end-to-end latency with event timestamps in the output vs produce time, at p99, under load.
- [ ] Kill an executor mid-stream and confirm the guarantee you need (duplicates are possible in continuous mode).

## Checked

2026-11-02

- Confirmed: Spark issue SPARK-52330 page was fetched.
- Removed or gated: The structured streaming guide continuous-processing page returned no usable text; the trigger syntax, asyncProgressTrackingEnabled and the 100 ms figure are gated, confirm in the Structured Streaming Programming Guide.

Method: documentation only; no commands were run.
