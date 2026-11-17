---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-es-poison-pill-handling
name: jaeger-es-poison-pill-handling
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, poison-pill-handling, rejected-documents, bulk-item-status, elasticsearch-mapping-conflict]
level: advanced
status: docs-checked
description: "Choose poison_pill_handling fail or drop for documents Elasticsearch rejects on every attempt, in sync write mode."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/elasticsearch/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop a bad span from blocking the pipeline, or make sure none is ever lost.

A poison pill is a document Elasticsearch rejects on every attempt, for example a span attribute that conflicts with the index mapping type. The sync writer reads the per-item status of each `_bulk` response and separates transient failures (429 back-pressure, unavailable node) from terminal rejections. A transient failure makes the whole batch error so the pipeline retries it. For terminal rejections:
- `fail` (default): the batch returns an error, the pipeline retries, and the rejected span blocks everything behind it until the document or mapping is fixed. Use when no span may be lost and someone watches the pipeline.
- `drop`: rejected documents are discarded and logged, and the batch completes. Use when losing a rare malformed span is acceptable and the pipeline must never stall.

A third option, forwarding rejected spans to a dead-letter pipeline, is chosen by topology: keep `fail` and declare `jaeger_storage_exporter` under `connectors:`.

Limits: a document that fails the whole request (for example larger than `http.max_content_length`, HTTP 413) is retried like any request failure until an operator removes it or raises the limit. In async mode the setting has no effect; the bulk buffer logs a rejected document and does not retry.

## Checked

2026-11-03. Confirmed against the Elasticsearch page, Poison pills section: definition, per-item status handling, transient versus terminal failures, fail (default) and drop behaviors and when to use each, the dead-letter option, the 413 limit case and the async-mode note. Nothing removed.
Method: documentation only; no commands were run.
