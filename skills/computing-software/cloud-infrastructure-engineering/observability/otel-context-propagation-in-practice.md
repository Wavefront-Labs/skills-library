---
id: computing-software.cloud-infrastructure-engineering.observability.otel-context-propagation-in-practice
name: otel-context-propagation-in-practice
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [context-propagation, propagator-configuration, otel-propagators-env, b3-propagator, manual-inject-extract, carrier-propagation, baggage-usage, baggage-span-processor, messaging-propagation, kafka-header-propagation, async-context, cross-thread-context, trace-context-through-proxies, load-balancer-trace-headers]
level: advanced
status: gated
description: "Fix broken traces: configure propagators, inject/extract over Kafka and custom carriers, carry context across threads, use baggage safely, keep headers via proxies."
sources: ["https://opentelemetry.io/docs/concepts/context-propagation/", "https://opentelemetry.io/docs/specs/otel/context/api-propagators/", "https://opentelemetry.io/docs/specs/otel/baggage/api/", "https://www.w3.org/TR/trace-context/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Context propagation in practice

## Propagators
`OTEL_PROPAGATORS=tracecontext,baggage` is the usual setting. Mixed estates can add `b3multi` or `b3`; the spec also lists `jaeger` (marked Deprecated) and `xray`. Every service in the path must understand at least one common format.

## Manual inject/extract (Python, Kafka) (gated: unconfirmed, source is paywalled or blocked)
```python
from opentelemetry import trace, propagate, context
tracer = trace.get_tracer("orders")
# producer
with tracer.start_as_current_span("publish orders", kind=trace.SpanKind.PRODUCER):
    headers = {}
    propagate.inject(headers)                         # writes the configured propagators' headers
    producer.send("orders", value=payload, headers=[(k, v.encode()) for k, v in headers.items()])
# consumer
carrier = {k: v.decode() for k, v in msg.headers}
ctx = propagate.extract(carrier)
with tracer.start_as_current_span("process orders", context=ctx, kind=trace.SpanKind.CONSUMER):
    handle(msg)
```
Same pattern for any carrier: a propagator's Inject and Extract write to and read from a carrier you define. Manual propagation is for custom transports.

## Async and threads
Context does not cross thread or task boundaries by itself in most runtimes. Pass or capture the current context explicitly when you hand work to another thread or queue; each language's context API documents how.

## Baggage
Key-value pairs propagated to downstream services (`baggage: tenant=acme,plan=gold`). Baggage names and values are case sensitive in language APIs. Do not put secrets or PII in baggage: it is sent on outbound requests, including to third parties.

## Proxies and load balancers
- Proxies must forward the `traceparent` and `tracestate` headers (W3C Trace Context); allowlist them if a gateway strips unknown headers.
- A proxy or load balancer that does its own tracing may use a different propagation format: make sure it matches the apps.
- Decide whether to trust incoming trace context at the edge.

## Verify
- [ ] A request through gateway -> service -> Kafka -> consumer shows as one trace.
- [ ] No orphan root spans in services that should always have a parent.

## Checked
- 2026-10-28. Checked against the OpenTelemetry context-propagation concept page, the propagators API and Baggage API specs, the SDK environment variables page and the W3C Trace Context page.
- Confirmed: `OTEL_PROPAGATORS` values (`tracecontext`, `baggage`, `b3`, `b3multi`, `jaeger` deprecated, `xray`), Inject/Extract on carriers, `traceparent`/`tracestate` headers, baggage case sensitivity.
- Removed (unconfirmed): "extracts the first present" composite behaviour, per-language thread-context recipes, baggage span processor, `TRACEPARENT` env var, ALB/GCP header names, Istio defaults.
- Gated: the Python `propagate.inject/extract` and `start_as_current_span(kind=...)` sample was not found in the fetched pages; it is kept as an illustration only.
Method: documentation only; no commands were run.
