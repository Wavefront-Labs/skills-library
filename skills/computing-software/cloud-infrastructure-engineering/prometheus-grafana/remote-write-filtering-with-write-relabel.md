---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.remote-write-filtering-with-write-relabel
name: remote-write-filtering-with-write-relabel
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, remote-write, write-relabel-filtering, remote-write-filtering, write-relabel-configs, cost-control, relabeling]
level: practitioner
status: verified
description: "Send only the series a remote backend needs with write_relabel_configs: allowlists, dropping labels, per-destination filters, and checking the effect on sample rate."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write", "https://grafana.com/docs/grafana-cloud/cost-management-and-billing/reduce-costs/metrics-costs/client-side-filtering/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filtering remote write with write_relabel_configs

`write_relabel_configs` run per destination, after `metric_relabel_configs`, only on what is sent. Local
storage keeps everything, so you can keep full detail locally and ship a subset.

## Allowlist (preferred for paid backends)
```yaml
remote_write:
  - url: https://metrics.example.com/api/v1/write
    write_relabel_configs:
      - source_labels: [__name__]
        regex: "up|slo:.*|job:.*:rate5m|node_(cpu_seconds_total|memory_MemAvailable_bytes|filesystem_avail_bytes)|kube_pod_status_phase"
        action: keep
```
Ship recording-rule outputs (`level:metric:operation`) plus a short list of raw metrics; dashboards built
on the backend must use the same rule names.

## Denylist
```yaml
    write_relabel_configs:
      - source_labels: [__name__]
        regex: "go_.*|process_.*|apiserver_request_duration_seconds_bucket|etcd_.*"
        action: drop
      - regex: "pod_template_hash|controller_revision_hash|id"
        action: labeldrop        # make sure the remaining labels still identify a unique series
```

## Per-destination
Two `remote_write` blocks with different filters: e.g. everything to self-hosted Mimir, SLO rules only to a
vendor. Each block has its own queue and memory.

## Measure the effect
```promql
rate(prometheus_remote_storage_samples_total[5m])                  # sent per destination (by url)
rate(prometheus_remote_storage_samples_dropped_total{reason="dropped_series"}[5m])   # removed by write_relabel_configs
rate(prometheus_tsdb_head_samples_appended_total[5m])               # ingested locally
```
Before shipping, test the regex against local data:
`count({__name__=~"<regex>"})` should equal the series you expect to send.

## Gotchas
- `labeldrop` that removes an identifying label merges series: dropping `path|user` from three series left a
  receiving Prometheus with one series and no error on either side, so samples vanish silently (other backends may
  reject the duplicates instead). Only drop labels that are constant or redundant.
- Regexes are fully anchored; `node_.*` is needed, `node_` matches only the literal name.
- Histograms: keep `_bucket`, `_sum` and `_count` together or `histogram_quantile` breaks remotely.
- Prometheus Operator: `spec.remoteWrite[].writeRelabelConfigs` (camelCase).

## Verify
- [ ] Sent sample rate dropped by the expected fraction.
- [ ] Backend dashboards and alerts still return data for every metric they use.
- [ ] No `out of order` or `duplicate sample` errors at the backend after `labeldrop`.
