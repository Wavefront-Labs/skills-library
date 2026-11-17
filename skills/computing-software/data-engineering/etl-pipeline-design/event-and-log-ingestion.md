---
id: computing-software.data-engineering.etl-pipeline-design.event-and-log-ingestion
name: event-and-log-ingestion
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, source-systems, event-ingestion, clickstream, log-ingestion, kafka-connect, firehose, snowplow, event-collection, schema-validation]
level: practitioner
status: draft
description: "Ingest application events and logs into the lake/warehouse: collection paths, schemas at the edge, buffering, file sizing for sinks, deduplication, PII and late events."
sources:
  - https://docs.snowplow.io/docs/fundamentals/
  - https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html
  - https://docs.confluent.io/kafka-connectors/s3-sink/current/overview.html
  - https://vector.dev/docs/
  - https://opentelemetry.io/docs/collector/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Event and log ingestion

**Goal:** high-volume events (clickstream, app events, server logs, IoT) arrive in the lake/warehouse complete, validated, deduplicated and queryable within the agreed latency.

## 1. Collection paths
| Source | Path |
|---|---|
| Web/mobile product events | tracker SDK → collector (Snowplow, Segment/RudderStack, or own endpoint) → stream |
| Backend domain events | service → Kafka/Kinesis/Pub/Sub (outbox pattern for DB-consistent events) |
| Server/app logs | agent (Vector, Fluent Bit, OTel Collector) → stream or object store |
| IoT | MQTT broker / IoT hub → stream |
Always put a durable buffer (stream or queue) between producers and the warehouse — it absorbs spikes and allows replay.

## 2. Schemas at the edge
- Define events in a schema registry (Avro/Protobuf/JSON Schema) or tracking plan; validate at the collector and route invalid events to a **bad-events** stream with the reason (Snowplow does this natively).
- Required envelope fields: `event_id` (UUID from producer), `event_name`, `event_version`, `occurred_at` (producer clock, UTC), `received_at` (collector), entity ids, source app/version.
- Client clocks lie: keep both `occurred_at` and `received_at`; use `received_at` for partitioning, `occurred_at` for analysis with sanity bounds.

## 3. Land in the lake/warehouse
- Stream → object storage sink (Kafka Connect S3 sink, Firehose, Pub/Sub → GCS subscription) with time-based partitions; or directly into warehouse streaming ingest (Snowpipe Streaming, BigQuery Storage Write API, Databricks/Spark streaming into Delta).
- File sizing: flush by size **and** time (e.g. 128 MB or 5 min). Firehose buffering hints, S3 sink `flush.size`/`rotate.interval.ms`. Tiny files → compact downstream.
- Columnar format (Parquet) for analytics; keep raw JSON only for the bad-events/forensics path.

## 4. Deduplicate
At-least-once delivery means duplicates (SDK retries, consumer restarts). Dedup on `event_id` within a window in silver:
```sql
SELECT * FROM bronze.events
WHERE received_date >= current_date - 2
QUALIFY ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY received_at) = 1;
```
Then MERGE into silver keyed on `event_id` so re-runs are idempotent.

## 5. PII and volume control
- Hash or drop IP addresses, emails and free text at the collector or first hop; enrichments (geo from IP) before dropping the raw value.
- Sampling for very high-volume debug logs; never sample business events.
- Retention per layer: raw events 30-90 days, aggregated forever.

## 6. Late and out-of-order events
Mobile clients send hours/days late (offline). Partition by `received_at`, model by `occurred_at`, and reprocess aggregates for a lookback window (e.g. last 3 days of `occurred_at`) on each run.

## Verify
- [ ] Event volume per event name compared with the source (collector counts) daily.
- [ ] Bad-events stream monitored; spikes alert the owning team.
- [ ] Duplicate rate in silver is 0 on `event_id`.
- [ ] Average sink file size within target.
