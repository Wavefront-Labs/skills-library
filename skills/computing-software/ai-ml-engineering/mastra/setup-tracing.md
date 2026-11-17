---
id: computing-software.ai-ml-engineering.mastra.setup-tracing
name: setup-tracing
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, tracing, observability, sampling, metadata, span-filtering, trace-ids, opentelemetry]
level: practitioner
status: docs-checked
description: "Configure Mastra observability and tracing: exporters, storage, sampling, metadata, tags, redaction, span filtering, serialization limits and external trace context."
sources:
  - https://mastra.ai/docs/observability/overview
  - https://mastra.ai/docs/observability/tracing/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get useful, affordable traces out of agents, workflows, tools and model calls.

## Base config
`npm install @mastra/observability @mastra/libsql @mastra/duckdb`, then route the observability domain to an analytics store:
```ts
new Mastra({
  storage: new MastraCompositeStore({ id: 'composite-storage',
    default: new LibSQLStore({ id: 'mastra-storage', url: 'file:./mastra.db' }),
    domains: { observability: await new DuckDBStore().getStore('observability') } }),
  observability: new Observability({ configs: { default: {
    serviceName: 'mastra',
    exporters: [new MastraStorageExporter(), new MastraPlatformExporter()],
    spanOutputProcessors: [new SensitiveDataFilter()],
  } } }),
})
```
- Keep `MastraStorageExporter` (Studio) and/or `MastraPlatformExporter` when adding external exporters (Langfuse, Datadog, Arize, any OTel platform).
- DuckDB for local; ClickHouse for high-volume production; metrics need an analytics-capable store.
- Serverless: `await mastra.observability.flush()` and use external storage.
- Several configs plus `configSelector: () => process.env.NODE_ENV || 'development'`.

## Sampling (per config)
`sampling: { type: 'always' | 'never' }`, `{ type: 'ratio', probability: 0.1 }`, or `{ type: 'custom', sampler: options => ... }` (e.g. read `options?.metadata?.userTier`).

## Metadata, tags, naming
- On a span: `context?.tracingContext.currentSpan?.update({ metadata: {...} })`.
- Top-level `environment` on `Mastra` tags all signals; if unset, `mastra dev` runs resolve to `development`, otherwise `NODE_ENV`; per-call `tracingOptions.metadata.environment` wins.
- Auto-extract from RequestContext: config `requestContextKeys: ['userId', 'user.id']` (dot paths) plus per-call `tracingOptions.requestContextKeys` (merged). Root spans extract automatically; child spans only when given `requestContext`. Explicit metadata wins.
- `tracingOptions: { tags: [...], metadata: {...}, rootSpanName: 'skill-analyze: typescript' }`. Tags apply to the root span only; `rootSpanName` renames only the root span.
- `hideInput: true` / `hideOutput: true` drop data from all exported spans of the trace; use `SensitiveDataFilter` for field-level redaction.
- Child spans: `currentSpan?.createChildSpan({ type: 'generic', name, input, metadata })`, then `.end({ output })` or `.error({ error })`.

## Shaping export
- Span processors (`SpanOutputProcessor`, run in order, must mutate and return the same span or return `undefined` to drop it; copies are dropped) vs per-exporter `customSpanFormatter` (async allowed; combine with `chainFormatters`; keep under about 100 ms).
- Filtering order: internal spans dropped unless `includeInternalSpans`, then `excludeSpanTypes` (e.g. `SpanType.MODEL_CHUNK`), then processors, then `spanFilter` (a throw keeps the span).
- `serializationOptions`: `maxStringLength` (131072), `maxDepth` (8), `maxArrayLength` (50), `maxObjectKeys` (50).

## Trace IDs and external context
`result.traceId` from `generate`/`stream`/`run.start` (undefined when tracing is off or sampled out). Join a parent trace with `tracingOptions: { traceId, parentSpanId }` (trace ID 1-32 hex, span ID 1-16 hex; invalid ones are replaced or ignored, not fatal). To nest a judge run under an earlier Mastra run use `nestUnderRun(turn)` from `@mastra/core/observability`.

## Outcomes
Spans carry `outcome`, `stopReason`, `stopReasonContext` (e.g. `blocked` / `guardrail`, `limit` / `max_steps`); use `endTime` to tell whether a span finished.

## Checked

Method: 2026-11-08 read the raw MDX of the Mastra observability overview and tracing pages in full and compared each claim in the skill (base config, storage advice, sampling types, metadata and tags rules, processors versus formatters, filtering order, serialization defaults, trace IDs, external context and nestUnderRun); all are supported and unchanged.
