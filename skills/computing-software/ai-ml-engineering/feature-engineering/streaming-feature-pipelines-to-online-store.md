---
id: computing-software.ai-ml-engineering.feature-engineering.streaming-feature-pipelines-to-online-store
name: streaming-feature-pipelines-to-online-store
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, streaming-features, online-feature-store, flink, kafka, feast-push, windowed-aggregations]
level: practitioner
status: draft
description: "Compute fresh features from event streams into an online store: windowed aggregations in Flink or Spark Structured Streaming, push APIs, late events and backfill consistency."
sources:
  - https://docs.feast.dev/reference/data-sources/push
  - https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Streaming feature pipelines to the online store

Batch features refreshed nightly are up to a day stale. Fraud, recommendations and dynamic pricing need features like "transactions in the last 10 minutes", updated within seconds.

## Architecture
events (Kafka/Kinesis) -> stream processor (Flink, Spark Structured Streaming, Kafka Streams, managed: Tecton/Databricks/Feast push) -> online store (Redis, DynamoDB, Bigtable) for serving + offline store (warehouse/lake) for training.

## Windowed aggregation (Flink SQL)
```sql
INSERT INTO card_features_sink
SELECT card_id, window_end AS event_ts,
       COUNT(*) AS txn_count_10m, SUM(amount) AS txn_sum_10m, MAX(amount) AS txn_max_10m
FROM TABLE(HOP(TABLE transactions, DESCRIPTOR(event_time), INTERVAL '1' MINUTE, INTERVAL '10' MINUTE))
GROUP BY card_id, window_start, window_end;
```
- Sliding (hop) windows give fresh values every slide; tumbling windows are cheaper but stale up to the window size.
- Use **event time** with watermarks (`WATERMARK FOR event_time AS event_time - INTERVAL '30' SECOND`) so late events land in the right window; decide what to do with events later than the watermark (drop, side output, correct).

## Spark Structured Streaming
```python
agg = (events.withWatermark("event_time", "30 seconds")
       .groupBy("card_id", F.window("event_time", "10 minutes", "1 minute"))
       .agg(F.count("*").alias("txn_count_10m"), F.sum("amount").alias("txn_sum_10m")))
agg.writeStream.foreachBatch(write_to_online_store).outputMode("update").start()
```

## Pushing into Feast
```python
from feast import FeatureStore
store = FeatureStore(".")
store.push("card_txn_push_source", df_batch, to=PushMode.ONLINE_AND_OFFLINE)
```
The `PushSource` is attached to a feature view; `ONLINE_AND_OFFLINE` also logs values for training.

## Training-serving consistency
- The same aggregation must be computable over history for training (backfill). Options: run the streaming job over historical events (Kappa), write a batch equivalent with identical window semantics, or log streamed values to the offline store and train on those logs.
- Point-in-time joins on the offline store use the feature `event_ts` (window end), not processing time.
- Validate: for a sample of entities, compare online values with the batch recomputation for the same timestamp.

## Operational concerns
- Freshness SLO and monitoring: lag between event time and online-store write time.
- Exactly-once vs at-least-once: duplicates inflate counts; dedupe by event id or use idempotent upserts.
- Hot keys (a merchant with millions of events) need pre-aggregation or key salting.
- TTL on online features so inactive entities do not serve ancient values.

## When not to stream
If the model's accuracy barely changes with daily vs minute-level freshness (test offline by simulating staleness), batch is simpler and cheaper.
