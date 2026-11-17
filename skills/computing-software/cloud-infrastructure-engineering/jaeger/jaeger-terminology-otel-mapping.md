---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-terminology-otel-mapping
name: jaeger-terminology-otel-mapping
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, tags-attributes, span-references, span-links, baggage]
level: intro
status: docs-checked
description: "Map Jaeger data-model terms to OpenTelemetry names: tags to attributes, logs to events, references to links, process to resource."
sources:
  - https://www.jaegertracing.io/docs/2.22/architecture/terminology/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: translate between the Jaeger and OpenTelemetry vocabularies.

Jaeger's data model is inspired by the OpenTracing Specification and is logically very similar to OpenTelemetry Traces:
- Tags map to Attributes. Both support typed values, but nested tags are not supported in Jaeger.
- Span Logs map to Span Events: structured point-in-time events on the span.
- Span References map to Span Links. Jaeger references have a required type (child-of or follows-from) and always refer to predecessor spans; OpenTelemetry links have no type but allow attributes.
- Process maps to Resource: a struct describing the entity that produces the telemetry.

Definitions: a span is a logical unit of work with an operation name, a start time and a duration; spans may be nested and ordered to model causal relationships. A trace is the data or execution path through the system, a directed acyclic graph of spans. Baggage is arbitrary user-defined key-value metadata attached to the distributed context and propagated by the tracing SDKs (see W3C Baggage).

## Checked

2026-11-08: confirmed against the Jaeger 2.22 Terminology page, read in full (mapping table, span, trace, baggage definitions). Removed the paragraph about the features page, which is not a cited source.

Method: documentation only; no commands were run.
