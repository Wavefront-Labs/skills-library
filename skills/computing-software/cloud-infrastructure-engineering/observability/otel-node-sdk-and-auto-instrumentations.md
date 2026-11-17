---
id: computing-software.cloud-infrastructure-engineering.observability.otel-node-sdk-and-auto-instrumentations
name: otel-node-sdk-and-auto-instrumentations
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [node-sdk-setup, auto-instrumentations-node-config, language-instrumentation, zero-code-instrumentation, nodejs]
level: practitioner
status: gated
description: "Set up OpenTelemetry in Node.js: --require register, NodeSDK in instrumentation.js, ESM loader hooks, enabling or disabling auto-instrumentations, and graceful shutdown."
sources: ["https://opentelemetry.io/docs/zero-code/js/", "https://opentelemetry.io/docs/languages/js/getting-started/nodejs/", "https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/metapackages/auto-instrumentations-node"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node SDK and auto-instrumentations-node

## Zero-code (env driven)
```bash
npm i @opentelemetry/api @opentelemetry/auto-instrumentations-node
export OTEL_SERVICE_NAME=web OTEL_TRACES_EXPORTER=otlp OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-agent:4318
export OTEL_NODE_RESOURCE_DETECTORS=env,host,os
export OTEL_NODE_ENABLED_INSTRUMENTATIONS=http,express,pg,ioredis   # or OTEL_NODE_DISABLED_INSTRUMENTATIONS=fs,dns
node --require @opentelemetry/auto-instrumentations-node/register app.js
```
Or `NODE_OPTIONS="--require @opentelemetry/auto-instrumentations-node/register"`.

## Code-based (instrumentation.js)
```js
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-proto');
const { PeriodicExportingMetricReader } = require('@opentelemetry/sdk-metrics');
const { OTLPMetricExporter } = require('@opentelemetry/exporter-metrics-otlp-proto');
// OTLP exporter package names above (gated: unconfirmed, source is paywalled or blocked)
const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter(),
  metricReader: new PeriodicExportingMetricReader({ exporter: new OTLPMetricExporter() }),
  instrumentations: [getNodeAutoInstrumentations()],
});
sdk.start();
process.on('SIGTERM', () => sdk.shutdown().finally(() => process.exit(0)));
```
`node --require ./instrumentation.js app.js` - it **must** load before `express`, `pg` etc. are required, because
instrumentation patches modules at require time.

## ESM
For ESM apps the Node.js getting-started page uses
`node --experimental-loader=@opentelemetry/instrumentation/hook.mjs --require ./instrumentation.js app.js`; see the OpenTelemetry JS ESM support docs.

## Gotchas
- Do not combine `--require .../register` in `NODE_OPTIONS` with a code-based `--import`/`--require` of your own SDK setup; the docs warn about conflicting flags.

## Verify
`OTEL_TRACES_EXPORTER=console` prints spans; `OTEL_LOG_LEVEL=debug` shows which instrumentations patched which modules.

## Checked
- 2026-10-28. Checked against the OpenTelemetry JS zero-code page, the Node.js getting-started page and the Kubernetes Operator Node.js notes.
- Confirmed: `--require @opentelemetry/auto-instrumentations-node/register`, `NODE_OPTIONS`, `OTEL_NODE_ENABLED_INSTRUMENTATIONS`, `OTEL_NODE_DISABLED_INSTRUMENTATIONS`, `OTEL_NODE_RESOURCE_DETECTORS` (documented example env,host,os), `NodeSDK`, `getNodeAutoInstrumentations`, `PeriodicExportingMetricReader`, `hook.mjs` loader command, conflicting-flags warning.
- Removed (unconfirmed): `container` detector value, per-instrumentation config examples, `--import` ESM recipe, bundler advice, fs/dns defaults, Lambda layer.
- Gated: the `@opentelemetry/exporter-*-otlp-proto` package names in the sample were not found in fetched pages (the js-contrib README page failed to fetch).
Method: documentation only; no commands were run.
