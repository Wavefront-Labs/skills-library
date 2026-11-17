---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-kafka-buffer-setup
name: jaeger-kafka-buffer-setup
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, kafka-exporter, kafka-receiver, ingester-config, kafka-topic]
level: practitioner
status: docs-checked
description: "Set up Jaeger collectors exporting to Kafka and ingesters reading it into storage, with the topic created ahead of time."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/kafka/
  - https://www.jaegertracing.io/docs/2.22/faq/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: put Kafka between collectors and storage.

Supported Kafka versions per the Jaeger page: 3.x. Jaeger acts as the collector that exports to a Kafka topic and as the ingester that reads Kafka and writes to a storage backend. Writing to Kafka is also useful for building post-processing data pipelines from the same topic.

Configuration uses the Kafka exporter and receiver from opentelemetry-collector-contrib; see their READMEs for the settings. Sample files in the repository: `config-kafka-collector.yaml` for collectors and `config-kafka-ingester.yaml` for ingesters.

Topic and partitions: unless the Kafka cluster auto-creates topics, create the topic ahead of time (see the Kafka quickstart). With at-least-once settings, batch size and write throughput are bounded by the number of partitions the ingester consumes, and ingester replicas beyond one per partition add nothing.

If the pipeline uses JSON encoding of Protobuf, trace IDs appear base64 encoded (for example fpDA7KInhOx+kMDsoieE7A==) instead of 32-char hex.

## Checked

2026-11-08: read the whole Kafka page and the FAQ (raw markdown from the jaegertracing/documentation repo, v2/2.22). Confirmed supported version, collector and ingester roles, sample files, topic creation and the base64 trace ID note. Removed unsupported claims: trace-ID sharding over partitions, the list of message encodings and the Jaeger-to-Kafka security matrix.

Method: documentation only; no commands were run.
