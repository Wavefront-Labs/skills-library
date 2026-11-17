---
id: computing-software.web-development.elysia.instrument-elysia-with-opentelemetry
name: instrument-elysia-with-opentelemetry
category: computing-software
field: web-development
product: elysia
tags: [opentelemetry, tracing, otlp-exporter, preload, bun-build-external, spans]
level: advanced
status: docs-checked
description: "Add @elysia/opentelemetry to an Elysia app, export spans over OTLP, add custom spans, preload library instrumentations and bundle for production."
sources:
  - https://elysiajs.com/patterns/opentelemetry.html
  - https://elysiajs.com/patterns/deploy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get request, lifecycle and custom spans from an Elysia server into an OpenTelemetry backend.

## Install and apply

```ts
import { Elysia } from 'elysia'
import { opentelemetry } from '@elysia/opentelemetry'

new Elysia().use(opentelemetry())
```

Install with `bun add @elysia/opentelemetry`. Spans are named after hook function names and related lifecycle events are grouped.

## Export to a backend (Axiom example)

```ts
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-node'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-proto'

new Elysia().use(opentelemetry({
  spanProcessors: [new BatchSpanProcessor(new OTLPTraceExporter({
    url: 'https://api.axiom.co/v1/traces',
    headers: { Authorization: `Bearer ${Bun.env.AXIOM_TOKEN}`, 'X-Axiom-Dataset': Bun.env.AXIOM_DATASET }
  }))]
}))
```

## Custom spans

- `record('database.query', () => db.query(...))` is `startActiveSpan` with auto-close and exception capture.
- `getCurrentSpan()` returns the current request span from `AsyncLocalStorage`, usable outside handlers; `setAttributes({ 'custom.attribute': 'value' })` is sugar for `getCurrentSpan().setAttributes`.
- Name your hooks: an arrow function shows up as `anonymous`; `.derive(async function getProfile({ cookie: { session } }) {...})` shows as `getProfile`.

## Library instrumentations (e.g. pg)

Instrumentations must run before the target module is imported. Put the plugin in its own file and preload it:

```ts
// src/instrumentation.ts
export const instrumentation = opentelemetry({ instrumentations: [new PgInstrumentation()] })
```

Use it in `src/index.ts` with `.use(instrumentation)` and add `bunfig.toml`:

```toml
preload = ["./src/instrumentation.ts"]
```

## Production build

OpenTelemetry monkey-patches `node_modules/<library>`, so keep instrumented libraries out of the bundle: `bun build --compile --external pg --outfile server src/index.ts`. Keep `node_modules` on the server, list `pg` under `dependencies` and the instrumentation packages under `devDependencies`, then run `bun install --production` (delete `node_modules` and reinstall if dev dependencies linger). Do not use `--minify`; it destroys function names used for span names.

## Checked

2026-11-07. Read in full: patterns/opentelemetry (install, Axiom exporter with `spanProcessors`, `record`, `getCurrentSpan`, `setAttributes`, named hooks, `PgInstrumentation` preload via `bunfig.toml`, `--external pg`, dependencies vs devDependencies, `bun install --production`) and patterns/deploy (the `--minify` warning, which says it reduces function names to a single character). Every claim matched the page text; nothing removed. The `getTracer` utility the page also mentions is not covered here.

Method: documentation only; no commands were run.
