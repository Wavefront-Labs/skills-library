---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.federating-aggregated-recording-rules
name: federating-aggregated-recording-rules
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [federate-recording-rules, aggregated-federation, federation, recording-rules, hierarchical-federation]
level: practitioner
status: docs-checked
description: "Federate only aggregated recording rules from leaf Prometheus servers to a global one: /federate match[], honor_labels, external labels, level:metric:operations naming."
sources: ["https://prometheus.io/docs/prometheus/latest/federation/", "https://prometheus.io/docs/practices/rules/", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config", "https://prometheus.io/docs/prometheus/latest/querying/functions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Federating aggregated recording rules

The federation docs' hierarchical pattern: many per-datacenter servers collect data in high detail (instance-level drill-down), and global servers collect and store only aggregated data (job-level drill-down) from them. The `/federate` endpoint returns the current value of a selected set of series; at least one `match[]` parameter is required, each an instant vector selector such as `up` or `{job="api-server"}`, and multiple `match[]` give the union.

## Leaf recording rules
Name rules `level:metric:operations` (the Prometheus rules page): `level` is the aggregation level and labels of the output, `metric` is the unchanged metric name (only `_total` is stripped when using `rate()` or `irate()`), `operations` is the list applied, newest first. Aggregate with a `without` clause naming the labels you drop, so other labels such as `job` are preserved; aggregate numerator and denominator separately, never average a ratio.
```yaml
groups:
  - name: federate
    rules:
      - record: instance_path:requests:rate5m
        expr: rate(requests_total{job="myjob"}[5m])
      - record: job:requests:rate5m
        expr: sum without (instance, path)(instance_path:requests:rate5m{job="myjob"})
```
Only a `job:` level series needs to be federated upward; the instance-level rule stays local.

## Global scrape
Pattern from the federation page (adapted):
```yaml
scrape_configs:
  - job_name: 'federate'
    scrape_interval: 15s
    honor_labels: true
    metrics_path: '/federate'
    params:
      'match[]':
        - '{__name__=~"job:.*"}'
    static_configs:
      - targets: ['source-prometheus-1:9090', 'source-prometheus-2:9090']
```
- `honor_labels: true` keeps the label values from the scraped data instead of renaming conflicting ones to `exported_job` / `exported_instance`; the configuration page calls it useful for federation and the Pushgateway.
- Global `external_labels` on the leaf are documented as applying to communication with external systems "federation, remote storage, Alertmanager", applied only when a series does not already have that label. Use distinct external labels per leaf so the global server can tell them apart.
- Native histograms: the scraping server needs `scrape_native_histograms: true` (protobuf scraping). Float samples are always federated as untyped.
- Cross-service federation is the other use case: pull selected series from another service's Prometheus into one server.

## Global queries
Aggregate classic histogram buckets by `le` before `histogram_quantile`, for example `histogram_quantile(0.9, sum by (le) (rate(http_request_duration_seconds_bucket[10m])))` (the functions page's form). If you federate a recorded rate of buckets, the same `sum by (le)` applies to the recorded series.

## Verify
- [ ] The federated series from each leaf appear on the global server with the leaf's `job` and `instance` labels intact (no `exported_` labels).
- [ ] Only the aggregated series named by `match[]` are present, not full-detail series.

## Checked
Date: 2026-11-07. Read in full: the Prometheus Federation page and the Recording rules (naming and aggregation) page. From the configuration page I read the global block (`scrape_interval` default 1m, `scrape_timeout` default 10s, `external_labels`) and the `honor_labels` entry; the rest of that ~3600 line page was not read. From the functions page I read only the `histogram_quantile` examples. Trims: removed the draft's `scrape_timeout: 25s` / 30s interval values, the claims that raw counters multiply series, that a global interval must be at least the leaf rule interval, that a slow `/federate` makes the target `up=0`, the `scrape_samples_scraped` thresholds, and the cluster/code label examples; the leaf rules were rewritten to follow the documented naming scheme (the draft's `sum by (job, code)` rules dropped the `without` guidance). The `_bucket` recorded-series rule and the `cluster:` prefix match were removed as not shown on the pages.
Method: documentation only; no commands were run.
