---
id: computing-software.cloud-infrastructure-engineering.observability.otel-browser-javascript-instrumentation
name: otel-browser-javascript-instrumentation
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [opentelemetry, otel-browser-instrumentation, web-tracer-provider, document-load, fetch-instrumentation, cors]
level: advanced
status: docs-checked
description: "Instrument browser apps with OpenTelemetry JS: tracer provider, ZoneContextManager, document-load, XHR and user-interaction instrumentations, traceparent meta tag."
sources: ["https://opentelemetry.io/docs/languages/js/getting-started/browser/", "https://opentelemetry.io/docs/languages/js/exporters/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenTelemetry browser instrumentation

**Goal:** frontend spans for page loads and API calls, linked to backend traces.

The OpenTelemetry JS browser guide warns that client instrumentation for the browser is experimental and mostly
unspecified, so pin versions and re-read the guide on upgrade.

## Setup (from the getting-started guide)
Packages: `@opentelemetry/api`, `@opentelemetry/core`, `@opentelemetry/sdk-trace`, `@opentelemetry/context-zone`,
`@opentelemetry/instrumentation`, `@opentelemetry/instrumentation-document-load`.
```ts
import { context, propagation, trace } from '@opentelemetry/api';
import { ConsoleSpanExporter, SimpleSpanProcessor, TracerProvider } from '@opentelemetry/sdk-trace';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import { CompositePropagator, W3CBaggagePropagator, W3CTraceContextPropagator } from '@opentelemetry/core';
import { registerInstrumentations } from '@opentelemetry/instrumentation';
import { DocumentLoadInstrumentation } from '@opentelemetry/instrumentation-document-load';

const tracerProvider = new TracerProvider({
  spanProcessors: [new SimpleSpanProcessor({ exporter: new ConsoleSpanExporter() })],
});
trace.setGlobalTracerProvider(tracerProvider);
context.setGlobalContextManager(new ZoneContextManager().enable());
propagation.setGlobalPropagator(new CompositePropagator({
  propagators: [new W3CTraceContextPropagator(), new W3CBaggagePropagator()],
}));
registerInstrumentations({ instrumentations: [new DocumentLoadInstrumentation()] });
```
The guide notes `BatchSpanProcessor` exports spans in batches and is more efficient than the simple processor; swap
the console exporter for a real backend exporter (see the exporters page).

## Pieces
- `DocumentLoadInstrumentation`: traces document load timings as spans (for example `documentFetch`).
- `@opentelemetry/instrumentation-user-interaction` (`UserInteractionInstrumentation`) and
  `@opentelemetry/instrumentation-xml-http-request` (`XMLHttpRequestInstrumentation`) cover clicks and Ajax requests.
- `ZoneContextManager` is the context manager the guide registers.
- To join the browser trace to the server's, the server's HTML template sets a `<meta name="traceparent"
  content="{version}-{traceId}-{spanId}-{sampleDecision}">` tag (`01` sampled, `00` not sampled), generated per request.
- The guide points to the OpenTelemetry Meta Packages for Web to get the common instrumentations at once.

## Production concerns
- Never ship backend credentials in the browser.
- Scrub URLs with tokens and avoid PII in attributes.

## Checked
2026-11-01. Confirmed on the JS browser getting-started page: experimental warning, package list, setup code,
instrumentations, traceparent meta tag, BatchSpanProcessor remark, meta packages. Removed: WebTracerProvider and
`sdk-trace-web` names (the current guide uses `TracerProvider` from `sdk-trace`), fetch instrumentation options,
CORS collector config, sampler and `visibilitychange` advice, the unreachable contrib metapackage link.
Method: documentation only; no commands were run.
