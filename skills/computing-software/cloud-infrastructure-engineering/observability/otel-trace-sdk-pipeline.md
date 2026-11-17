---
id: computing-software.cloud-infrastructure-engineering.observability.otel-trace-sdk-pipeline
name: otel-trace-sdk-pipeline
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [opentelemetry, distributed-tracing, tracer-provider, trace-exporter-config, span-processor, batch-span-processor, simple-span-processor, span-limits, attribute-limits, messaging-spans, producer-consumer-spans]
level: practitioner
status: docs-checked
description: "Configure the OpenTelemetry trace SDK: TracerProvider, OTLP exporter, batch vs simple processors, span and attribute limits, and producer/consumer messaging spans."
sources: ["https://opentelemetry.io/docs/specs/otel/trace/sdk/", "https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/", "https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trace SDK pipeline

## TracerProvider + exporter (Python shown; same shape in every SDK)
```python
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider, SpanLimits
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

provider = TracerProvider(
    resource=Resource.create({"service.name": "checkout", "service.version": "1.8.0"}),
    span_limits=SpanLimits(max_span_attributes=64, max_events=64, max_attribute_length=4096),
)
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True),
    max_queue_size=4096, schedule_delay_millis=2000, max_export_batch_size=512, export_timeout_millis=10000))
trace.set_tracer_provider(provider)
# on shutdown: provider.shutdown()  -> flushes the queue
```
Env equivalents: `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_PROTOCOL=grpc|http/protobuf`,
`OTEL_BSP_MAX_QUEUE_SIZE` (2048), `OTEL_BSP_SCHEDULE_DELAY` (5000 ms), `OTEL_BSP_MAX_EXPORT_BATCH_SIZE` (512),
`OTEL_SPAN_ATTRIBUTE_COUNT_LIMIT` (128), `OTEL_ATTRIBUTE_VALUE_LENGTH_LIMIT` (unlimited), `OTEL_SPAN_EVENT_COUNT_LIMIT`.

## Batch vs simple processor
| | Batch | Simple |
|---|---|---|
| Export | async, batched | synchronous per span end |
| Production | yes | no (latency on every span end) |
| Use | always | tests, debugging, very short-lived scripts |
When the batch queue is full, spans are **dropped** (SDK self-metrics/logs report it); raise queue size or
fix the exporter path. Always call `shutdown()`/`forceFlush()` in serverless and CLI tools or the last batch is lost.

## Limits
Limits protect memory from runaway attributes (huge SQL, payload dumps). The trace SDK spec defines how limits apply to attributes, events and links. Set `max_attribute_length` for SQL/statement attributes.

## Messaging spans
- Producer: span kind `PRODUCER`, name `publish orders` (`{operation} {destination}`), inject context into
  message headers.
- Consumer: kind `CONSUMER`, name `process orders`; for batch receives create one span with **links** to each
  message's producer context instead of a parent (a batch has many parents).
- Attributes: `messaging.system` (kafka), `messaging.destination.name`, `messaging.operation.type`
  (`send`, `receive`, `process`), `messaging.kafka.consumer.group`.

## Verify
- [ ] Collector receives spans; SDK logs show no "queue full, dropping span".
- [ ] Consumer spans link to producer spans across the broker in the trace view.

## Checked
- 2026-10-28. Checked against the SDK environment variables spec page, the trace SDK spec, the Python SDK docs (SpanLimits, BatchSpanProcessor) and the messaging spans semconv page (semconv 1.26 schema for the Kafka rename).
- Confirmed: `OTEL_BSP_*` defaults (2048, 5000 ms, 512), `OTEL_SPAN_EVENT_COUNT_LIMIT` 128, `SpanLimits` and `BatchSpanProcessor` argument names, `messaging.operation.type`, `messaging.kafka.consumer.group`.
- Removed: `dropped_attributes_count` claim (not in the fetched pages).
Method: documentation only; no commands were run.
