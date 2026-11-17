---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-direct-otlp-lossless
name: jaeger-direct-otlp-lossless
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, otlp-retry, grpc-unavailable, poison-pill, direct-ingest]
level: sme
status: docs-checked
description: "Configure direct OTLP ingest so storage errors reach SDKs as retryable Unavailable or 503 responses."
sources:
  - https://www.jaegertracing.io/docs/2.22/deployment/delivery-guarantees/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let clients retry when storage fails.

The OTLP receiver turns the storage error into an OTLP failure response: gRPC Unavailable or HTTP 503, both retryable per the OTLP specification. The SDK or agent keeps the batch in its buffer, backs off and retries within its own budget. That budget is finite by default: the OpenTelemetry Go SDK batch span processor gives an export 30 seconds and its OTLP exporter retries for one minute. So the guarantee is that a failure is reported to the client instead of absorbed by the collector; how long an outage the client survives is client configuration.

Jaeger reports every storage error as retryable, even a document rejected on every attempt. With Elasticsearch `poison_pill_handling: fail` a client would retry such a span until its budget ran out. So direct ingest pairs `write_mode: sync` with `poison_pill_handling: drop` or the dead-letter pipeline.

Pipeline: receivers `[otlp]`, processors `[]`, exporters `[jaeger_storage_exporter]` with `queue` having `wait_for_result: true`, `sizer: bytes`, `num_consumers: 4`, `queue_size: 104857600` and a batch block (`flush_timeout: 200ms`, `min_size: 1048576`, `max_size: 4194304`).

Keep `retry_on_failure` disabled for direct ingest: the client already retries, and a collector retry would only hold the request open. Keep `block_on_overflow` at default false so a full queue returns a retryable error as back-pressure. No queue at all is also lossless, with one write per request.

## Checked

2026-11-03. Confirmed against the Delivery Guarantees page, Direct ingest over OTLP: Unavailable or 503 retryable responses, the SDK 30 second and one minute budgets, every storage error reported as retryable, pairing sync with drop or dead-letter, the example pipeline and queue values, retry_on_failure disabled, block_on_overflow default and the no-queue option. Nothing removed.
Method: documentation only; no commands were run.
