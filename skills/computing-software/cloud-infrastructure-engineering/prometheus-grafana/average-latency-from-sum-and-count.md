---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.average-latency-from-sum-and-count
name: average-latency-from-sum-and-count
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [average-latency-sum-count, sum-over-count, latency-measurement, promql-histograms, histogram-avg]
level: practitioner
status: verified
description: "Compute mean latency or size from histogram/summary _sum and _count (or histogram_avg for native histograms), aggregate it correctly and know its limits."
sources: ["https://prometheus.io/docs/practices/histograms/", "https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_avg", "https://prometheus.io/docs/concepts/metric_types/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Average latency from _sum and _count

prometheus.io histograms practice: the average request duration over the last 5 minutes is
```promql
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])
```
Works for histograms and summaries.

## Aggregated
```promql
sum by (route) (rate(http_request_duration_seconds_sum[5m]))
/ sum by (route) (rate(http_request_duration_seconds_count[5m]))
```
Native histograms: `histogram_avg(sum by (route) (rate(http_request_duration_seconds[5m])))`.

## When average is right
- Throughput/capacity: total time spent (`sum(rate(_sum))`) = busy workers needed (Little's law: concurrency = arrival rate x mean latency).
- Cheap trend line when buckets are not available (summary without quantiles).

## When it misleads
- Tail behaviour: a mean can stay flat while p99 doubles. Pair with quantiles or `histogram_fraction` for SLOs.
- No traffic gives `NaN` (0/0): a promtool test with flat `_sum` and `_count` returned `NaN`.

## Gotchas
- Divide sums and counts of the same label sets; averaging per-instance averages is wrong.
- `_sum` can decrease if negative observations exist (not for durations); then `rate` treats it as a reset.

## Verify
- [ ] Little's law check: `sum(rate(_sum[5m]))` approximates average in-flight requests metric where available.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), client_golang 1.25.0 on Go 1.26.
- promtool test: `_sum` rising 10 per minute and `_count` 5 per minute gave `rate(sum)/rate(count)` = 2; flat series gave `NaN`.
- Live: a Go histogram with exponentially distributed observations (mean 0.1): `rate(_sum)/rate(_count)` 0.106 (classic and native jobs), `sum by (job) (rate(_sum))/sum by (job) (rate(_count))` 0.102, `histogram_avg(rate(x[20s]))` on the native-only job 0.103.
- The formula, its use for summaries and the `_sum` negative-observation caveat: Prometheus histograms-and-summaries practice page. `histogram_avg` and its equivalence to `histogram_sum / histogram_count`: 3.15 functions page. Little's law is arithmetic.
