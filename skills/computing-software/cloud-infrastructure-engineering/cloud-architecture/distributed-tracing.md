---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.distributed-tracing
name: distributed-tracing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, performance-engineering, distributed-tracing, opentelemetry-tracing, trace-context, span-analysis, critical-path, x-ray, application-insights]
level: practitioner
status: draft
description: "Use distributed tracing to find latency: instrumenting with OpenTelemetry, context propagation, sampling choices, reading critical paths, and spotting N+1 and fan-out issues."
sources: ["https://opentelemetry.io/docs/concepts/signals/traces/", "https://www.w3.org/TR/trace-context/", "https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Distributed tracing for latency analysis

## Instrumentation
1. OpenTelemetry auto-instrumentation for HTTP servers/clients, gRPC, DB drivers, messaging.
2. Manual spans around significant internal work (serialisation, external calls without plugins).
3. Propagate **W3C Trace Context** (`traceparent`, `tracestate`) across HTTP and message headers
   (inject into message attributes for queues).
4. Resource attributes: `service.name`, `service.version`, `deployment.environment`.

## Sampling
- Head-based (e.g. 5-10%) for cost; parent-based to keep traces complete.
- Tail-based at the collector to keep all errors and slow traces (policy: latency > 1 s, status error).

## Reading traces
- **Critical path**: the chain of spans that determines end-to-end time; optimise there only.
- **N+1**: many identical sequential DB spans per request -> batch or join.
- **Sequential fan-out** that could be parallel.
- **Gaps** between spans: uninstrumented work, queueing, GC, thread pool waits.
- **Retries** visible as repeated client spans.
- Compare p50 vs p99 traces using exemplars linked from latency histograms.

## Gotchas
- Broken context across async boundaries (thread pools, queues) yields orphan traces.
- High-cardinality span attributes are fine; high-cardinality metric labels aren't - keep detail in traces.

## Verify
- [ ] A sampled slow request shows complete spans from edge to DB.
