---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-prometheus-scrape-reference
name: grafana-alloy-prometheus-scrape-reference
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [prometheusscrape, scrape-interval, native-histograms, scrape-protocols, scrape-limits, excluded-labels]
level: practitioner
status: docs-checked
description: "Configure prometheus.scrape: defaults for interval, timeout and path, scrape_protocols values, native histograms, sample and label limits, and clustering excluded_labels."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/reference/components/prometheus/prometheus.scrape.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# prometheus.scrape reference

`prometheus.scrape` takes `targets` (a list of label maps) and `forward_to` (a list of Prometheus receivers), and scrapes each target.

## Defaults worth knowing
- `scrape_interval` 60s, `scrape_timeout` 10s, `metrics_path` `/metrics`.
- `honor_labels` false, `honor_timestamps` true, `enable_compression` true, `enable_http2` true.
- `scrape_native_histograms` false; `metric_name_validation_scheme` `"legacy"`; `metric_name_escaping_scheme` `"underscores"`.

## Protocols and native histograms
`scrape_protocols` accepts `OpenMetricsText0.0.1`, `OpenMetricsText1.0.0`, `PrometheusProto`, `PrometheusText0.0.4` and `PrometheusText1.0.0`. To ingest native histograms you need both `scrape_native_histograms = true` and `PrometheusProto` listed first in `scrape_protocols`.

## Limits
`sample_limit`, `label_limit`, `target_limit` and `body_size_limit` cap what one scrape may return; a scrape that exceeds one is treated as failed.

## Injected labels and series
The page lists `job` and `instance` as labels injected into scraped series, and `up`, `scrape_duration_seconds` and `scrape_samples_scraped` among the automatically available scrape metrics.

## Clustering
```alloy
prometheus.scrape "pods" {
  targets    = discovery.kubernetes.pods.targets
  forward_to = [prometheus.remote_write.default.receiver]
  clustering {
    enabled = true
  }
}
```
With `enabled = true` the targets are sharded across cluster peers. Labels starting `__meta_` are excluded from the ownership hash; add more with `excluded_labels` so that volatile labels do not move targets between nodes.

Debug metrics: `prometheus_fanout_latency`, `prometheus_forwarded_samples_total`, `prometheus_scrape_targets_gauge`.

## Checked

2026-11-04. Confirmed against the prometheus.scrape reference (reference/components/prometheus/prometheus.scrape.md): argument defaults, scrape_protocols values, native histogram requirement, limits, injected labels and metrics, clustering excluded_labels, debug metrics. Removed the unconfirmed timeout-versus-interval constraint.

Method: documentation only; no commands were run.
