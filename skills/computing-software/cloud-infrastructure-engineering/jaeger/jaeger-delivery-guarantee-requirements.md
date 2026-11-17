---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-delivery-guarantee-requirements
name: jaeger-delivery-guarantee-requirements
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, delivery-guarantees, batch-processor, wait-for-result, lossless-pipeline]
level: sme
status: docs-checked
description: "Build a lossless Jaeger pipeline: storage that reports failures, no batch processor, and an exporter queue with wait_for_result."
sources:
  - https://www.jaegertracing.io/docs/2.22/deployment/delivery-guarantees/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make sure a storage failure is never hidden from the sender.

The guarantee is a property of the whole pipeline: storage must return a truthful result for every write, and every component between receiver and storage must wait for that result before acknowledging.

Storage: Cassandra and ClickHouse write synchronously and return errors. Elasticsearch and OpenSearch do so only with `write_mode: sync`; their default async mode reports success before anything reached the backend.

Two components acknowledge early and break the guarantee:
- The batch processor hands each batch to a background goroutine and returns success immediately. If the export fails it logs `Sender failed` and discards the batch. Jaeger's sample configs such as config.yaml and config-elasticsearch.yaml include the batch processor, so they are not lossless.
- An exporter queue without `wait_for_result` enqueues and returns success. Only `wait_for_result: true` blocks until the write completes and returns its result. With no queue block the exporter writes synchronously, one write per incoming batch.

The recommended batching is the queue with `wait_for_result: true` and a `batch` block: it merges requests from many clients into one write up to `batch.max_size` and returns the result to every contributor. `batch.min_size` must be positive (at zero nothing merges); `batch.flush_timeout` bounds added latency.

## Checked

The storage, batch processor, queue wait_for_result and batching claims were confirmed against the Delivery Guarantees page. The page header marks version 2.22 as outdated in favour of 2.23, so recheck defaults against the latest docs.

Method: docs-checked 2026-11-09 against the Jaeger 2.22 Delivery Guarantees page (full page read from a downloaded copy).
