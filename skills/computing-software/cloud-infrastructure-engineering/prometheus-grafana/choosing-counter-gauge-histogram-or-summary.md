---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.choosing-counter-gauge-histogram-or-summary
name: choosing-counter-gauge-histogram-or-summary
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [metric-type-selection, counter-vs-gauge, instrumentation, histogram-vs-summary, data-model]
level: practitioner
status: docs-checked
description: "Decide which Prometheus metric type to use for a measurement with a decision table, naming consequences and the queries each type enables."
sources: ["https://prometheus.io/docs/practices/instrumentation/", "https://prometheus.io/docs/concepts/metric_types/", "https://prometheus.io/docs/practices/histograms/", "https://prometheus.io/docs/practices/naming/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing the metric type

The instrumentation page's rule of thumb: if the value can go down, it is a gauge. Counters can only go up (and reset, such as when a process restarts). Summaries and histograms are for distributions.

## Decision table
| Measuring | Type | Name | Query |
|---|---|---|---|
| Things that happened (requests, bytes sent) | Counter | `*_total` (for example `http_requests_total`; with a unit, `process_cpu_seconds_total`) | `rate()` for the per-second rate |
| Current level (in-progress requests, free memory, temperature) | Gauge | unit suffix, plural (`node_memory_usage_bytes`) | raw value; never `rate()` a gauge |
| Durations or sizes you need quantiles of, aggregated across instances | Histogram (prefer native if the client library supports it) | `*_seconds`, `*_bytes` | `histogram_quantile()` |
| Per-instance quantiles only, no aggregation needed | Summary | `*_seconds` | read the `quantile` label series directly |
| Time something last happened | Gauge holding a Unix timestamp | for example `..._timestamp_seconds` | `time() - my_timestamp_metric` |
| Metadata about the running binary | Pseudo-metric named `*_build_info` | `foobar_build_info` | n/a |

## Rules from the pages
- Counter: use for cumulative event counts or amounts; raw counters are rarely useful, so use `rate()`. Do not use a counter for a value that can decrease (the metric types page: use a gauge for the number of currently running processes).
- Gauge: snapshots of state (in-progress requests, free/total memory, temperature).
- Histogram: observations counted in buckets plus a sum. Native histograms (Go and Java client libraries) are preferred over classic histograms and summaries: no bucket boundaries to pick, always aggregatable, one series. A classic histogram is `_bucket{le=...}` (cumulative), `_sum` and `_count`.
- Summary: streaming quantiles computed in the instrumented program over a sliding window, plus `_sum` and `_count`. Quantiles and window must be chosen at instrumentation time, and quantiles cannot be aggregated (averaging a `quantile="0.95"` series across replicas is statistically meaningless).
- Fleet-wide quantile from a classic histogram: `histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))`; from a native histogram: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds[5m])))`.
- Fraction of observations in a range (native histograms): `histogram_fraction(0, 0.3, sum by (job) (rate(http_request_duration_seconds[5m])))`.
- Average from either type: rate of `_sum` divided by rate of `_count` (native: `histogram_avg(rate(...))`). A quantile-less summary (just `_sum` and `_count`) is a legitimate use of a summary.
- Rule of thumb on the histograms page: use native histograms if available; if you need aggregation without them, use classic histograms with well-chosen buckets; consider a summary only if aggregation is not needed.

## Gotchas
- A classic histogram is one series per bucket plus `_sum` and `_count`; more buckets give more accuracy at significant series cost. Classic bucket boundaries are fixed at instrumentation, and `le="0.3"` style queries return nothing if no bucket has that exact boundary.
- Negative observations can make `_sum` go down, which `rate()` treats as a counter reset and skews the result (summaries and classic histograms only).
- Use base units (seconds, bytes, ratio 0-1), not milliseconds or megabytes; one unit and one quantity per metric name.
- Do not put label names in metric names, and do not use high-cardinality values (user IDs, email addresses) as labels. The instrumentation page suggests keeping label cardinality below 10 for most metrics.
- Export a count of failures together with a total-attempts metric so the failure ratio is easy to compute.

## Verify
- [ ] Every counter is queried through `rate()` (or another range function), never raw, in dashboards and alerts.
- [ ] Every gauge is never wrapped in `rate()`.
- [ ] Metric names carry a unit suffix in base units, and accumulating counts end in `_total`.

## Checked
Date: 2026-11-07. Read in full: the Prometheus instrumentation practices page (counter vs gauge rule, failures, labels, timestamps-not-time-since), the metric types concepts page, the histograms and summaries page (count/sum, bucketing, quantile table, rules of thumb) and the metric and label naming page (suffixes, base units, `_build_info`, timestamp example). Trims: removed `increase()`, `avg_over_time`/`max_over_time`, "gauge = 1 with `group_left` join" for info metrics, the claim that a gauge "loses data between scrapes", the "sum/count is cheaper than a summary with quantiles" claim and the `promtool check metrics` verify, none of which these pages state. Added the negative-observation `_sum` caveat, native-histogram preference and the naming rules from the pages read.
Method: documentation only; no commands were run.
