---
id: computing-software.cloud-infrastructure-engineering.observability.kafka-buffering-between-collector-tiers
name: kafka-buffering-between-collector-tiers
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [kafka-buffering, collector-kafka-pipeline, collector-deployment, otel-collector, kafka]
level: advanced
status: docs-checked
description: "Put Kafka between collector tiers: kafka exporter and receiver config, encodings, partitions and consumer groups, offset handling, lag monitoring and replay."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/kafkareceiver", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/kafkaexporter", "https://opentelemetry.io/docs/collector/deployment/gateway/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka buffering between collector tiers

## Why
A durable buffer absorbs spikes and backend outages (bounded by Kafka retention rather than an in-memory queue), decouples
teams, and lets you replay or fan out to several consumers (e.g. Tempo and a data lake).

## Topology
apps -> agent collectors -> **kafka exporter** -> topics (`otlp_spans`, `otlp_metrics`, `otlp_logs`) ->
**kafka receiver** in consumer collectors -> processors (sampling, transform) -> backends.

## Producer side
```yaml
exporters:
  kafka:
    brokers: [kafka-0:9092, kafka-1:9092, kafka-2:9092]
    traces: {topic: otlp_spans, encoding: otlp_proto}
    partition_traces_by_id: true
    producer: {compression: zstd, required_acks: -1, max_message_bytes: 4000000}
    sending_queue: {enabled: true, queue_size: 10000}
    retry_on_failure: {enabled: true, max_elapsed_time: 10m}
```

## Consumer side
```yaml
receivers:
  kafka:
    brokers: [kafka-0:9092, kafka-1:9092, kafka-2:9092]
    traces: {topics: [otlp_spans], encoding: otlp_proto}
    group_id: otel-tempo-writer
    initial_offset: latest            # earliest to replay from retention
    autocommit: {enable: true, interval: 1s}
    message_marking: {after: true, on_error: false}   # commit only after successful pipeline
```
(The receiver takes a `topics` list per signal; the exporter takes a single `topic`. Older collector versions used top-level `topic`/`encoding`.) Consumers in the same `group_id` share partitions;
max useful consumers = partition count. Size partitions for peak throughput.

## Operations
- Lag: monitor consumer-group lag per group with a Kafka-side exporter; alert when lag age exceeds tolerance.
- Kafka retention is your outage budget.
- Message size: batch before Kafka, but keep messages under the producer `max_message_bytes` (default 1000000, before compression) and the broker limit.
- Replay: start a new consumer group with `initial_offset: earliest` (it applies only when no offset was committed).

## Gotchas
- A permanently failing backend with `message_marking.after: true` leaves messages unmarked and they are reprocessed after a rebalance; see `message_marking.on_error`, `on_permanent_error` and `error_backoff` in the receiver README.
- PII redaction must happen before Kafka (data at rest).
- Producer and consumer must use the same `encoding`.

## Checked
Checked 2026-10-28 against the kafkareceiver and kafkaexporter READMEs (collector-contrib main, v0.15x era; deprecations cite v0.123 and v0.154).
- Confirmed: exporter `brokers`, per-signal `topic` and `encoding` (default `otlp_proto`), `partition_traces_by_id` (default false), `producer`-level `compression` (none, gzip, snappy, lz4, zstd), `required_acks`, `max_message_bytes` (default 1000000, measured before compression), `sending_queue`, `retry_on_failure`; receiver `group_id`, `initial_offset` (latest or earliest, default latest), `autocommit`, `message_marking` with `after` and `on_error`.
- Fixed: receiver uses `topics` (list, default `otlp_spans`) per signal, not `topic`.
- Confirmed gotcha: `message_marking.on_error`/`on_permanent_error`, `error_backoff`; unmarked messages reprocess after a rebalance.
- Removed: partition sizing figure, retention figures, the lag metric name, "hours" outage claim, the `kafka-consumer-groups --reset-offsets` command, the broker `max.message.bytes` wording and the "oversized messages fail permanently" claim.

Method: documentation only; no commands were run.
