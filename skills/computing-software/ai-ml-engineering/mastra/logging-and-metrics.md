---
id: computing-software.ai-ml-engineering.mastra.logging-and-metrics
name: logging-and-metrics
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, pinologger, metrics, logging, observability, trace-correlation, duckdb]
level: practitioner
status: docs-checked
description: "Set up Mastra PinoLogger with trace-correlated logs, choose which levels reach observability storage, query logs, and pick storage for automatic duration, token and cost metrics."
sources:
  - https://mastra.ai/docs/observability/logging
  - https://mastra.ai/docs/observability/metrics/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: structured logs tied to traces, and metrics without extra instrumentation.

## Logger
```typescript
new Mastra({ logger: new PinoLogger({ name: 'Mastra', level: 'info' }) })  // from '@mastra/loggers'
```
Inside workflow steps and tools use `mastra.getLogger()` (tools: `context?.mastra.getLogger()`); levels `debug`, `info`, `warn`, `error`. A second argument with a structured object makes logs filterable: `logger.info('workflow info log', { agent })`.

## Trace correlation
With observability configured, logger calls (including Mastra internals) are forwarded to observability storage and, inside a traced operation, get `trace_id` and `span_id` (W3C format) in the native output. Pretty printing is on by default; set `prettyPrint: false` for JSON. `ConsoleLogger` appends the fields as an object argument. Control independently:
```typescript
new Mastra({ logger, loggerOptions: { correlation: true, export: false } }) // both default true
```
Observability level, separate from the console level:
```typescript
configs: { default: { serviceName: 'my-app', exporters: [new MastraStorageExporter()],
  logging: { enabled: true, level: 'info' } } }
```
`enabled` defaults to `true`, `level` to `'warn'`; allowed `'debug' | 'info' | 'warn' | 'error' | 'fatal'`.

Custom `IMastraLogger` classes still work through a deprecated dual-write fallback, without trace fields. To get them, extend `MastraLogger` and implement `__attachObservability(ctx)`; use `ctx.options.correlation` with `ctx.resolveTraceFields()`, and `ctx.getLogSink()?.[level](message, buildLogRecordData(args))` when `ctx.options.export` (imports from `@mastra/core/logger`).

## Query logs
```typescript
const logs = await new MastraClient().listLogsVNext({
  filters: { level: 'error' }, pagination: { page: 1, perPage: 50 },
  orderBy: { field: 'timestamp', direction: 'desc' } })
```
Persistent stores (DuckDB, ClickHouse) keep logs across restarts.

## Metrics
Derived automatically from spans: duration (agents, workflows, tools, model calls, processors), token usage, and cost estimates (provider/model prices from models.dev or a custom gateway), all with trace correlation.
- Needs an analytics-capable store: DuckDB (`@mastra/duckdb`, local), ClickHouse (`@mastra/clickhouse`, production), `PostgresStoreVNext` with the observability domain enabled, or in-memory (lost on restart). Spanner disables metrics by default (`disableMetrics: false` only for light workloads). LibSQL, MSSQL and MongoDB do not implement metrics.
- Setup: composite storage routing `observability` to `await new DuckDBStore().getStore('observability')`, plus `MastraStorageExporter` (add `MastraPlatformExporter` to send to Mastra Platform). Exact config is in the setup-tracing skill.
- View in the Studio observability dashboard, or query via the observability store, `@mastra/client-js`, HTTP endpoints or CLI. In production always include a timestamp range in metric queries.

Related: computing-software.ai-ml-engineering.mastra.setup-tracing

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. Fixed cross-reference to setup-tracing. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
