---
id: computing-software.cloud-infrastructure-engineering.linkerd.distributed-tracing-proxy-spans
name: distributed-tracing-proxy-spans
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, distributed-tracing, spans, collector, observability]
level: advanced
status: docs-checked
description: "Know what Linkerd contributes to distributed tracing and what the application and collector must provide."
sources:
  - https://linkerd.io/2.19/features/distributed-tracing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Linkerd's role in tracing is simple: when a proxy sees a tracing header on a proxied HTTP request, it emits a trace span that records the exact time spent in the proxy. Unlike most Linkerd features, tracing needs code changes and configuration.

You must provide:

- an ingress layer that starts the trace on selected requests
- a client library in the application, or another mechanism to propagate trace headers
- a trace collector that turns span data into traces
- a trace backend that stores the data and lets users query it

Much of what is often credited to tracing needs none of this in Linkerd:

- live service topology and dependency graphs
- aggregated service health, latencies and request volumes
- aggregated path or route health, latencies and request volumes

So start with the dashboard and per-route metrics, and add tracing when you need per-request timing across several services.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/features/distributed-tracing/.

Removed or reworded: Two inferred statements (no spans without components; broken-trace behaviour).

Method: documentation only; no commands were run.
