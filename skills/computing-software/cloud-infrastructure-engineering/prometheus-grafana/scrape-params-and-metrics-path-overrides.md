---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.scrape-params-and-metrics-path-overrides
name: scrape-params-and-metrics-path-overrides
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, scrape-config, scrape-params, metrics-path-override, params, metrics-path, __metrics_path__, __param_, __scheme__, __address__, relabel-params, multi-target-exporter, blackbox-exporter, snmp-exporter, per-target-path, pca]
level: practitioner
status: verified
description: "Send query params and custom paths on scrapes: static params, per-target __param_ and __metrics_path__ via relabeling, the multi-target exporter pattern, scheme/port overrides."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config", "https://prometheus.io/docs/guides/multi-target-exporter/", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scrape params and metrics_path overrides

**Goal:** scrape endpoints that are not `GET /metrics` — a different path, query parameters
that select what to collect, or one exporter that probes many targets.

## 1. Static per-job settings
```yaml
scrape_configs:
  - job_name: app
    scheme: https
    metrics_path: /internal/metrics
    params:
      collect[]: [cpu, memory]       # repeated key → ?collect[]=cpu&collect[]=memory
      format: [prometheus]
```
`params` values are lists. These apply to every target in the job.

## 2. Per-target overrides with magic labels
Before relabeling, every target has `__address__`, `__scheme__`, `__metrics_path__` and
`__param_<name>` labels; set them in `relabel_configs` (or directly in `file_sd`/`static_configs`
labels) to vary path or params per target:
```yaml
  - job_name: file-targets
    file_sd_configs: [{files: ["targets/*.yml"]}]
# targets/app.yml
- targets: ["a:8080"]
  labels: {__metrics_path__: /actuator/prometheus, __scheme__: https}
- targets: ["b:9100"]
  labels: {__param_collect: cpu}
```
Labels starting with `__` are dropped after relabeling, so they never reach the stored series.

## 3. Multi-target exporter pattern (blackbox, snmp, json_exporter)
One exporter, many probed targets; the real target goes into a `target` query param and the
exporter's own address becomes `__address__`:
```yaml
  - job_name: blackbox-http
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets: [https://example.com, https://api.example.com/health]
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target          # ?target=https://example.com
      - source_labels: [__param_target]
        target_label: instance                # keep the probed URL as instance
      - target_label: __address__
        replacement: blackbox-exporter:9115   # actually scrape the exporter
```
Vary the module per target with `__param_module` from a `module` label. The resulting
request is `GET http://blackbox-exporter:9115/probe?module=http_2xx&target=https://example.com`
(on the wire the target is URL-encoded: `target=https%3A%2F%2Fexample.com`, as `/targets` shows).

## 4. Port and scheme rewrites from Kubernetes annotations
```yaml
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scheme]
        regex: (https?)
        target_label: __scheme__
```
The `regex: (.+)` guard on the path means pods without the annotation keep the default
`/metrics` instead of getting an empty path.

## Gotchas
- `params` and `__param_x` with the same name: the relabeled one wins per target.
- Setting `__metrics_path__` to a path with a query string does not work (the `?` is percent-encoded into the
  path: `/metrics%3Fx=1`); put the query in `__param_*`.
- `__scheme__` must be `http` or `https`; relabeling it to anything else fails the target (`unsupported protocol scheme "ftp"`).
- The `/targets` page shows the final scrape URL per target — use it to debug the rewrite
  before writing PromQL.
- For `/probe` jobs, `instance` must be set explicitly (step 3) or every probe shares
  `instance="blackbox-exporter:9115"` and collides.

## Verify
- [ ] `/targets` shows the expected URL including path and params for one target of each kind.
- [ ] `curl` of that exact URL from the Prometheus host returns metrics.
- [ ] No stored series carries a `__param_*` or `__metrics_path__` label.
