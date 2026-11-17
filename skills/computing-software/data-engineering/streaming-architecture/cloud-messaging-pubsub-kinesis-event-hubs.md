---
id: computing-software.data-engineering.streaming-architecture.cloud-messaging-pubsub-kinesis-event-hubs
name: cloud-messaging-pubsub-kinesis-event-hubs
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, pubsub, google-pubsub, kinesis, amazon-kinesis-data-streams, azure-event-hubs, managed-kafka, shards, partitions, ordering-keys]
level: practitioner
status: draft
description: "Compare Google Pub/Sub, Amazon Kinesis Data Streams, Azure Event Hubs and managed Kafka: scaling units, ordering, retention, replay, delivery semantics, limits and cost drivers."
sources:
  - https://cloud.google.com/pubsub/docs/overview
  - https://cloud.google.com/pubsub/docs/ordering
  - https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html
  - https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html
  - https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-features
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud messaging: Pub/Sub vs Kinesis vs Event Hubs

**Goal:** pick and size the managed event stream on your cloud knowing exactly how it orders, scales, retains and charges.

## 1. Model comparison
| | Google Pub/Sub | Kinesis Data Streams | Azure Event Hubs | Managed Kafka (MSK, Confluent, Event Hubs Kafka API) |
|---|---|---|---|---|
| Model | topics + subscriptions; per-message ack | shards (ordered log) | partitions (ordered log) + consumer groups | partitions (ordered log) |
| Scaling unit | none visible (auto) | shard: 1 MB/s or 1,000 rec/s in, 2 MB/s out | throughput/processing units; partitions fixed at creation in some tiers | partitions + brokers |
| Ordering | only with **ordering keys** enabled on subscription | per shard (partition key → shard) | per partition (partition key) | per partition |
| Retention / replay | ack'd messages kept per subscription retention (up to 7 days; topic retention up to 31 days) + seek to timestamp/snapshot | 24 h default, up to 365 days | 1-7 days (standard), up to 90 days (premium/dedicated) | configurable, tiered storage |
| Delivery | at-least-once; exactly-once delivery option for pull subscriptions in a region | at-least-once | at-least-once | at-least-once; EOS with transactions |
| Consumers | push or pull subscriptions, each subscription gets every message | shared throughput or enhanced fan-out (dedicated 2 MB/s per consumer per shard) | consumer groups with checkpointing (blob store) | consumer groups, offsets in Kafka |

## 2. Sizing
- Kinesis: shards = max(in MB/s ÷ 1, in records/s ÷ 1000, out MB/s ÷ 2 per consumer without fan-out). On-demand capacity mode removes sizing at a price premium.
- Event Hubs: partition count limits consumer parallelism — choose for peak consumers (can't easily reduce); throughput units cap ingress/egress.
- Pub/Sub: no partitions to size; watch per-region quotas and subscriber flow control; ordering keys limit throughput per key (~1 MB/s).

## 3. Integration with data platforms
- Pub/Sub → BigQuery subscriptions (direct write), Cloud Storage subscriptions, Dataflow.
- Kinesis → Firehose (S3, Redshift, Snowflake, Iceberg), Lambda, Managed Flink, Spark/Databricks connector.
- Event Hubs → Capture (Avro/Parquet to ADLS), Stream Analytics, Fabric eventstreams; Kafka protocol endpoint lets Kafka clients and Kafka Connect work unchanged.

## 4. Choosing
- Single-cloud, simple fan-out, minimal ops → the native service.
- Need Kafka ecosystem (Connect, Streams, Schema Registry, exactly-once transactions), long retention, multi-cloud portability → managed Kafka.
- Strict per-entity ordering at high volume → log-based (Kinesis/Event Hubs/Kafka) with good partition keys; Pub/Sub ordering keys for modest per-key rates.

## 5. Cost drivers
Pub/Sub: data volume (throughput) and retention storage. Kinesis: shard-hours (provisioned) or data in/out (on-demand), extended retention, enhanced fan-out. Event Hubs: TUs/PUs/CUs per hour plus capture. Kafka: brokers/storage or cluster units. Model peak and average; idle provisioned capacity is the usual waste.

## Verify
- [ ] Capacity math documented for peak with ≥30% headroom.
- [ ] Ordering requirement mapped to the right key mechanism and tested.
- [ ] Retention ≥ maximum consumer outage + reprocessing window.
- [ ] Consumer lag / iterator age alerts exist (`GetRecords.IteratorAgeMilliseconds`, `subscription/oldest_unacked_message_age`, Event Hubs consumer lag).
