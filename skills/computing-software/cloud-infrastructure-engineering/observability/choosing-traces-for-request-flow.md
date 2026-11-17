---
id: computing-software.cloud-infrastructure-engineering.observability.choosing-traces-for-request-flow
name: choosing-traces-for-request-flow
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [when-to-use-traces, request-flow-analysis, telemetry-signals, signal-selection, distributed-tracing]
level: practitioner
status: draft
description: "Decide when traces answer the question: cross-service latency attribution, fan-out, dependency mapping. Covers what traces cannot do cheaply and how to combine with metrics."
sources: ["https://opentelemetry.io/docs/concepts/signals/traces/", "https://grafana.com/docs/tempo/latest/introduction/", "https://sre.google/workbook/monitoring/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing traces for request-flow questions

A trace is the tree of spans for one request across services. It answers questions about *where time and
errors went inside a request*, which neither metrics nor logs answer well.

## Use traces when the question is
- "Which hop made this request slow?" - critical path across services, queues and DB calls.
- "What does this endpoint call, and how often?" - fan-out, N+1 queries, retries, duplicate calls.
- "Is the error originating here or propagated?" - span status and exception events per hop.
- "What changed between fast and slow requests?" - compare attributes of slow vs normal spans (TraceQL, or
  Tempo/Grafana "compare" views).
- Service dependency graph / service map (derived from spans via service graph connector or metrics-generator).

## Traces are a poor fit for
- Exact counts and long-range trends when you sample (use span-derived RED metrics computed *before* sampling:
  spanmetrics connector or Tempo metrics-generator).
- Single-process debugging where a profile shows more (CPU hotspots inside one span -> use profiles).
- Batch jobs with millions of items: one trace per item is costly; trace per batch with span links instead.

## Combining
1. Alert on metrics (RED from spans or app metrics).
2. Jump from a latency spike via **exemplars** to a representative trace.
3. From the span, jump to logs filtered by `trace_id`, or to a profile via span profiles.

## Prerequisites before traces are useful
- Context propagation works across every hop (including queues and proxies) - otherwise you get broken fragments.
- Consistent `service.name` and semantic-convention span names (`GET /orders/{id}`, not raw URLs).
- A sampling strategy that keeps errors and slow traces (tail sampling) if you sample at all.

## Verify
Open a trace for a known multi-service request; there should be one root span and no orphan spans
(`{ rootServiceName = nil }`-style search, or Tempo "missing root span" counts).
