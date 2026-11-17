---
id: computing-software.data-engineering.apache-spark.streaming-rate-limiting
name: streaming-rate-limiting
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, structured-streaming, maxoffsetspertrigger, maxfilespertrigger, minoffsetspertrigger, maxbytespertrigger, backlog, rate-limit]
level: practitioner
status: docs-checked
description: "Bound Structured Streaming micro-batch size with maxOffsetsPerTrigger, maxFilesPerTrigger, maxBytesPerTrigger and minOffsetsPerTrigger to survive backlogs and restarts."
sources:
  - https://spark.apache.org/docs/latest/streaming/structured-streaming-kafka-integration.html
  - https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html
  - https://github.com/apache/spark/blob/master/connector/kafka-0-10-sql/src/main/scala/org/apache/spark/sql/kafka010/KafkaMicroBatchStream.scala
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streaming rate limiting

**Goal:** keep each micro-batch a predictable size so a backlog (first start, outage, replay) does not create one giant batch that OOMs or runs for hours.

## Kafka source
```python
(spark.readStream.format("kafka")
  .option("subscribe", "orders")
  .option("startingOffsets", "earliest")
  .option("maxOffsetsPerTrigger", 2_000_000)      # total across all partitions per trigger (default: none)
  .option("minOffsetsPerTrigger", 50_000)         # wait for at least this many...
  .option("maxTriggerDelay", "5m")                 # ...but fire after this long anyway (default 15m)
  .option("minPartitions", 64)                     # desired minimum Spark partitions; splits large Kafka partitions
  .load())
```
- `maxOffsetsPerTrigger` is proportionally split across topicPartitions of different volume.
- `minOffsetsPerTrigger` sets the minimum offsets per trigger; if `maxTriggerDelay` is exceeded a trigger fires even if fewer are available.
- `startingOffsets` applies when a query is started fresh; a restarted query resumes from its checkpoint.

## File source
```python
spark.readStream.schema(schema).format("json") \
    .option("maxFilesPerTrigger", 1000) \
    .load("s3a://landing/events/")
```
`maxFilesPerTrigger` (default: no max) or `maxBytesPerTrigger` limit new files per trigger; only one of the two may be set, and a stream always reads at least one file so it can make progress.

## Trigger.AvailableNow interaction
`trigger(availableNow=True)` processes all data available at start, possibly in multiple micro-batches based on the source options (such as `maxFilesPerTrigger` or `maxBytesPerTrigger` for the file source), then stops. The one-time micro-batch trigger (`once=True`) is deprecated in favour of it.

## Sizing the limit
1. Measure throughput from `query.lastProgress` (`numInputRows`, `processedRowsPerSecond`) at steady state.
2. Pick a limit so a batch fits your latency target and executor memory.
3. Backlog drain time is roughly backlog divided by (limit per batch divided by batch duration). If that is too long, scale compute, not the limit alone.

## Gotchas
- Without a limit, a restart after an outage reads the whole backlog in one trigger.
- Adding, deleting or changing rate limits between restarts is allowed; changes to subscribed topics or files are generally not allowed.
- `failOnDataLoss` (default true) fails the query when data may have been lost (for example topics deleted or offsets out of range); the docs note it can be a false alarm.

## Verify
- [ ] `lastProgress["numInputRows"]` never exceeds the limit; batch durations stable during a replay.
- [ ] The Kafka source's `avgOffsetsBehindLatest` progress metric trends down after an outage.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in the Kafka integration guide: maxOffsetsPerTrigger / minOffsetsPerTrigger / maxTriggerDelay (default 15m) / minPartitions / failOnDataLoss semantics; in the streaming guide: file-source maxFilesPerTrigger / maxBytesPerTrigger, Available-now vs deprecated one-time trigger, rate-limit changes allowed across restarts, topic changes generally not allowed; avgOffsetsBehindLatest exists in KafkaMicroBatchStream.scala. Wrong claim fixed: maxOffsetsPerTrigger is split proportionally by partition volume, not lag. Removed Auto Loader options, the 2-3x sizing rule and the state-blowup claim.

Method: documentation only; no commands were run.
