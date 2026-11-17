---
id: computing-software.cloud-infrastructure-engineering.observability.distributed-tracing-design
name: distributed-tracing-design
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability, distributed-tracing, tracing, opentelemetry, otel, spans, span-naming, span-attributes, span-kind, span-links, semantic-conventions, async-tracing, messaging, kafka, sqs, w3c-trace-context, baggage, tail-sampling, load-balancing-exporter, otel-collector, jaeger, grafana-tempo, aws-x-ray, zipkin, honeycomb, datadog-apm, span-metrics, service-graph, critical-path]
level: advanced
status: draft
description: "Design useful traces: span granularity and naming, attributes worth adding, async messaging with span links, tail-sampling architecture in the OTel Collector, span metrics."
sources: ["OpenTelemetry documentation - Traces, semantic conventions and Collector tail sampling processor", "W3C Trace Context Recommendation", "Charity Majors, Liz Fong-Jones, George Miranda - Observability Engineering (O'Reilly)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Distributed tracing design — spans that explain latency and failure

**Goal:** traces where any slow or failed request can be followed across services and queues,
spans carry the attributes needed to group and compare them, and the sampling keeps the
interesting traces at a cost you can pay.

Baseline plumbing (OTel SDKs, propagation everywhere, head vs tail sampling in principle) is in
`computing-software.cloud-infrastructure-engineering.observability.instrumentation-strategy`.
This skill designs the traces themselves.

## 1. Span granularity
- One span per **unit of work that can be slow or fail independently**: inbound request,
  outbound HTTP/gRPC call, DB query, cache call, queue publish/consume, significant in-process
  step (template render, model inference).
- Don't span every function — 500-span traces are slow to load and expensive; use span
  events for points in time (retry attempt, cache miss) instead of child spans.
- Auto-instrumentation gives the edges; add manual spans for business steps auto-instrumentation can't see.

## 2. Naming and kind
- Span names are **low-cardinality**: `GET /orders/{id}`, `SELECT orders`, `orders process` —
  never with IDs or raw SQL. High-cardinality names explode span-metrics and break grouping.
- Set `SpanKind` correctly (SERVER, CLIENT, PRODUCER, CONSUMER, INTERNAL); backends build service graphs from it.
- Follow OTel semantic conventions (`http.request.method`, `http.response.status_code`, `db.system`, `messaging.system`) so tooling works without custom mapping. Note conventions were renamed across versions — pin a version.

## 3. Attributes worth the bytes
High-cardinality attributes are fine on spans (that's their strength): `user.id` or a hashed
equivalent, `tenant.id`, `order.id`, feature-flag variants, build/version, region/AZ, cache hit,
retry count, payload size. These let you ask "are slow checkouts all one tenant / one version?"
Never put secrets, tokens or raw personal data in attributes; hash or omit.
Record errors with `span.recordException` and status `ERROR` only for real failures (not 404s that are expected).

## 4. Async and messaging
- Inject trace context into message headers/attributes on publish (PRODUCER span); extract on consume.
- For one message → one consumer, the consumer span can be a child. For **batch consumes** or fan-in, start a new trace per batch and add **span links** to each message's context — parent/child would misrepresent timing.
- Long-running workflows (minutes-days): link traces per step instead of one giant trace; carry a business correlation ID as an attribute.
- Use **baggage** sparingly to propagate tenant or request-class to downstream services; it is sent on every hop and visible to third parties if you call out — strip at egress.

## 5. Tail-sampling architecture
Tail sampling needs all spans of a trace on the same collector:
```yaml
# tier 1 (agents/gateways): route by trace ID
exporters:
  loadbalancing:
    routing_key: traceID
    resolver: { dns: { hostname: otel-sampler-headless } }
# tier 2 (samplers)
processors:
  tail_sampling:
    decision_wait: 10s
    policies:
      - { name: errors,  type: status_code, status_code: { status_codes: [ERROR] } }
      - { name: slow,    type: latency,     latency: { threshold_ms: 1000 } }
      - { name: base,    type: probabilistic, probabilistic: { sampling_percentage: 5 } }
```
Size `decision_wait` above your p99 trace duration; spans arriving later are decided without the rest. Generate **span metrics** (RED per span name) *before* sampling (spanmetrics connector) so rates are accurate.

## Gotchas
- A missing propagation hop (an old proxy, a queue without headers) splits traces silently; test end-to-end with a known request.
- Clock skew between hosts makes child spans appear before parents; rely on durations within a host.
- Sampling inconsistently across services (each deciding independently with head sampling) gives broken traces; honour the parent's sampled flag.
- Unbounded attribute values (full request bodies) blow up storage; set attribute length limits in the SDK.

## Verify
- [ ] A test request traverses every hop including queues as one trace (or linked traces).
- [ ] Span names are low-cardinality; span-metrics series count is stable.
- [ ] Key business attributes (tenant, version, region) are present on server spans.
- [ ] Error and slow traces are kept at ~100%; baseline sampled.
- [ ] No secrets or raw PII in attributes (spot-checked).

Uncertain: config keys follow the OTel Collector contrib processors as documented; verify against your collector version.
