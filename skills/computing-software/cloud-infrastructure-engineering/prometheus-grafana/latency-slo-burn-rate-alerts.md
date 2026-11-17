---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.latency-slo-burn-rate-alerts
name: latency-slo-burn-rate-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [latency-slo-alerting, latency-burn-rate, histogram-fraction, slo-based-alerting, burn-rate, promql-histograms]
level: advanced
status: verified
description: "Alert on latency SLO burn with histogram buckets (fraction of requests slower than a threshold) or histogram_fraction for native histograms."
sources: ["https://sre.google/workbook/alerting-on-slos/", "https://prometheus.io/docs/practices/histograms/", "https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_fraction"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Latency SLO burn-rate alerts

Turn latency into a ratio: SLI = requests faster than T / all requests. Then burn-rate maths is identical to availability.

## Classic histogram (bucket boundary at T must exist)
```yaml
- record: slo:sli_latency_bad:ratio_rate1h
  expr: |
    1 - (
      sum(rate(http_request_duration_seconds_bucket{job="api", le="0.3"}[1h]))
      / sum(rate(http_request_duration_seconds_count{job="api"}[1h]))
    )
```
SLO "99% of requests under 300ms" means error budget = 1%; fast-burn page when `ratio_rate1h > 14.4 * 0.01 and ratio_rate5m > 14.4 * 0.01`.

## Native histogram
```promql
1 - histogram_fraction(0, 0.3, sum(rate(http_request_duration_seconds{job="api"}[1h])))
```
Any threshold works (interpolated), no fixed bucket needed (run on 3.15.1 with a native-histogram input in `promtool test rules`).

## Choosing what counts
- Usually only successful requests count for latency (errors are already in the availability SLO); filter `code!~"5.."` on both numerator and denominator.
- Exclude long-polling/streaming routes or give them their own SLO.

## Gotchas
- If 300ms is not a bucket boundary, `le="0.3"` returns nothing: alerts silently never fire (tested: with only `le="0.5"` the ratio query returned no series and `absent(...{le="0.3"})` returned 1). Add an alert on `absent(...{le="0.3"})` or check in CI.
- Changing bucket layouts in a deploy breaks the SLI; pin boundaries used by SLOs.
- p99 threshold alerts ("p99 > 300ms for 10m") are simpler but do not map to budget consumption; prefer the ratio form for paging.

## Verify
- [ ] Injected latency on 5% of requests triggers the page within minutes in staging; promtool test included.
