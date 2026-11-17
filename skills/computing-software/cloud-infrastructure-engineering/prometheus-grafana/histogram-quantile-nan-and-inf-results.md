---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.histogram-quantile-nan-and-inf-results
name: histogram-quantile-nan-and-inf-results
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [histogram-quantile-nan, missing-inf-bucket, histogram-quantile, promql-histograms, bucket-boundaries]
level: advanced
status: verified
description: "Explain and fix NaN, +Inf and implausible values from histogram_quantile: empty windows, missing +Inf bucket, quantile in the last bucket, non-monotonic buckets."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_quantile", "https://prometheus.io/docs/practices/histograms/#errors-of-quantile-estimation", "https://prometheus.io/docs/concepts/metric_types/#histogram"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# histogram_quantile NaN and Inf results

## Cases (from the function docs)
| Output | Cause | Fix |
|---|---|---|
| `NaN` | no observations in the window (all bucket rates 0) | expected at idle; show "no traffic" or use `or` fallback; widen window |
| `NaN` | fewer than two buckets | the docs special case for classic histograms; check what was scraped |
| `NaN` | `+Inf` bucket missing from the series (docs: the highest bucket must be `+Inf`) | include it: do not filter `le!="+Inf"`; check relabel rules that drop it |
| no result, plus a warning `bucket label "le" is missing or has a malformed value` | `le` lost by aggregation | aggregate with `sum by (le, ...)`; never drop `le` |
| upper bound of the highest finite bucket (the second highest bucket, docs) | quantile falls in the `+Inf` bucket | add higher buckets; a p99 above your top bucket is unknown |
| value equals a bucket boundary often | coarse buckets; linear interpolation within the bucket | add buckets near the SLO threshold |
| inconsistent (quantile not increasing with q) | buckets non-monotonic due to scrape timing / mixed versions with different layouts | aggregate only series with identical bucket layouts; tiny differences (1e-12 of the two buckets) are ignored, larger ones are raised to the previous bucket and flagged with the info annotation `input to histogram_quantile needed to be fixed for monotonicity` |
| `-Inf` for q<0, `+Inf` for q>1 (with a warning) | invalid q | q in [0,1] |

## Correct shape
```promql
histogram_quantile(0.99, sum by (le, route) (rate(http_request_duration_seconds_bucket[5m])))
```
Native histograms: `histogram_quantile(0.99, sum by (route) (rate(http_request_duration_seconds[5m])))` (no `le`).

## Bucket layout changes
Mixing old and new bucket sets across instances during a rollout yields distorted quantiles: buckets present only on some series undercount. The non-monotonic annotation above is the usual symptom.

## Checked
Run on Prometheus 3.15.0 with buckets 0.3 / 1.2 / 5 / +Inf holding 50 / 90 / 98 / 100 requests per minute: p50 = 0.3, p95 = 3.575, p99 = 5 (the 5 bucket bound); an all-zero histogram returned NaN; a series with only a `+Inf` bucket returned NaN; the series without `+Inf` returned NaN; `sum(rate(...))` that dropped `le` returned an empty result with the warning above; q = -1 gave -Inf and q = 1.5 gave +Inf; a non-monotonic layout returned a value with the monotonicity info annotation.

## Verify
- [ ] Top finite bucket exceeds your worst realistic latency (check `rate(x_bucket{le="+Inf"}) - rate(x_bucket{le="<top>"})` is near 0).
- [ ] Dashboards display "no data" sensibly when idle.
