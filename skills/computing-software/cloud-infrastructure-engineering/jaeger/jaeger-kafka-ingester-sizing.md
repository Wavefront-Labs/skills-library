---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-kafka-ingester-sizing
name: jaeger-kafka-ingester-sizing
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, ingester-sizing, partitions, max-fetch-size, bulk-processing-max-bytes]
level: sme
status: docs-checked
description: "Size ingester batches by adding partitions, not fetch settings, and keep queue.batch.max_size below bulk max_bytes."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/kafka/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get large storage writes from the Kafka ingester.

With `wait_for_result` set, batch size is bounded by the number of partitions the ingester consumes. The receiver processes each partition serially and partitions concurrently, so at most one record per partition waits in the exporter's batcher at a time. A topic with few partitions yields small storage writes. Add partitions to increase write throughput; raising `queue.batch.max_size` alone does not help.

Adding ingester replicas adds processing capacity, up to one replica per partition, but does not enlarge batches: replicas share the same partitions, so each owns fewer and produces smaller batches.

The receiver's fetch settings (`max_fetch_size`, `max_partition_fetch_size`, `min_fetch_size`, `max_fetch_wait`) control bytes returned per fetch and wait time, not how many records reach the exporter at once. The receiver makes one pipeline call per fetched record, so a larger fetch only fills the receiver's buffer.

Elasticsearch and OpenSearch: keep `queue.batch.max_size` well below `bulk_processing.max_bytes`. The collector measures batches in OTLP protobuf bytes while the storage measures the encoded `_bulk` body, which is larger, so a batch at the limit is split across several `_bulk` requests. Both must stay below Elasticsearch's `http.max_content_length`, 100 MB by default.

## Checked

2026-11-03. Confirmed against the Kafka page, Sizing section: batch size bounded by partitions, serial per-partition processing, replicas not enlarging batches, the fetch settings listed, the max_size versus bulk_processing.max_bytes guidance and the 100 MB http.max_content_length default. Nothing removed.
Method: documentation only; no commands were run.
