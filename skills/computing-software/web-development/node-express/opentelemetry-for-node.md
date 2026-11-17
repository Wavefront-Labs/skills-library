---
id: computing-software.web-development.node-express.opentelemetry-for-node
name: opentelemetry-for-node
category: computing-software
field: web-development
product: node-express
tags: [opentelemetry-node, apm, distributed-tracing, otel, observability]
level: advanced
status: gated
description: "Instrumenting Node.js with OpenTelemetry: SDK setup loaded before the app, auto-instrumentations, OTLP export to a collector or APM, custom spans, log correlation, and sampling."
sources:
  - https://opentelemetry.io/docs/languages/js/getting-started/nodejs/
  - https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/packages/auto-instrumentations-node
  - https://opentelemetry.io/docs/concepts/sampling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# APM and OpenTelemetry for Node

## 1. Setup (load before anything else)
```js
// instrumentation.mjs
import { NodeSDK } from "@opentelemetry/sdk-node";
import { getNodeAutoInstrumentations } from "@opentelemetry/auto-instrumentations-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-proto";
import { OTLPMetricExporter } from "@opentelemetry/exporter-metrics-otlp-proto";
import { PeriodicExportingMetricReader } from "@opentelemetry/sdk-metrics";

const sdk = new NodeSDK({
  serviceName: process.env.OTEL_SERVICE_NAME ?? "orders-api",
  traceExporter: new OTLPTraceExporter(),                 // OTEL_EXPORTER_OTLP_ENDPOINT, default http://localhost:4318
  metricReader: new PeriodicExportingMetricReader({ exporter: new OTLPMetricExporter() }),
  instrumentations: [getNodeAutoInstrumentations({ "@opentelemetry/instrumentation-fs": { enabled: false } })],
});
sdk.start();
process.on("SIGTERM", () => sdk.shutdown().finally(() => process.exit(0)));
```
```bash
node --import ./instrumentation.mjs dist/server.js      # ESM; CommonJS: node --require ./instrumentation.js
```
Ran on Node 24.22 with @opentelemetry/sdk-node 0.223.0, auto-instrumentations-node 0.81.2 and a local OTLP/HTTP receiver on the default port 4318 (the exporter reached it with no endpoint configured): with `--import ./instrumentation.mjs` an ESM Express app exported a trace containing the service name, the HTTP server span, the `/orders/:id` route and the custom `order.place` span, and metrics every interval. Two details: the batch span processor only flushed because the app waited; a plain `process.exit()` lost the trace unless `sdk.shutdown()` ran (default `OTEL_BSP_SCHEDULE_DELAY` is several seconds); and pino `trace_id`/`span_id` injection only appeared once the ESM loader hook was added (`--experimental-loader=@opentelemetry/instrumentation/hook.mjs`), which also produced an OTLP `/v1/logs` export.
- Instrumentation patches modules at load time: it must run **before** `express`, `pg`, `http` etc. are imported. ESM needs `--import` (and the SDK's loader hook registration); importing it at the top of `server.js` is too late for ESM.
- Zero-code alternative: `npm i @opentelemetry/auto-instrumentations-node` and `node --require @opentelemetry/auto-instrumentations-node/register app.js` with `OTEL_*` env vars (ran against the ESM test app: the trace exported).
- Disable noisy instrumentations (fs, dns) to cut overhead.

## 2. Export
Send OTLP to an OpenTelemetry Collector (batching, tail sampling, routing) which forwards to your backend (Grafana Tempo, Honeycomb, Datadog, New Relic, Jaeger; no Collector or backend was available to run: gated: unconfirmed, source is paywalled or blocked). Vendors accept OTLP directly too; the collector keeps app config vendor-neutral.

## 3. Custom spans and attributes
```js
import { trace, SpanStatusCode } from "@opentelemetry/api";
const tracer = trace.getTracer("orders");
export async function placeOrder(cart) {
  return tracer.startActiveSpan("order.place", async (span) => {
    span.setAttribute("order.items", cart.items.length);
    try { return await doPlace(cart); }
    catch (e) { span.recordException(e); span.setStatus({ code: SpanStatusCode.ERROR }); throw e; }
    finally { span.end(); }
  });
}
```
Never put PII or secrets in attributes. Follow semantic conventions (`http.route` is stable; the database attribute is now `db.system.name`, `db.system` is the older name; checked in the semantic-conventions registry).

## 4. Logs correlation
Pino/Winston instrumentations inject `trace_id`/`span_id` into log records, linking logs to traces in the backend.

## 5. Sampling and overhead
- `OTEL_TRACES_SAMPLER=parentbased_traceidratio`, `OTEL_TRACES_SAMPLER_ARG=0.1` for 10% head sampling; parent-based keeps distributed traces whole (ran with ratio `0`: no trace was exported).
- Tail sampling in the collector keeps all errors and slow traces (gated: unconfirmed, source is paywalled or blocked; not run).
- Measure the CPU overhead of auto-instrumentation under your own load; no figure was measured here.

## Verify
- [ ] A request shows one trace spanning HTTP server, DB and outgoing HTTP spans with the correct route; logs carry trace ids; spans flush on shutdown.
