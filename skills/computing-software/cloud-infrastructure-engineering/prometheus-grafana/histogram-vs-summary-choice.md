---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.histogram-vs-summary-choice
name: histogram-vs-summary-choice
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, histogram-vs-summary, summary-quantiles, histograms, latency, data-model, pca]
level: practitioner
status: docs-checked
description: "Choose between native histogram, classic histogram and summary: aggregation, error, cost, never averaging quantiles, and SLO fractions from each, per Prometheus practices."
sources: ["https://prometheus.io/docs/practices/histograms/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Histogram vs summary

The Prometheus histograms-and-summaries practices page says: if you can, use native histograms and prefer them over both
classic histograms and summaries. Native histogram support in client libraries is still rare (it needed the protobuf
exposition format, so the Java and Go libraries); classic histograms can be ingested as native histograms with custom
bucket boundaries (NHCB) by configuring Prometheus.

| | Native histogram | Classic histogram | Summary |
|---|---|---|---|
| Set at instrumentation | a resolution (and maybe a bucket-limiting strategy) | bucket boundaries | phi-quantiles and sliding window; others cannot be calculated later |
| Instrumentation cost | cheap (increment counters) | cheap (increment counters) | relatively expensive (streaming quantile calculation) |
| Time series | one, with composite samples | `_sum`, `_count` and one per bucket | `_sum`, `_count` and one per quantile |
| Quantile error | limited by the configured resolution | limited by the width of the bucket the quantile is in | configurable, generally very low |
| Quantile and window chosen | ad hoc in PromQL | ad hoc in PromQL | preconfigured at instrumentation |
| Aggregation | ad hoc in PromQL; buckets always compatible | ad hoc, provided bucket boundaries did not change | not aggregatable |

Rules of thumb from the page: use native histograms with a resolution matching your accuracy needs; if you cannot but need
aggregation, use classic histograms with well-chosen buckets; only if aggregation is not needed consider summaries.

## The averaging trap
```promql
avg(http_request_duration_seconds{quantile="0.95"})                                    # BAD: statistically nonsensical
histogram_quantile(0.95, sum(rate(http_request_duration_seconds[5m])))                 # native histogram
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[5m]))) # classic histogram
```

## Mean latency (all three types)
```promql
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])   # summary or classic histogram
histogram_avg(rate(http_request_duration_seconds[5m]))                                         # native histogram
```
Sum and count are additive: aggregate after the `rate`, before the division.

## SLO fraction
```promql
histogram_fraction(0, 0.3, sum by (job) (rate(http_request_duration_seconds[5m])))   # native: estimated by interpolation
sum by (job) (rate(http_request_duration_seconds_bucket{le="0.3"}[5m]))
  / sum by (job) (rate(http_request_duration_seconds_count[5m]))                      # classic: needs a bucket at exactly 0.3
```
With classic histograms, if no bucket has the boundary no result is returned (no interpolation); if only some do, the
result is incomplete without any warning. A summary cannot give this fraction.

## Gotchas
- Quantile-less summaries (only `_sum` and `_count`) are a legitimate use of summaries.
- If observations can be negative, `_sum` can go down and `rate()` treats the drop as a counter reset; native histograms
  are rate'd as a whole and avoid this.
- Changing bucket layouts is disruptive: histograms with different layouts must be reconciled, and for NHCBs the
  aggregated result may collapse to one bucket (the query gets an info-level annotation).

## Verify
- [ ] No dashboard averages or sums `quantile=` series.
- [ ] Every classic-histogram latency threshold used in a `le=` query is an existing bucket boundary.

## Checked
Checked 2026-11-07. Read in full: the whole Prometheus "Histograms and summaries" practices page (overview, library support, count
and sum, bucketing, Apdex, quantiles with the comparison table and error discussion, rules of thumb, visualization). The page has changed
since the earlier draft: it now recommends native histograms over classic histograms and summaries, so the old "prefer classic
histograms, summaries only for a single instance" framing was rewritten. Removed as not on the page: the claim that the native histogram error
is a relative error, the Go "objectives empty default" remark, and the dashboard-wide "every SLO threshold is a bucket
boundary or native" check (kept as a classic-only check). I did not open the native histogram specification or the PromQL
function reference for histogram_fraction, histogram_avg and histogram_quantile; their usage here is exactly as shown in the page examples.
Method: documentation only; no commands were run.
