---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-service-discovery-and-relabeling
name: prometheus-service-discovery-and-relabeling
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, service-discovery, kubernetes-sd, kubernetes-sd-configs, file-sd, file-sd-configs, ec2-sd, consul-sd, dns-sd, http-sd, relabeling, relabel-configs, relabel-configs-vs-metric-relabel-configs, metric-relabel-configs, meta-labels, keep, drop, labelmap, hashmod, sharding, address-rewrite, service-discovery-page, pca]
level: advanced
status: verified
description: "Turn discovered targets into the right scrape set: __meta_* labels, keep/drop/replace/labelmap/hashmod, address rewriting, annotation-driven scraping, file_sd, and the service-discovery page."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes_sd_config", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#file_sd_config", "https://relabeler.promlabs.com/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service discovery and relabeling

**Goal:** discovery hands Prometheus candidate targets with `__meta_*` labels; relabeling
decides which to scrape, where, and with what labels. Done right you never hand-edit
target lists again.

## 1. The two relabel stages
| Stage | Runs | Sees | Use for |
|---|---|---|---|
| `relabel_configs` | before scrape, per target | `__address__`, `__scheme__`, `__metrics_path__`, `__param_*`, `__meta_*`, `job` | choose targets, rewrite address/path, set labels from metadata |
| `metric_relabel_configs` | after scrape, per sample | `__name__` and the sample's labels | drop expensive metrics, rename labels, scrub cardinality |

Labels starting with `__` are dropped after `relabel_configs`, so copy what you need into
a normal label. `__tmp_*` is the convention for scratch labels.

## 2. Actions
```yaml
relabel_configs:
  - { action: keep,    source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape], regex: "true" }
  - { action: drop,    source_labels: [__meta_kubernetes_namespace], regex: "kube-system|monitoring" }
  - { action: replace, source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path], regex: "(.+)", target_label: __metrics_path__ }
  - action: replace                       # rewrite host:port to annotation port
    source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
    regex: "([^:]+)(?::\\d+)?;(\\d+)"
    replacement: "$1:$2"
    target_label: __address__
  - { action: labelmap, regex: __meta_kubernetes_pod_label_(.+) }                 # copy pod labels
  - { action: replace, source_labels: [__meta_kubernetes_pod_name], target_label: pod }
  - { action: labeldrop, regex: "pod_template_hash|controller_revision_hash" }
  - { action: hashmod, source_labels: [__address__], modulus: 4, target_label: __tmp_shard }
  - { action: keep, source_labels: [__tmp_shard], regex: "${SHARD}" }            # manual sharding (env-expanded by your deploy tooling, not by Prometheus)
```
- `regex` is anchored (`^...$`) and RE2; `source_labels` are joined with `separator` (default `;`).
- `keep`/`drop` match the joined value; `replace` only writes `target_label` when `regex` matches.
- Newer actions: `lowercase`, `uppercase`, `keepequal`, `dropequal`.
- Order matters; relabel rules run top to bottom and later rules see earlier results.

## 3. Discovery mechanisms worth knowing
```yaml
# Kubernetes: roles node | service | pod | endpoints | endpointslice | ingress
- job_name: kubernetes-pods
  kubernetes_sd_configs: [{ role: pod, namespaces: { names: [] } }]
# file_sd: any tool writes JSON/YAML, Prometheus watches it (no reload)
- job_name: file
  file_sd_configs: [{ files: ["/etc/prometheus/targets/*.json"], refresh_interval: 1m }]
# [{"targets":["10.0.0.5:9100"],"labels":{"env":"prod","role":"db"}}]
# cloud: ec2_sd_configs (role/filters), azure_sd_configs, gce_sd_configs; consul_sd_configs; dns_sd_configs (SRV/A); http_sd_configs (your own endpoint returning the file_sd JSON shape)
```
- Kubernetes `role: endpoints` scrapes each pod behind a Service and gives both service and pod
  meta labels; `role: pod` catches pods with no Service. Avoid scraping both for the same app.
- `file_sd` is the escape hatch for anything: write the file atomically (tmp + rename). Edits to a watched file are picked up within seconds without a reload (tested).
- Each SD config contributes targets; Prometheus dedupes identical label sets within a job (three file_sd entries with two identical gave two targets).

## 4. metric_relabel_configs patterns
```yaml
metric_relabel_configs:
  - { action: drop, source_labels: [__name__], regex: "go_gc_.*|promhttp_.*" }
  - { action: labeldrop, regex: "id|image" }            # cAdvisor cardinality
  - { action: replace, source_labels: [__name__], regex: "old_name", replacement: "new_name", target_label: __name__ }
  - { action: keep, source_labels: [__name__], regex: "(container_cpu_usage_seconds_total|container_memory_working_set_bytes)" }  # allow-list for noisy exporters
```
Samples dropped here still cost scrape time and bandwidth, not storage; fix the exporter or
scope its collectors when the volume is large.

## 5. Debugging
- `/service-discovery` shows discovered vs active targets and the **before/after labels**
  for each; this is where you learn why a target was dropped.
- `promtool check config` catches syntax, not logic. For logic use the relabeler playground
  (relabeler.promlabs.com) or a scratch Prometheus with the config.
- `prometheus_sd_discovered_targets{config="..."}` vs `prometheus_target_scrape_pool_targets`
  show how many survived relabeling.
- Kubernetes SD needs RBAC: `list`/`watch` on pods, services, endpoints/endpointslices, nodes.

## Gotchas
- Annotation-based scraping (`prometheus.io/scrape`) is a convention, not built in; you
  write the relabel rules (or use the Operator's ServiceMonitor instead).
- `labelmap` with a broad regex can import high-cardinality pod labels; follow it with `labeldrop`.
- Changing `job`/`instance` through relabeling changes series identity: old series go stale,
  dashboards using those labels break.
- `hashmod` sharding splits targets, not series; a single huge target still lands on one shard.

## Verify
- [ ] `/service-discovery` shows zero unexpected drops and the final label set you intended.
- [ ] A new pod with the annotation appears in `/targets` without a Prometheus reload.
- [ ] `scrape_samples_post_metric_relabeling` is materially lower than `scrape_samples_scraped` on jobs where you drop metrics.
