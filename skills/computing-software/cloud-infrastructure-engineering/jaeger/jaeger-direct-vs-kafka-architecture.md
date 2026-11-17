---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-direct-vs-kafka-architecture
name: jaeger-direct-vs-kafka-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, direct-to-storage, kafka-buffer, ingester, spike-handling]
level: practitioner
status: docs-checked
description: "Compare direct-to-storage Jaeger with a Kafka buffer between collectors and ingesters, including data-loss tradeoffs."
sources:
  - https://www.jaegertracing.io/docs/2.22/architecture/
  - https://www.jaegertracing.io/docs/2.22/faq/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose how spans get from collectors to storage.

Direct to storage: collectors receive data and write it directly. The storage must handle average and peak traffic. Collectors may use an in-memory queue to smooth short peaks, but a sustained spike can drop data if the storage cannot keep up.

Via Kafka: to prevent data loss between collectors and storage, Kafka acts as an intermediary persistent queue. Collectors are configured with Kafka exporters, and an additional component, the ingester, reads from Kafka and saves to storage. An ingester is very similar to a collector, only configured with a Kafka receiver instead of RPC-based receivers. Multiple ingesters scale up ingestion and automatically partition the load among themselves.

Failure mode: Jaeger drops data when storage is too slow; adding collectors gives only small, temporary relief and does not remove the storage bottleneck.

## Checked

2026-11-08: read the whole Architecture page and the FAQ (raw markdown from the jaegertracing/documentation repo, v2/2.22). Confirmed both deployment options and the collector scaling caveat. Removed unsupported claims: the performance guide remarks and the trace-ID Kafka sharding and idle-ingester details.

Method: documentation only; no commands were run.
