---
id: computing-software.cloud-infrastructure-engineering.observability.correlation-id-and-business-transaction-id-design
name: correlation-id-and-business-transaction-id-design
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [correlation-id-design, business-transaction-id, trace-id-in-logs, w3c-trace-context, baggage, logging]
level: practitioner
status: draft
description: "Decide when a trace id is enough and when you need a separate correlation or business transaction id (orders, jobs, async workflows) and how to carry it."
sources: ["https://www.w3.org/TR/trace-context/", "https://opentelemetry.io/docs/concepts/signals/baggage/", "https://opentelemetry.io/docs/specs/otel/trace/api/#link"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Correlation ids vs trace ids

## Rules
- A trace id identifies one request tree. Use it for request-level correlation; it is generated and propagated by OTel (`traceparent`).
- A business transaction id (order_id, job_id, payment_id) spans many traces over minutes or days: retries, async workers, scheduled follow-ups. Log it and put it as a span attribute; do not try to stretch one trace across days.
- Legacy `X-Request-ID`/`X-Correlation-ID`: keep accepting and logging it at the edge, but map it to the trace (attribute `http.request.header.x-request-id`) rather than maintaining a parallel propagation system.

## Carrying a business id
- Span attribute on the root span of each trace touching the entity: `app.order.id`.
- Log field on every log line inside those traces (MDC/contextvars).
- Across async hops where the next trace starts fresh, add a span **link** to the producing span plus the business id attribute.
- Baggage only if downstream services need the value for their own attributes; baggage is sent on every outbound call and is visible to third parties, so never put PII in it.

## Querying
- Tempo: `{ span.app.order.id = "o-123" }` finds all traces for the order.
- Loki: `{service_name=~".+"} | json | order_id="o-123"` (or structured metadata) gives the whole lifecycle.

## Gotchas
- Business ids as metric labels explode cardinality; they belong in traces and logs only.
- Generating your own trace ids in app code breaks sampling and propagation; let the SDK do it.
- Attribute names should be namespaced (`app.`) to avoid future semconv collisions.

## Verify
- [ ] Given an order id, support can find every trace and log for it in under a minute.
- [ ] No business ids appear in metric label sets (`count by (__name__)` audit of label names).
