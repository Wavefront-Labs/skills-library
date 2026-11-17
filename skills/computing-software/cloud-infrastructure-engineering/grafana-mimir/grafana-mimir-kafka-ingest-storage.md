---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-kafka-ingest-storage
name: grafana-mimir-kafka-ingest-storage
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [ingest-storage, kafka, partitions, architecture, message-size]
level: sme
status: docs-checked
description: "Covers enabling the Mimir ingest storage architecture with a Kafka backend: required flags, recommended settings and Apache Kafka record size limits."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-kafka-backend/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kafka backend for ingest storage

From Mimir 3.0 ingest storage is the preferred and stable architecture. It uses Kafka as the first ingestion layer, decoupling the write and read paths.

## Required flags (all Mimir components)

- `-ingest-storage.enabled=true`
- `-ingest-storage.kafka.address=<host:port>[,<host:port>...]`: seed brokers (list several for bootstrap availability).
- `-ingest-storage.kafka.topic=<name>`
- `-ingest-storage.kafka.auto-create-topic-default-partitions=<number>`: partitions to create if the topic is missing; it must be at least the number of ingesters in one zone.

Recommended: `-distributor.remote-timeout=5s`, because pushing to Kafka-compatible backends can be slower than writing directly to ingesters.

## Backend-specific settings

Kafka implementations differ in API behaviour. For Apache Kafka, set the broker `message.max.bytes=16000000`. Mimir's default `-ingest-storage.kafka.producer-max-record-size-bytes` is about 15.2 MB while Kafka's default is 1 MB, so otherwise Kafka rejects larger records. Topic-level alternative:

```bash
bin/kafka-configs.sh --bootstrap-server <host:port> \
  --alter --entity-type topics --entity-name <topic-name> \
  --add-config max.message.bytes=16000000
```

The page gives the same `message.max.bytes` setting for Confluent Kafka, and for WarpStream the flag `-ingest-storage.kafka.use-compressed-bytes-as-fetch-max-bytes=false`.

## Checked

2026-11-04. Confirmed against the Mimir page "Configure the Grafana Mimir Kafka backend": required flags, partition-count rule, `-distributor.remote-timeout=5s`, the Apache Kafka record size settings and the topic-level command. Removed the "Operational effects" section (not on the page).
Method: documentation only; no commands were run.
