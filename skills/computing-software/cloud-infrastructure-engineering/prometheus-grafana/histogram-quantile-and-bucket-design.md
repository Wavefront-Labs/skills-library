---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.histogram-quantile-and-bucket-design
name: histogram-quantile-and-bucket-design
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql, histogram-quantile, histogram-quantile-usage, quantile-aggregation-by-le, bucket-boundaries, bucket-layout, latency, slo]
level: practitioner
status: verified
description: "Compute latency percentiles with histogram_quantile (rate first, sum by le), understand interpolation error, and design classic bucket boundaries around SLO thresholds."
sources: ["https://prometheus.io/docs/practices/histograms/", "https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_quantile"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# histogram_quantile and bucket design

## The canonical query
```promql
histogram_quantile(0.99,
  sum by (le, job) (rate(http_request_duration_seconds_bucket[5m])))
```
1. `rate` the `_bucket` counters first.
2. `sum by (le, <grouping labels>)`: keep `le`; drop instance/pod to aggregate.
3. Then `histogram_quantile`.
Forgetting `le` in the `by` clause returns nothing (run in `promtool test rules`: `histogram_quantile(0.95, sum by (job) (rate(d_bucket[5m])))` gave an empty result); forgetting `rate` gives quantiles over everything since the counters started (run: `histogram_quantile(0.5, sum by (le) (d_bucket))` returned the all-time answer, 0.1).

## How accurate it is
Prometheus finds the bucket containing the quantile rank and **linearly interpolates** inside it.
- With buckets 0.1, 0.25, 0.5, 1 and a true p99 of 0.27 s, the answer can be anywhere in 0.25-0.5 depending on
  distribution; error = bucket width. Worked and run: per-minute increments of 25, 45, 49.5, 50 and 50 observations in the `le` = 0.1, 0.25, 0.5, 1, +Inf buckets give a p95 rank of 47.5 of 50, which lies in (0.25, 0.5]: 0.25 + 0.25 x (47.5 - 45) / (49.5 - 45) = 0.3889, and Prometheus returned 0.38888888888888884. The p99 rank equals the cumulative count of the 0.5 bucket, so it returned 0.5 (0.5000000000000067 with float rounding).
- If the quantile falls in the `+Inf` bucket, the result is the upper bound of the second-highest bucket, i.e. the highest finite bound (functions docs; run: 80 of 100 observations above 1 s gave 1 for p99). A flat line = "off the chart", not a real value.
- Other documented special cases: no observations give NaN, fewer than two buckets give NaN, and the highest bucket must be `+Inf` or the result is NaN.
- At low traffic (few requests per window) results are noisy; use a longer window.

## Designing buckets
- Put a boundary **exactly at every SLO threshold** (e.g. 0.3 s) so `le="0.3"` gives an exact good-event count.
- Dense where you care (around typical latency and SLO), sparse elsewhere; 10-15 buckets is typical.
- Cover the realistic max (timeouts) so +Inf is rare.
- Common layouts: Go `prometheus.DefBuckets` (`.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10` in client_golang `histogram.go`) for web; `ExponentialBuckets(0.001, 2, 15)` for wide ranges (the signature is `(start, factor, count)` and the 15 buckets run from 0.001 to 16.384 s, computed). The Python client's `Histogram.DEFAULT_BUCKETS` is different (run: also 0.075, 0.75, 7.5 and so on, 15 buckets including +Inf), so dashboards and SLO thresholds written for one do not line up with the other.
- Each bucket multiplies series by label combinations: 15 buckets x 20 routes x 5 codes x 50 pods = 75,000 series (plus the `_sum` and `_count` series).
  Drop labels before adding buckets.
- Changing buckets later breaks continuity; when you need flexibility consider native histograms. In 3.15 they are scraped only when `scrape_native_histograms` is set in config (the `native-histograms` feature flag is a no-op), and the functions docs show `histogram_quantile(0.9, sum by (job) (rate(x[10m])))` with no `le` for them (this part is from the docs).

## Verify
- [ ] Every latency SLO threshold appears as an `le` value: `count by (le) (x_bucket)`.
- [ ] p99 panels aren't flat at the top bucket during incidents (if so, add higher buckets).

## Checked
Prometheus 3.15.1 `promtool test rules` with 13 series (classic histogram buckets for two instances, a slow-tail histogram) and five expressions: the canonical query with p95 (interpolation checked by hand) and p99 (rank on a boundary), missing `le`, no `rate`, and the quantile in the `+Inf` bucket. Docs read: querying/functions.md at tag v3.15.1 (`histogram_quantile` special cases); `histogram.go` in client_golang (DefBuckets, ExponentialBuckets signature); Python prometheus_client `Histogram.DEFAULT_BUCKETS` printed.
