---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-avoiding-average-of-averages
name: promql-avoiding-average-of-averages
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [average-of-averages, weighted-average, aggregation, ratio-queries, promql, latency-measurement]
level: practitioner
status: verified
description: "Compute correct means and ratios across instances: sum numerators and denominators first instead of averaging per-instance averages, percentages or quantiles."
sources: ["https://prometheus.io/docs/practices/histograms/", "https://prometheus.io/docs/prometheus/latest/querying/operators/#aggregation-operators", "https://prometheus.io/docs/prometheus/latest/querying/functions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Avoiding average of averages

`avg()` over per-instance ratios weights a quiet instance the same as a busy one. Aggregate the parts, then divide.

## Mean latency
```promql
# wrong: average of per-instance means
avg(rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m]))
# right: total time / total requests
sum(rate(http_request_duration_seconds_sum[5m])) / sum(rate(http_request_duration_seconds_count[5m]))
```

## Error ratio
```promql
# wrong
avg by (job) (rate(errors_total[5m]) / rate(requests_total[5m]))
# right
sum by (job) (rate(errors_total[5m])) / sum by (job) (rate(requests_total[5m]))
```

## CPU utilisation across nodes of different sizes
```promql
# wrong: average of per-node percentages (2-core and 64-core nodes weighted equally)
avg(1 - avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))
# right: busy cores / total cores
sum(rate(node_cpu_seconds_total{mode!="idle"}[5m])) / count(node_cpu_seconds_total{mode="idle"})
```

## Quantiles
- Averaging p99s across instances is meaningless; aggregate histogram buckets: `histogram_quantile(0.99, sum by (le) (rate(x_bucket[5m])))`.
- Summaries cannot be aggregated at all: change to histograms.

## Over time
`avg_over_time(ratio[1d])` weights each evaluation equally regardless of traffic; for SLIs use `sum(increase(errors[1d])) / sum(increase(requests[1d]))`.

## Checked
Prometheus 3.15.0 with one instance averaging 0.1 s per request on 10 requests per minute and another averaging 1 s on 1000: the `avg(sum/count)` form returned 0.55 s, the `sum(sum)/sum(count)` form 0.99 s. With instance 1 at 100% errors on 1 request/min and instance 2 at 0% on 10: `avg by (job)` of ratios returned 0.5, summed numerator over summed denominator 0.0909. Summaries cannot be aggregated into quantiles (docs: prometheus.io/docs/practices/histograms).

## Verify
- [ ] Fleet-level ratio panels use summed numerators and denominators (review queries containing `avg(` over a division).
