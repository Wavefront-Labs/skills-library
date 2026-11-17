---
id: computing-software.data-engineering.apache-spark.streaming-deduplication
name: streaming-deduplication
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, structured-streaming, streaming-deduplication, dropduplicateswithinwatermark, dropduplicates, idempotent-sink, merge-into, foreachbatch, exactly-once, deduplication]
level: advanced
status: docs-checked
description: "Deduplicate streams in Spark: dropDuplicatesWithinWatermark, dropDuplicates with event time, bounded state, and idempotent MERGE in foreachBatch as the durable backstop."
sources:
  - https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html
  - https://docs.delta.io/latest/delta-update.html#data-deduplication-when-writing-into-delta-tables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deduplication in Structured Streaming

**Goal:** remove duplicates caused by at-least-once producers, retries and replays without unbounded state.

## Option 1: dropDuplicatesWithinWatermark
```python
deduped = (events
           .withWatermark("event_ts", "2 hours")
           .dropDuplicatesWithinWatermark(["event_id"]))
```
The Structured Streaming guide describes `dropDuplicatesWithinWatermark` for the case where the event-time column cannot be part of the unique identifier: duplicates are dropped within the watermark delay even when their event times differ.

## Option 2: dropDuplicates with event time in the key
```python
deduped = (events.withWatermark("event_ts", "2 hours")
           .dropDuplicates(["event_id", "event_ts"]))
```
The guide shows `dropDuplicates` on the id plus the event-time column with a watermark; with the event time in the key, duplicates must share the same event time.

## Option 3: idempotent sink (always add this for durability)
State-based dedupe forgets after the delay and is lost if you reset the checkpoint. Make the sink itself idempotent:
```python
def upsert(batch_df, batch_id):
    batch_df = batch_df.dropDuplicates(["event_id"])          # dedupe within the micro-batch
    batch_df.createOrReplaceTempView("updates")
    batch_df.sparkSession.sql("""
      MERGE INTO silver.events t
      USING updates s ON t.event_id = s.event_id
        AND t.event_date >= current_date() - INTERVAL 3 DAYS    -- prune target scan
      WHEN NOT MATCHED THEN INSERT *""")

(deduped.writeStream.foreachBatch(upsert)
   .option("checkpointLocation", "s3://ckpt/events_silver/").start())
```
The Delta docs' deduplication section uses an insert-only MERGE for this. The partition predicate keeps the merge from scanning the whole table; pick a window wider than realistic duplicate spread.

## Choosing the delay
Measure how far apart duplicates arrive (producer retry timeouts, upstream replay windows). A larger delay means more state; the guide documents a RocksDB state store provider for large state.

## Gotchas
- Dedupe keys must be stable upstream identifiers, not ingestion UUIDs generated per attempt.
- `foreachBatch` can re-run a batch after failure (same `batch_id`); the MERGE makes it harmless.

## Verify
- [ ] Inject the same event twice (minutes apart) into a test topic: one row in the sink.
- [ ] State rows (`numRowsTotal` for the dedupe operator) plateau.
- [ ] `SELECT event_id, count(*) ... HAVING count(*) > 1` on the sink returns nothing.

## Checked

2026-10-28. Confirmed against: Structured Streaming guide (dropDuplicates with and without watermark, dropDuplicatesWithinWatermark, RocksDB state store provider, foreachBatch, stateOperators numRowsTotal), Delta update page (deduplication when writing). Removed (not confirmable in the fetched pages): 3.5+ gate, first-occurrence and state-expiry details, unbounded-state claim, 1-24 hour range, RocksDB provider class name, new-checkpoint claim.

Method: documentation only; no commands were run.
