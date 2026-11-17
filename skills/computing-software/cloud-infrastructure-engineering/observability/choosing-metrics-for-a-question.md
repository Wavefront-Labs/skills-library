---
id: computing-software.cloud-infrastructure-engineering.observability.choosing-metrics-for-a-question
name: choosing-metrics-for-a-question
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [when-to-use-metrics, metrics-selection, telemetry-signals, signal-selection, cardinality]
level: practitioner
status: draft
description: "Decide whether a monitoring question should be answered by a metric: aggregatable, cheap, bounded cardinality, alertable. Includes test questions and anti-patterns."
sources: ["https://prometheus.io/docs/practices/instrumentation/", "https://opentelemetry.io/docs/concepts/signals/metrics/", "https://sre.google/sre-book/monitoring-distributed-systems/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing metrics for a question

Metrics are numbers pre-aggregated at the source and stored as time series. They are the cheapest signal per
event (cost is per series, not per request) and the only one you should page on directly.

## Use a metric when all of these hold
1. **The answer is a number over time**: rate, ratio, latency distribution, queue depth, saturation.
2. **You will aggregate it**: sum across pods, ratio errors/requests, quantile over a histogram.
3. **Dimensions are bounded**: every label has a small, known value set (method, status class, route template,
   region). Rule of thumb: under 10 values per label, under ~1,000 series per metric per target.
4. **You need it for alerting, SLOs or long-range trends**: metrics are retained for months cheaply.

## Do not use a metric when
- The key dimension is unbounded: user ID, request ID, email, full URL path, SQL text, error message. Put that
  in logs/wide events or span attributes; a metric with `user_id` label creates one series per user.
- You need the individual event ("which request failed and why") - metrics lose identity on aggregation.
- The event is rare and you need its details (a deploy, a config change) - use an annotation/event log.

## Decision test
Write the PromQL or alert you expect to run *before* adding the metric. If you cannot write
`sum by (x) (rate(m[5m]))` or `histogram_quantile(...)` that answers a real question, you probably want a log.

## Picking the type
| Question | Type |
|---|---|
| How many / how fast | Counter (`_total`), query with `rate()` |
| Current level (queue depth, temperature, in-flight) | Gauge |
| How long / how big, need percentiles across instances | Histogram (native or classic buckets) |
| Per-instance quantile only, cannot aggregate | Summary (rarely the right choice) |

## Anti-patterns
- Encoding events as gauges set to 1 (use counters, or logs).
- Pre-computing percentiles in the app and exporting them as gauges - they cannot be averaged across instances.
- One metric per variant (`http_requests_get_total`) instead of a label.
- Exporting a metric "just in case": each series costs memory in every Prometheus/Mimir replica forever.

## Verify
`count by (__name__)({__name__="my_metric"})` for series count, and check the dashboard/alert that consumes it exists.
