---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.dropping-unused-metrics
name: dropping-unused-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, metric-dropping, drop-unused-metrics, metric-relabel-configs, mimirtool-analyze, cost-control, servicemonitor]
level: practitioner
status: verified
description: "Find metrics no dashboard or rule uses (mimirtool analyze) and drop them at scrape time with metric_relabel_configs, including ServiceMonitor syntax and safe rollout."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#metric_relabel_configs", "https://grafana.com/docs/mimir/latest/manage/tools/mimirtool/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dropping unused metrics

## 1. Find what is used
```bash
mimirtool analyze grafana --address=https://grafana.example.com --key=$GRAFANA_SA_TOKEN   # -> metrics-in-grafana.json
mimirtool analyze rule-file rules/*.yml                                                    # -> metrics-in-ruler.json
mimirtool analyze prometheus --address=http://prom:9090 \
  --grafana-metrics-file=metrics-in-grafana.json --ruler-metrics-file=metrics-in-ruler.json
# -> prometheus-metrics.json with in_use_metric_counts and additional_metric_counts (unused) + series counts
jq -r '.additional_metric_counts[] | "\(.count)\t\(.metric)"' prometheus-metrics.json | sort -rn | head -30
```
Run on mimirtool 3.2.2 against Grafana 13.2.4 and Prometheus 3.15.1: the three files are written with those default names, and each entry of `additional_metric_counts` has `metric`, `count` and `job_counts`.
Also ask teams: ad-hoc Explore queries and external API consumers don't show in this analysis.

## 2. Drop at scrape
```yaml
scrape_configs:
  - job_name: kubernetes-pods
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: "go_gc_.*|go_memstats_(?:frees|mallocs|lookups)_total|apiserver_request_sli_duration_seconds_bucket|rest_client_rate_limiter_duration_seconds_bucket"
        action: drop
```
ServiceMonitor:
```yaml
spec:
  endpoints:
    - port: metrics
      metricRelabelings:
        - sourceLabels: [__name__]
          regex: "go_gc_.*"
          action: drop
```
`metric_relabel_configs` run after the scrape and before storage: the bytes are still transferred and
parsed, but no series are created.

## 3. Roll out safely
1. Drop in staging, run `mimirtool analyze` again on dashboards to confirm none break.
2. Watch `scrape_samples_post_metric_relabeling` vs `scrape_samples_scraped` per job to see the saving.
3. Prefer dropping whole histograms' `_bucket` only when nobody computes quantiles from them.

## Gotchas
- Regex anchors fully; `go_gc_` without `.*` matches nothing.
- Dropping from the source exporter (collector flags) is cheaper than relabel drop: e.g.
  `node_exporter --no-collector.<name>`.

## Verify
- [ ] Head series fell by the expected amount.
- [ ] Grafana dashboards using these jobs show no "No data" panels.
