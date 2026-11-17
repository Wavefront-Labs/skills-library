---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.trace-driven-debugging-across-services
name: trace-driven-debugging-across-services
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, troubleshooting, trace-driven-debugging, distributed-tracing, exemplars, opentelemetry]
level: advanced
status: docs-checked
description: "Debug latency and errors across services with traces: exemplars from a metric to a trace, how to read spans, status and kind, links and context propagation."
sources: ["https://opentelemetry.io/docs/concepts/signals/traces/", "https://grafana.com/docs/tempo/latest/traceql/", "https://grafana.com/docs/grafana/latest/fundamentals/exemplars/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trace-driven debugging

**Goal:** go from an aggregate symptom (latency up) to the specific request path and span responsible.

## From metric to trace (Grafana exemplars)
- An exemplar is a specific trace representative of a measurement in a time interval. Metrics give an aggregate view,
  traces a fine-grained view of one request, and exemplars link the two.
- To find what contributes to latency you compare a trace for a fast response against one for a slow response; with
  production data volumes that is laborious, and exemplars help by pinpointing traces with high latency within an
  interval. Then combine the trace with other system or location properties for faster root cause analysis.
- In Grafana, exemplar support is for the Prometheus data source only and must be enabled; exemplars show as stars
  next to the metric in Explore and dashboards, and hovering shows the trace ID. From Loki logs, a derived field with a
  regular expression can extract `traceID` so a log line links to the trace.
- In the trace view, the top strip shows the whole trace across all levels from client to database query, giving a view of
  time distribution; you can magnify a segment and expand or collapse levels to reach the span of interest, and click a
  span for its metadata.

## Reading a trace (OpenTelemetry)
- A trace is spans linked by `trace_id` and `parent_id`; the root span has no parent. A span has a name, parent span ID,
  start and end timestamps, span context, attributes, events, links and status. Each span looks like a structured log
  with context and hierarchy, and may come from different processes, services, VMs or datacenters.
- Context propagation is what lets spans from different places be assembled into one trace. Broken propagation is
  therefore a reason a trace is incomplete.
- Span status is `Unset` (finished without error), `Error`, or `Ok` (explicitly marked successful by the developer). An
  `Error` status means an error occurred in the operation, for example an HTTP 500 in a server span.
- Span kind is Client, Server, Internal, Producer or Consumer. The parent of a server span is often a remote client span;
  the child of a client span is usually a server span. Producer and consumer spans cover asynchronous jobs, and the
  consumer may start long after the producer ended.
- Span links associate a span with other spans causally, for example linking a queued asynchronous operation's trace to
  the trace that caused it, because its start time cannot be predicted.
- Attributes should be added at span creation where possible so they are available to SDK sampling.

## Querying (Grafana Tempo)
TraceQL is Tempo's language for selecting traces, with syntax similar to PromQL and LogQL where possible; traces have a
tree structure with timestamps and arbitrary key/value data, and the page says it can be used for root cause analysis of
an outage. TraceQL metrics generate metrics from traces. Traces Drilldown lets you investigate without writing queries.
Read the TraceQL language reference for exact query syntax; it is not on the overview page.

## Verify
- [ ] Incident notes cite trace IDs for a slow and a fast request and the span that differs.
- [ ] Context propagation is intact across every hop on the request path, including queues (links).

## Checked

Checked 2026-11-09. Confirmed against the OpenTelemetry Traces concept page, the Tempo TraceQL overview and the Grafana
exemplars introduction. Removed: the SRE Book Effective Troubleshooting source (not used), both TraceQL query examples
(syntax not on the overview page), critical-path reading rules, N+1 and gap heuristics, the tail sampling advice, clock
skew advice and the span profiles pivot, none of which appeared on the pages read.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.
