---
id: computing-software.data-engineering.apache-flink.kinesis-and-pulsar-connectors
name: kinesis-and-pulsar-connectors
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-kinesis, kinesis, pulsar, flink-pulsar-connector, efo, aws]
level: practitioner
status: docs-checked
description: "Read from and write to Amazon Kinesis and Apache Pulsar with Flink: new source APIs, EFO vs polling, shard/topic discovery, watermarks, and starting positions."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/kinesis/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/pulsar/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kinesis and Pulsar connectors

## Kinesis (flink-connector-aws-kinesis-streams)
`KinesisStreamsSource` replaces the deprecated legacy `FlinkKinesisConsumer`. There is no state compatibility between them: start the new source from `AT_TIMESTAMP` slightly before the old one stopped (some records may be reprocessed).
```java
Configuration cfg = new Configuration();
cfg.set(KinesisSourceConfigOptions.STREAM_INITIAL_POSITION, KinesisSourceConfigOptions.InitialPosition.TRIM_HORIZON);
cfg.set(KinesisSourceConfigOptions.READER_TYPE, KinesisSourceConfigOptions.ReaderType.EFO);
cfg.set(KinesisSourceConfigOptions.EFO_CONSUMER_NAME, "orders-agg");
KinesisStreamsSource<Event> src = KinesisStreamsSource.<Event>builder()
    .setStreamArn("arn:aws:kinesis:<REGION>:<ACCOUNT_ID>:stream/orders")
    .setSourceConfig(cfg)
    .setDeserializationSchema(new EventSchema())
    .build();
env.fromSource(src, watermarkStrategy, "kinesis-orders");
```
- **Polling** is the default `READER_TYPE`: all concurrent consumers share one read quota per shard. **EFO** (enhanced fan-out) needs `READER_TYPE` = `EFO` and an `EFO_CONSUMER_NAME`; each consumer gets a dedicated read quota per shard, at additional cost. Consumer names must be unique per stream; reusing one terminates existing subscriptions.
- The source reads records in order per partition key through resharding: it checks that a shard's parents (up to 2) are completely read before reading the shard.
- The default start is LATEST (`STREAM_INITIAL_POSITION` is optional). On restore from a checkpoint or savepoint the configured position is ignored.
- If source parallelism exceeds the shard count, some subtasks read nothing: set `withIdleness` on the watermark strategy or watermark generation blocks.
- Sink: `KinesisStreamsSink`, with optional `setMaxBatchSize`, `setMaxInFlightRequests` and `setMaxBatchSizeInBytes`.
- Auth: the default credentials provider `AUTO` searches ENV_VARS, SYS_PROPS, WEB_IDENTITY_TOKEN, PROFILE and the EC2/ECS provider, in that order.

## Pulsar (flink-connector-pulsar)
```java
PulsarSource<String> src = PulsarSource.builder()
    .setServiceUrl("pulsar://pulsar:6650").setAdminUrl("http://pulsar:8080")
    .setTopics("persistent://public/default/orders")
    .setSubscriptionName("flink-orders")
    .setStartCursor(StartCursor.earliest())
    .setDeserializationSchema(new SimpleStringSchema())
    .build();
```
- The default subscription type is Exclusive (cumulative acknowledgment). The source acknowledges messages when checkpoints complete.
- `pulsar.client.enableTransaction` (default false) starts the transaction coordinator client. If checkpointing or transactions are disabled, set `pulsar.source.enableAutoAcknowledgeMessage` to true.
- Topic patterns: `setTopicPattern("topic-.*")` covers topics under one tenant and namespace; use `RegexSubscriptionMode` to limit it to persistent or non-persistent topics.

## Verify
- [ ] Restore from checkpoint resumes at the right shard/cursor positions without gaps.
- [ ] Pulsar subscription backlog is stable at steady state.

## Checked

2026-10-31. Confirmed against the Flink stable Kinesis and Pulsar DataStream connector pages: deprecated `FlinkKinesisConsumer` and no state compatibility, `READER_TYPE` default POLLING, EFO options and cost note, shard parent ordering, LATEST default and restore behaviour, idleness note, sink builder options, credential provider order, Pulsar Exclusive default, acknowledge-on-checkpoint, transaction and auto-acknowledge options, topic pattern behaviour. Removed: per-shard MB/s and read-rate figures, version gates, sink delivery guarantee claims, `ProvisionedThroughputExceeded` advice, Key_Shared/Failover notes, `DeliveryGuarantee.EXACTLY_ONCE` claim, partition-discovery option, Kinesis lag metric name.

Method: documentation only; no commands were run.
