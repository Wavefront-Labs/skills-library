---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.estimating-cardinality-before-shipping-a-metric
name: estimating-cardinality-before-shipping-a-metric
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [cardinality-estimation, series-count-estimate, cardinality, metric-naming, histogram-buckets, capacity-planning]
level: practitioner
status: verified
description: "Estimate series count for a new metric (labels x values x instances x buckets) before merging, and compare the estimate with TSDB stats after rollout."
sources: ["https://prometheus.io/docs/practices/instrumentation/#do-not-overuse-labels", "https://prometheus.io/docs/prometheus/latest/querying/api/#tsdb-stats", "https://prometheus.io/docs/practices/naming/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Estimating cardinality before shipping

## Formula
series = product(distinct values per label) x instances x series-per-metric
- series-per-metric: counter/gauge 1; classic histogram = buckets + 1 (`+Inf`) + `_sum` + `_count`; summary = quantiles + 2.
- Use realistic distinct values, not the theoretical maximum, but also state the worst case.

## Example
`http_request_duration_seconds` histogram, 12 buckets, labels route (40), method (4 but only ~1.5 per route in practice), code class (5), 30 pods:
- per pod: 40 x 1.5 x 5 x (12+3) = 4,500
- fleet: 4,500 x 30 = 135,000 series
Dropping `method` (route implies method) and using native histograms (1 series per label set) gives 40 x 5 x 30 = 6,000.

prometheus.io guidance (instrumentation practices): try to keep the cardinality of your metrics below 10, limit the metrics that exceed that to a handful across the whole system, and investigate alternatives above 100.

## After rollout, compare
```promql
count({__name__="http_request_duration_seconds_bucket"})
count by (route) (http_request_duration_seconds_count)   # distinct values reality check
```
`/api/v1/status/tsdb` (`seriesCountByMetricName`) or `promtool tsdb analyze` for top metrics.

## Gotchas
- Pod churn multiplies: each deploy creates a new set of series (`instance`/`pod` change). Count series over a day, not just head series at one moment, when budgeting.
- Labels that are correlated (route and method) do not multiply fully; uncorrelated ones do.
- Exemplars do not add series; adding a label "for debugging" does.

## Verify
- [ ] PR includes the estimate; post-deploy actual within 2x of estimate.
