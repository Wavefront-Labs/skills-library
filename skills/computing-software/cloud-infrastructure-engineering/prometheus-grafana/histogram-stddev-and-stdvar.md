---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.histogram-stddev-and-stdvar
name: histogram-stddev-and-stdvar
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [histogram-stddev, histogram-stdvar, native-histograms, promql-histograms, anomaly-detection]
level: advanced
status: verified
description: "Use histogram_stddev and histogram_stdvar on native histograms to measure spread of latency or size distributions, and their estimation limits."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_stddev-and-histogram_stdvar", "https://prometheus.io/docs/specs/native_histograms/", "https://prometheus.io/docs/prometheus/latest/querying/functions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# histogram_stddev and histogram_stdvar

`histogram_stddev(v instant-vector)` and `histogram_stdvar(v)` return the estimated standard deviation / variance of observations in each **native** histogram sample. Classic (`_bucket`) histograms are ignored (no output).

## Usage
```promql
# spread of request latency over the last 5m per route
histogram_stddev(sum by (route) (rate(http_request_duration_seconds[5m])))
# coefficient of variation (spread relative to mean)
histogram_stddev(sum by (route) (rate(http_request_duration_seconds[5m])))
  / histogram_avg(sum by (route) (rate(http_request_duration_seconds[5m])))
```

## How it estimates
Each bucket's observations are assumed to sit at a representative point of the bucket (geometric mean of the bounds for the usual exponential buckets; arithmetic mean of the bounds for the zero bucket and custom buckets), and the mean is the histogram's `sum / count`, so the result is an approximation whose accuracy depends on bucket resolution (schema). For one schema-0 histogram with buckets `[1 2 3]` over (0.5,1], (1,2], (2,4], sum 25 and count 6 the variance is 5.416 and the standard deviation 2.327, matching a hand computation.

## When it is useful
- Detecting widening latency distributions (bimodal behaviour, partial degradation) that p50 hides.
- Capacity: variability of request sizes.
For alerting on user experience, quantiles or `histogram_fraction` against an SLO threshold are clearer.

## Gotchas
- Requires native histograms end to end (instrumentation, protobuf scraping, storage, remote write).
- Do not apply to `rate()` of classic buckets; use `stddev_over_time` on gauges for non-histogram data.

## Verify
- [ ] Query returns results for the native histogram metric (`histogram_count(rate(x[5m]))` works first).

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), client_golang 1.25.0 on Go 1.26.
- promtool unit tests with native samples `{{schema:0 sum:25 count:6 buckets:[1 2 3]}}`: `histogram_stddev` 2.327 and `histogram_stdvar` 5.416 (hand check in Python with geometric-mean representatives and mean = sum/count gave 5.41); `histogram_stddev(cls_bucket)` on a classic series returned nothing; `histogram_stddev(sum by (r) (rate(nh[2m])))` and `histogram_avg(sum by (r) (rate(...)))` evaluated (2.327 and 4.167), so the coefficient-of-variation expression is valid.
- Live: a Go native histogram scraped by Prometheus 3.15.1 gave `histogram_stddev(rate(x[20s]))` 0.103 and `histogram_avg` 0.104 (exponential-distributed observations with mean 0.1).
- Estimation rule (geometric mean for exponential buckets, arithmetic mean for zero and custom buckets, floats ignored): 3.15 functions page. No feature flag was needed for these functions in 3.15.1.
