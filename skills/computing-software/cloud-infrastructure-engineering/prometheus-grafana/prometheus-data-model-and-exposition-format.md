---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-data-model-and-exposition-format
name: prometheus-data-model-and-exposition-format
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, data-model, exposition-format, text-format, openmetrics, metric-types, counter, gauge, histogram, summary, labels, series-identity, le-label, quantile-label, total-suffix, created-suffix, info-metrics, stateset, exemplars-format, content-negotiation, promtool-check-metrics, pca]
level: practitioner
status: verified
description: "Read and write the Prometheus text/OpenMetrics exposition format: metric types and reserved labels, series identity, suffix rules, and validating an endpoint with promtool check metrics."
sources: ["https://prometheus.io/docs/concepts/data_model/", "https://prometheus.io/docs/concepts/metric_types/", "https://prometheus.io/docs/instrumenting/exposition_formats/", "https://github.com/prometheus/OpenMetrics/blob/main/specification/OpenMetrics.md"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Data model and exposition format

**Goal:** understand what a time series *is* to Prometheus so you can read any `/metrics`
page, spot malformed output, and know why a label change is a new series.

## 1. The model
- A **time series** is identified by its metric name plus the full set of label name/value
  pairs: `http_requests_total{job="api", method="GET", status="200"}`. Change one label
  value and you have a different series. The name itself is just the label `__name__`.
- Each series is a sequence of `(timestamp_ms, float64)` samples (plus native histogram
  samples in newer versions).
- Names match `[a-zA-Z_:][a-zA-Z0-9_:]*`; colons are reserved for recording rules. Label
  names match `[a-zA-Z_][a-zA-Z0-9_]*`; `__`-prefixed labels are internal. (UTF-8 names are
  allowed from 3.0 with quoting: `{"http.requests", "k8s.pod"="x"}`.)

## 2. Metric types and what they expand to
| Type | Series produced | Reserved labels/suffixes |
|---|---|---|
| counter | `name_total` (monotonic; resets to 0 on restart) | `_total`, OpenMetrics also `_created` |
| gauge | `name` (any value) | none |
| histogram | `name_bucket{le="<bound>"}` cumulative counts, `name_sum`, `name_count`; always a `le="+Inf"` bucket | `le` |
| summary | `name{quantile="0.99"}`, `name_sum`, `name_count` | `quantile` |
| info / stateset (OpenMetrics) | `name_info{version="1.2"} 1`, `name{state="x"} 1/0` | — |

Rules PromQL relies on: use `rate()` on counters and histogram buckets, never on gauges;
`histogram_quantile()` needs the `le` label and cumulative buckets; summaries' quantiles
cannot be aggregated across instances (averaging percentiles is wrong).

## 3. The text format, line by line
```
# HELP http_requests_total Total HTTP requests.
# TYPE http_requests_total counter
http_requests_total{method="GET",status="200"} 1027 1700000000000
http_requests_total{method="POST",status="500"} 3
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{le="0.1"} 240
http_request_duration_seconds_bucket{le="0.5"} 390
http_request_duration_seconds_bucket{le="+Inf"} 400
http_request_duration_seconds_sum 53.4
http_request_duration_seconds_count 400
# TYPE build_info gauge
build_info{version="2.3.1",commit="abc"} 1
```
- Optional trailing integer timestamp in **milliseconds**; omit it (server timestamps are
  what you want). With the default `honor_timestamps: true` Prometheus keeps the exposed timestamp, and
  series that carry their own timestamps do not go stale when they vanish: they linger for the 5 minute
  lookback (`track_timestamps_staleness` changes this). A sample stamped in 2023 was not returned by an
  instant query in 2026 (tested).
- Values: float, `NaN`, `+Inf`, `-Inf`. Label values are UTF-8, escape `\\`, `\"`, `\n`.
- `# TYPE` must precede the samples of that family; untyped is the default if absent.
- Content-Type: `text/plain; version=0.0.4` (Prometheus text) or
  `application/openmetrics-text; version=1.0.0`. OpenMetrics requires `# EOF` at the end,
  declares `# UNIT`, puts exemplars after `# {trace_id="..."} 1.2 1700000000.0`, and
  the counter family is declared **without** `_total` (`# TYPE http_requests counter`)
  while the sample keeps the suffix.
- The exposition-format docs list native histograms as a protobuf-format feature; enable them with
  `scrape_native_histograms: true`, after which the default scrape-protocol order starts with `PrometheusProto`.

## 4. Validate an endpoint
```bash
curl -s http://app:8080/metrics | promtool check metrics
# exit 0 = clean, 3 = lint problems printed, 1 = parse error
curl -s -H 'Accept: application/openmetrics-text' http://app:8080/metrics | tail -1   # must be "# EOF"
```
Lint messages seen on 3.15.1: `metric names should not contain abbreviated units` (a name like `a_ms`),
`counter metrics should have "_total" suffix`, `non-counter metrics should not have "_total" suffix`,
`non-histogram metrics should not have "le" label` (same for `quantile`), `no help text`, and
`metric not unique` (same name and labels twice). `# TYPE` after samples is a parse error
(`second TYPE line ... or TYPE reported after samples`). A duplicate series inside one scrape is **not** a
scrape error: the target stays `up`, the first value is kept and the later one is dropped (counted in
`prometheus_target_scrapes_sample_duplicate_timestamp_total` when the values differ).

## 5. Design implications
- Every unique label combination is a series. Never put user ids, request ids, full URLs or
  timestamps in labels; see `...prometheus-grafana.prometheus-metric-design-and-cardinality-control`.
- Info metrics (`*_info` with value 1) are how you attach version/build/metadata without
  polluting every other series; join with `on(instance) group_left(version)`.
- Counter resets are detected by `rate()`/`increase()` (a decrease is treated as a reset);
  do not expose a counter that legitimately decreases.
- A histogram's buckets are fixed at instrumentation time; changing them creates new `le`
  series and breaks quantile continuity across the change.

## Verify
- [ ] `promtool check metrics` on the endpoint exits 0 (it exits 3 for lint problems such as `no help text`).
- [ ] Every counter ends in `_total`; every histogram has `+Inf`, `_sum`, `_count`.
- [ ] No sample lines carry explicit timestamps unless you can explain why.
- [ ] Series count per scrape (`scrape_samples_scraped`) matches your expectation within a few percent.
