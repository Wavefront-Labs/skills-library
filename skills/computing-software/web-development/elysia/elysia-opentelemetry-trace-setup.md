---
id: computing-software.web-development.elysia.elysia-opentelemetry-trace-setup
name: elysia-opentelemetry-trace-setup
category: computing-software
field: web-development
product: elysia
tags: [opentelemetry, tracing, observability, plugin, otlp]
level: advanced
status: docs-checked
description: "Add OpenTelemetry tracing to an Elysia server with @elysia/opentelemetry and an OTLP span exporter, and tune the SDK options."
sources:
  - https://elysiajs.com/plugins/opentelemetry.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: collect spans from Elysia and any OpenTelemetry-compatible library, then ship them to a collector such as Jaeger.

This skill covers the plugin config reference page only; that page points to /patterns/opentelemetry for usage and utilities, which are not covered here.

1. Install `@elysia/opentelemetry` plus the SDK/exporter packages used in the example (`@opentelemetry/sdk-trace-node`, `@opentelemetry/exporter-trace-otlp-proto`).
2. Apply the plugin to an instance:

```typescript
import { Elysia } from 'elysia'
import { opentelemetry } from '@elysia/opentelemetry'
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-node'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-proto'

new Elysia().use(
    opentelemetry({
        spanProcessors: [new BatchSpanProcessor(new OTLPTraceExporter())]
    })
)
```

Parent and child spans are applied automatically across libraries.

Options (the plugin extends OpenTelemetry SDK options):
- `serviceName` (string): the namespace the service is identified as.
- `spanProcessors` (SpanProcessor[]) or `traceExporter` (SpanExporter, wrapped in a BatchSpanProcessor). If an exporter or span processor is not configured programmatically, the package auto-sets the default OTLP exporter over http/protobuf with a BatchSpanProcessor.
- `sampler`: default samples all traces.
- `instrumentations`: default `getNodeAutoInstrumentations()`.
- `autoDetectResources` (default true), `resource`, `resourceDetectors` (default envDetector, processDetector, hostDetector; needs autoDetectResources true). Without `resourceDetectors`, set env `OTEL_NODE_RESOURCE_DETECTORS` to a list from `env, host, os, process, serviceinstance (experimental), all, none`, e.g. `export OTEL_NODE_RESOURCE_DETECTORS="env,host"`.
- `contextManager` (default AsyncHooksContextManager), `textMapPropagator` (default W3C Trace Context plus Baggage via CompositePropagator), `metricReader`, `views` (e.g. histogram bucket sizes), `spanLimits`.

Gotcha: not configuring an exporter or span processor does not disable tracing; per the page the package sets up the default OTLP http/protobuf exporter with a BatchSpanProcessor.

## Checked

Checked 2026-11-07 against the Elysia documentation source (plugins/opentelemetry.html); each claim, option name and default was compared with the page text. Removed the invented Verify step; aligned the exporter fallback and serviceName wording with the page.

Method: documentation only; no commands were run.
