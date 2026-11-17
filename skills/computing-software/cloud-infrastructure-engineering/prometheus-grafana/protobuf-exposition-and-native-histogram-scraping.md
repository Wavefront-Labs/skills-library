---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.protobuf-exposition-and-native-histogram-scraping
name: protobuf-exposition-and-native-histogram-scraping
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, protobuf-exposition, native-histogram-scrape, native-histograms, scrape-protocols, client-golang]
level: advanced
status: verified
description: "Scrape native histograms: enable them in the client, negotiate protobuf exposition (PrometheusProto), keep classic buckets during migration, and verify with curl."
sources: ["https://prometheus.io/docs/specs/native_histograms/", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config", "https://pkg.go.dev/github.com/prometheus/client_golang/prometheus#HistogramOpts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protobuf exposition and native histogram scraping

Native histograms can only be exposed in the **protobuf** format (`application/vnd.google.protobuf;
proto=io.prometheus.client.MetricFamily;encoding=delimited`); the text formats of Prometheus 3.15 do not carry them.

## Client (Go example)
```go
h := prometheus.NewHistogram(prometheus.HistogramOpts{
    Name:                            "http_request_duration_seconds",
    Help:                            "Request latency.",
    Buckets:                         prometheus.DefBuckets,   // keep classic buckets too during migration
    NativeHistogramBucketFactor:     1.1,                     // ~10% relative error, enables native
    NativeHistogramMaxBucketNumber:  160,
    NativeHistogramMinResetDuration: time.Hour,
})
```
The Go client was the one run here; check each other client library's own documentation for native histogram support
(prometheus_client 0.26.0 for Python has no native histogram type).

## Prometheus
```yaml
global:
  scrape_protocols: [PrometheusProto, OpenMetricsText1.0.0, OpenMetricsText0.0.1, PrometheusText0.0.4]
scrape_configs:
  - job_name: api
    scrape_native_histograms: true          # default false
    always_scrape_classic_histograms: true  # also ingest the classic _bucket series (migration period)
    native_histogram_bucket_limit: 160      # reduce resolution if a histogram has more buckets
```
Protobuf must come first in the negotiated list for Prometheus to ask for it. With `scrape_native_histograms: true` and no
`scrape_protocols` set, 3.15.1 already puts `PrometheusProto` first (the `Accept` header started with
`application/vnd.google.protobuf;...;q=0.7`), so the explicit global list above is only needed to pin the order.

## Check the target
```bash
curl -s -H 'Accept: application/vnd.google.protobuf;proto=io.prometheus.client.MetricFamily;encoding=delimited' \
  http://app:8080/metrics | wc -c                          # binary output = protobuf served
```
In PromQL a native histogram is one series without `le`:
`histogram_quantile(0.99, sum(rate(http_request_duration_seconds[5m])))`.

## Gotchas
- Remote write 1.0 needs `send_native_histograms: true` (default false; a no-op for the v2 message); the receiving backend must accept them.
- Without `always_scrape_classic_histograms`, the `_bucket`, `_sum` and `_count` series are not stored (a native-only job had one series, the classic job 14) and old dashboards break.
- Federation exposes native histograms only over protobuf as well: `/federate` returned an empty body for a native-only histogram as text and the series when asked with the protobuf `Accept` header.

## Verify
- [ ] `count(http_request_duration_seconds)` returns series (native) and `_bucket` too during migration.
- [ ] `histogram_count(rate(http_request_duration_seconds[5m]))` equals the classic `_count` rate (both were 49.06 per second in the test).

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), prometheus_client 0.26.0 on Python 3.14, client_golang 1.25.0 on Go 1.26.
- The Go `HistogramOpts` block compiled and ran as written against client_golang 1.25.0 (needs Go 1.26 for that release); `curl` with the protobuf `Accept` returned 5941 binary bytes and `text/plain` returned classic buckets only.
- Prometheus 3.15.1 with four jobs against that target: native+classic (1 native series and 12 `_bucket` series), native only (1 series), classic default (14 series), native with `native_histogram_bucket_limit: 20` (histogram stored with 18 buckets instead of 126). The skill's global `scrape_protocols` plus job YAML passes `promtool check config`.
- `histogram_quantile(0.99, sum(rate(x[20s])))`, `histogram_fraction`, `histogram_avg`, `histogram_stddev` returned values on the native job; `histogram_count(rate())` equalled the classic `rate(_count)`.
- Accept header of the native-histogram job: logged by a local server (protobuf first, q=0.7). Federation behaviour: `/federate` with and without the protobuf Accept header.
- `send_native_histograms` default and the v2 no-op: 3.15 configuration page.
