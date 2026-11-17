---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-binary-components
name: jaeger-binary-components
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, jaeger-components, ocb, tail-sampling-processor, spanmetrics-connector]
level: advanced
status: docs-checked
description: "Know which receivers, processors, exporters, connectors and extensions ship in the Jaeger v2 binary."
sources:
  - https://www.jaegertracing.io/docs/2.22/architecture/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know what you can use in a pipeline.

The binary is built on the OpenTelemetry Collector framework and includes official upstream components, components from opentelemetry-collector-contrib (Kafka exporter and receiver, tail sampling processor) and Jaeger's own.

Jaeger's own: Jaeger Storage Extension (hub for storage backends), Jaeger Storage Exporter, Jaeger Query Extension (query APIs and UI), Adaptive Sampling Processor, Remote Sampling Extension (endpoints from a static file or adaptive sampling).

Receivers: OTLP; Jaeger (gRPC or Thrift); Kafka (OTLP, Jaeger or Zipkin formats); Zipkin (v1 and v2); No-op (query-only deployment).

Processors: Batch, Tail Sampling, Memory Limiter (back-pressure when overloaded), Attributes (filter, rewrite, enrich, redact, reduce volume), Filter (drops spans and events; may cause broken traces).

Exporters: OTLP (gRPC), OTLP HTTP, Kafka, Prometheus, Debug, No-op.

Connectors: Span Metrics, Forward.

Extensions: Health Check v2, zPages, pprof (Go net/http/pprof for performance profiles).

Customize the set with the OpenTelemetry Collector Builder (ocb).

## Checked

2026-11-08: read the whole Architecture page (raw markdown from the jaegertracing/documentation repo, v2/2.22), including the Jaeger Binary and component lists. Confirmed every listed component and description.

Method: documentation only; no commands were run.
