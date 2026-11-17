---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.native-histogram-functions-and-migration
name: native-histogram-functions-and-migration
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql, native-histograms, histogram-fraction, histogram-count-sum, histogram-avg, native-histogram-migration, classic-to-native]
level: advanced
status: verified
description: "Query native histograms (histogram_quantile, histogram_fraction, histogram_count/sum/avg/stddev) and migrate dashboards and rules from classic _bucket series safely."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_fraction", "https://prometheus.io/docs/specs/native_histograms/", "https://grafana.com/docs/mimir/latest/send/native-histograms/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Native histogram functions and migration

A native histogram is **one series** (no `le`, no `_bucket/_sum/_count` suffixes) holding exponential
buckets, count and sum.

## Functions
```promql
histogram_quantile(0.99, sum by (job) (rate(http_request_duration_seconds[5m])))   # no "le" needed
histogram_fraction(0, 0.3, sum(rate(http_request_duration_seconds[5m])))            # share of requests <= 300 ms
histogram_count(rate(http_request_duration_seconds[5m]))     # = classic rate(_count)
histogram_sum(rate(http_request_duration_seconds[5m]))       # = classic rate(_sum)
histogram_avg(rate(http_request_duration_seconds[5m]))       # sum/count (3.x)
histogram_stddev(rate(...)) ; histogram_stdvar(rate(...))    # spread estimates
```
`histogram_fraction` makes any threshold an SLI after the fact: no need to have a bucket at 0.3.

## Migration plan
1. Enable native histograms in clients **alongside** classic buckets (Go: set both `Buckets` and
   `NativeHistogramBucketFactor`).
2. Prometheus: `scrape_native_histograms: true` (3.x setting, default false) and
   `always_scrape_classic_histograms: true` so both forms are stored. Remote write: `send_native_histograms: true`.
3. Duplicate each dashboard panel/rule with the native query; compare for a few weeks. (Two jobs scraping the same target gave classic p99
   0.632 s, native p99 0.526 s, since the classic result is limited to the default bucket bounds.)
4. Switch recording rules and SLO queries; keep the `record` names stable so consumers don't change.
5. Drop classic buckets (client or `metric_relabel_configs` drop `_bucket`).

| Classic | Native |
|---|---|
| `histogram_quantile(0.9, sum by (le) (rate(x_bucket[5m])))` | `histogram_quantile(0.9, sum(rate(x[5m])))` |
| `rate(x_count[5m])` | `histogram_count(rate(x[5m]))` |
| `rate(x_bucket{le="0.3"}[5m]) / rate(x_count[5m])` | `histogram_fraction(0, 0.3, rate(x[5m]))` |

## Gotchas
- Check every hop (Grafana panels, remote stores, federation consumers) for native histogram support before dropping classic buckets;
  federation needs the protobuf format.
- `native_histogram_bucket_limit` lowers the resolution of a histogram that has more buckets than the limit (126 buckets became 18
  with a limit of 20); accuracy drops slightly.

## Verify
- [ ] Native and classic p99 agree within the classic bucket width during parallel run.
- [ ] Series count per histogram dropped (one series vs ~15).

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), Prometheus Operator API reference (main), jq 1.8.2, client_golang 1.25.0 (Go 1.26).
- Live: a Go client exposing classic and native buckets was scraped by jobs with `scrape_native_histograms` and `always_scrape_classic_histograms`; `histogram_quantile(0.99, sum(rate(x[20s])))`, `histogram_fraction(0, 0.3, rate(x[20s]))`, `histogram_avg`, `histogram_stddev` returned values on native data; `histogram_count(rate())` and `rate(_count)` were both 49.06; native p99 0.526 against classic p99 0.632; the native series carried 126 buckets, 18 with `native_histogram_bucket_limit: 20`.
- promtool unit tests with the native sample notation `{{schema:0 sum:25 count:6 buckets:[1 2 3]}}`: `histogram_count`, `histogram_avg` (4.17), `histogram_fraction(0, 2, ...)` (0.5), `histogram_quantile(0.9, sum(...))`, `histogram_stddev` (2.327), `histogram_stdvar` (5.416) all evaluated; they need no feature flag in 3.15.1. The stddev matches a hand computation with geometric-mean bucket representatives and `sum/count` as the mean.
- Classic `histogram_stddev(x_bucket)` returned nothing.
- `scrape_native_histograms` default and the migration flags: 3.15 configuration page.
