---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-dead-letter-pipeline
name: jaeger-dead-letter-pipeline
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, dead-letter, storage-connector, rejection-reason, dead-letter-spans-metric]
level: sme
status: docs-checked
description: "Forward spans that storage rejects permanently to a dead-letter exporter by declaring jaeger_storage_exporter as a connector."
sources:
  - https://www.jaegertracing.io/docs/2.22/deployment/delivery-guarantees/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep rejected spans instead of dropping them.

Declare `jaeger_storage_exporter` under `connectors:` instead of `exporters:`. It then writes batches like the exporter (same `queue` and `retry_on_failure` settings; an enabled queue needs `wait_for_result: true`) and re-emits terminally rejected spans onto its output pipeline:
```
service:
  pipelines:
    traces:
      receivers: [kafka]
      exporters: [jaeger_storage_exporter]
    traces/dead_letter:
      receivers: [jaeger_storage_exporter]
      exporters: [kafka/dead_letter]
```
Keep storage at `write_mode: sync` with `poison_pill_handling: fail`; the connector decides what a rejection means. Today only Elasticsearch and OpenSearch in sync mode report rejections in the needed form. If one file needs both forms, name one, for example `jaeger_storage_exporter/dead_letter`.

Sink requirements:
- It must deliver synchronously: disable its `sending_queue`, otherwise a queued exporter acknowledges at enqueue.
- It must refuse what it does not keep: `otlphttp` treats OTLP partial success as success. A kafka sink acknowledges per `producer.required_acks` (default 1, or all); set `producer.max_message_bytes` (example 8388608) and the broker's `message.max.bytes` to fit a whole batch's rejected spans.

Each forwarded span carries the attribute `jaeger.storage.rejection_reason`. Watch the `jaeger_storage_exporter_dead_letter_spans` metric: a trickle means a few malformed spans; a sudden rise usually means a mapping change rejecting a whole class of spans.

## Checked

2026-11-03. Confirmed against the Delivery Guarantees page, Dead-letter pipeline section: connector form of jaeger_storage_exporter, wait_for_result requirement, fail handling and the Elasticsearch/OpenSearch sync-only limitation, naming with a suffix when both forms are used, sink requirements (disabled sending_queue, partial success, required_acks, max_message_bytes, message.max.bytes), the rejection_reason attribute and the dead_letter_spans metric. Nothing removed.
Method: documentation only; no commands were run.
