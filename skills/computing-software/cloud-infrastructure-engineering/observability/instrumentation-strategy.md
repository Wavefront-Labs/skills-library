---
id: computing-software.cloud-infrastructure-engineering.observability.instrumentation-strategy
name: instrumentation-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability, instrumentation, opentelemetry, otel, otel-collector, otlp, red-method, use-method, golden-signals, metrics, structured-logging, json-logs, distributed-tracing, w3c-trace-context, traceparent, exemplars, head-sampling, tail-sampling, cardinality, semantic-conventions, jaeger, tempo, datadog, honeycomb]
level: practitioner
status: draft
description: "Plan service instrumentation: RED for requests and USE for resources, OpenTelemetry SDKs and Collector, structured logs with trace IDs, context propagation, sampling and cardinality limits."
sources: ["OpenTelemetry documentation - concepts, semantic conventions and Collector", "W3C Trace Context Recommendation", "Google SRE Book ch. 6 Monitoring Distributed Systems", "Brendan Gregg - The USE Method"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Instrumentation strategy — signals you can join, at a cost you can afford

**Goal:** every service emits consistent metrics, logs and traces through OpenTelemetry,
linked by trace ID, so an alert leads to the failing request and its log lines within
minutes — without blowing up storage bills.

## 1. Decide what to measure
- **RED** for every request-driven component: **R**ate, **E**rrors, **D**uration
  (as a histogram). Per endpoint/route, per dependency call.
- **USE** for every resource (CPU, memory, disk, connection pools, queues, thread pools):
  **U**tilisation, **S**aturation (queue length, wait time), **E**rrors.
- Golden signals (latency, traffic, errors, saturation) are the same idea for SLOs.
- Business events (orders placed, payments failed) as counters; they detect breakage tech metrics miss.

## 2. OpenTelemetry as the plumbing
- Use the OTel SDK plus auto-instrumentation (Java agent, Python `opentelemetry-instrument`,
  Node `@opentelemetry/auto-instrumentations-node`, .NET, Go via libraries/eBPF) to get HTTP,
  gRPC, DB and messaging spans and metrics for free; add manual spans around business logic.
- Configure with standard env vars:
  ```bash
  OTEL_SERVICE_NAME=checkout
  OTEL_RESOURCE_ATTRIBUTES=service.version=1.42.0,deployment.environment.name=prod
  OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
  OTEL_TRACES_SAMPLER=parentbased_traceidratio
  OTEL_TRACES_SAMPLER_ARG=0.1
  ```
- Send OTLP to an **OpenTelemetry Collector** (agent per node + gateway tier), not directly
  to vendors. The Collector does batching, retries, `memory_limiter`, attribute redaction,
  `k8sattributes` enrichment and fan-out to any backend — your vendor becomes swappable.
- Follow **semantic conventions** (`http.request.method`, `http.response.status_code`,
  `url.path`, `db.system`) so dashboards and backends understand data uniformly. Several
  conventions were renamed when HTTP semconv stabilised; check versions when upgrading.

## 3. Structured logs that join with traces
- JSON, one event per line, fixed keys: `timestamp` (RFC 3339 UTC), `level`, `service`,
  `message`, `trace_id`, `span_id`, plus event fields. Log bridges in OTel SDKs inject IDs.
- Log events and decisions, not every function call; errors once, where handled, with stack.
- Never log secrets, tokens or personal data; redact in the app and again in the Collector.
- Levels mean something: `ERROR` = needs a human eventually; `WARN` = degraded but handled.

## 4. Propagate context everywhere
- W3C `traceparent` / `tracestate` headers (the OTel default) across HTTP and gRPC;
  `baggage` for small cross-cutting keys (tenant tier), never sensitive data.
- Messaging: inject context into message headers/attributes on publish and extract on
  consume (span links for batch consumers).
- Edge: decide whether to trust incoming `traceparent` from the internet (usually start a new trace and link).
- Metrics **exemplars** attach trace IDs to histogram buckets, so a latency spike on a
  dashboard clicks through to a slow trace.

## 5. Sampling and cost
- **Head sampling** (`parentbased_traceidratio`) is cheap but blind: 10% sampling keeps
  10% of errors too.
- **Tail sampling** in the Collector gateway (`tail_sampling` processor) keeps 100% of
  errors and slow traces plus a small percentage of the rest. Needs all spans of a trace
  on one Collector — use the `loadbalancing` exporter keyed by trace ID.
- Metrics stay unsampled; they are your accurate counts. Derive RED from spans in the
  Collector (`spanmetrics` connector) if the app does not emit them.
- Logs: sample or drop DEBUG in prod; set retention tiers (e.g. 7-14 days hot, longer in object storage).

## 6. Cardinality rules
- Metric labels: bounded sets only — route template, method, status class, region.
  Never user ID, request ID, raw URL, email. High-cardinality detail belongs on spans and logs.
- Set limits in the SDK/Collector (views to drop attributes, cardinality limits) and alert on series growth.

## Gotchas
- Mixed propagators (B3 in one service, W3C in another) silently break traces; set `OTEL_PROPAGATORS=tracecontext,baggage` (add `b3` only when bridging).
- Async work (thread pools, goroutines, callbacks) loses context unless explicitly passed.
- Auto-instrumentation can double-count spans when both a framework and a library integration are active.
- `url.full` on spans may include query-string tokens; scrub before export.
- Histograms with default buckets rarely match your SLO thresholds; configure views.
- The Collector without `memory_limiter` OOMs under backpressure and drops everything.

## Verify
- [ ] Every service exposes RED metrics per route and USE metrics for its pools/queues.
- [ ] A single request can be followed across all services in one trace.
- [ ] Clicking a log line's `trace_id` opens the trace; an exemplar on a latency panel does too.
- [ ] 100% of error traces are retained under the sampling policy.
- [ ] No metric has an unbounded label; series count per service is tracked.
- [ ] Logs contain no secrets or personal data (spot-check plus Collector redaction rules).

Related: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.slos-and-error-budgets, computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-and-alert-rules
