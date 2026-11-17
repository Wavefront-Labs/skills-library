---
id: computing-software.cloud-infrastructure-engineering.observability.metrics-vs-logs-vs-traces-tradeoffs
name: metrics-vs-logs-vs-traces-tradeoffs
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability, metrics, logs, traces, three-pillars, wide-events, telemetry-signals, signal-selection, cardinality, dimensionality, aggregation, sampling, cost-of-observability, retention, exemplars, span-metrics, log-derived-metrics, profiles, continuous-profiling, events, observability-2-0, telemetry-budget, prometheus, honeycomb, datadog, grafana-stack]
level: practitioner
status: draft
description: "Choose the right signal per question: what metrics, logs, traces and wide events each answer, their cost and cardinality limits, converting between them, and a per-service telemetry budget."
sources: ["Charity Majors, Liz Fong-Jones, George Miranda - Observability Engineering (O'Reilly)", "OpenTelemetry documentation - Signals", "Prometheus documentation - Instrumentation best practices"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Metrics vs logs vs traces — pick the signal that answers the question

**Goal:** each question you need to answer about a system is backed by the cheapest signal
that can answer it, and you know when to convert one signal into another instead of
collecting everything three times.

## 1. What each signal is good at
| Signal | Shape | Strength | Weakness | Cost driver |
|---|---|---|---|---|
| **Metrics** | pre-aggregated numbers over time, few labels | cheap, fast, long retention; alerting and trends | can't drill to an individual request; cardinality explodes with labels | number of active series (label combinations) |
| **Logs** | discrete records, free-form or structured | full detail of one event; audit; debugging the unexpected | expensive at volume; counting/aggregating is slow | bytes ingested and indexed |
| **Traces** | causally linked spans per request | latency breakdown across services; "where did the time go" | sampled; weak for aggregates unless span-metrics are derived | spans stored (× sampling rate) |
| **Wide events** (one rich structured event per request/unit of work) | many high-cardinality fields | arbitrary slicing after the fact ("which tenant on which build?") | needs a columnar store built for it | events × width |
| **Profiles** | CPU/memory stacks over time | why code is slow or allocating | language/runtime-specific | sample rate |

## 2. Map questions to signals
- "Is the service healthy right now? Page me if not." → **metrics** (SLI counters, burn rate).
- "Which dependency made this request slow?" → **traces**.
- "Why did *this* order fail?" → **logs** (or a trace with events), found via trace_id/order_id.
- "Is the latency regression confined to one tenant, region or version?" → **wide events / traces with rich attributes**; metrics only if you pre-guessed the label.
- "What did user X do, for an auditor, 2 years later?" → **audit logs**, immutable, long retention.
- "Why is CPU higher after the deploy?" → **profiles**.

## 3. Cardinality is the main design constraint
- Metric label values multiply: 50 endpoints × 5 status classes × 200 pods = 50,000 series for one metric. Add `customer_id` and it's millions — most TSDBs and vendors bill or fall over here.
- Rule: metrics get **bounded** labels (endpoint template, status class, region); unbounded dimensions (user, order, request ID) go on traces/logs/events.
- Exemplars bridge the two: a metric bucket carries a sample trace ID, so a latency spike links to a concrete slow trace.

## 4. Convert rather than duplicate
- **Span metrics** (OTel spanmetrics connector, vendor APM): RED metrics derived from 100% of spans before sampling — no separate request counters needed.
- **Log-derived metrics** (Loki recording rules, CloudWatch metric filters): fine for legacy apps you can't instrument; slower and costlier than native counters.
- **Traces from logs:** not reliably possible — propagate context at the source.

## 5. Set a telemetry budget per service
Typical starting proportions (adjust): metrics for all SLIs and resource saturation; traces
with ~100% errors/slow + a few % baseline; logs at INFO for business events and errors only.
Review monthly: cost per signal per service, and which dashboards/queries actually used each. Delete what nobody queried in 90 days.

## Gotchas
- "Three pillars" thinking leads to three disconnected tools; the value is in **joining** them (shared service names, trace_id in logs, exemplars).
- Averages in metrics hide bimodal latency; use histograms.
- Sampled traces can't count; never compute error rates from sampled spans without weighting.
- Debug logs as a substitute for tracing creates the most expensive tracing system possible.
- Vendor pricing differs by signal (per host, per series, per GB, per span); the cheapest design depends on your contract.

## Verify
- [ ] Each alert is backed by a metric, not a log query (or the exception is documented).
- [ ] No unbounded identifier is used as a metric label.
- [ ] Logs and traces share trace_id; metrics carry exemplars where supported.
- [ ] Cost per signal per service is reported and reviewed monthly.
- [ ] Unused dashboards, metrics and log streams are pruned on a schedule.

Related: computing-software.cloud-infrastructure-engineering.observability.instrumentation-strategy, computing-software.cloud-infrastructure-engineering.observability.distributed-tracing-design
