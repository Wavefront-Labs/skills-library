---
id: computing-software.cloud-infrastructure-engineering.kubernetes.prometheus-cr-tuning-and-scrapeconfig
name: prometheus-cr-tuning-and-scrapeconfig
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, prometheus-operator, prometheus-cr, prometheus-retention, prometheus-sharding, scrapeconfig-crd, additionalscrapeconfigs, monitoring]
level: advanced
status: docs-checked
description: "Tune the Prometheus CR (retention, storage, resources, selectors, shards, remote write) and scrape non-Kubernetes targets with the ScrapeConfig CRD or additionalScrapeConfigs."
sources: ["https://prometheus-operator.dev/docs/api-reference/api/#monitoring.coreos.com/v1.Prometheus", "https://prometheus-operator.dev/docs/developer/scrapeconfig/", "https://prometheus-operator.dev/docs/platform/storage/", "https://raw.githubusercontent.com/prometheus/prometheus/main/documentation/prometheus-mixin/alerts.libsonnet", "https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus CR tuning and ScrapeConfig

## Prometheus CR essentials
```yaml
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata: {name: k8s, namespace: monitoring}
spec:
  replicas: 2                       # HA pair; both scrape everything
  shards: 1                         # >1 distributes scraped targets onto several shards (replicas x shards = Pods)
  retention: 15d
  retentionSize: 90GB               # maximum bytes of data; also see retentionPercentage; keep below the PVC size
  storage:
    volumeClaimTemplate:
      spec: {storageClassName: gp3, resources: {requests: {storage: 100Gi}}}
  resources: {requests: {cpu: "1", memory: 8Gi}, limits: {memory: 12Gi}}
  serviceMonitorSelector: {matchLabels: {release: kube-prometheus-stack}}
  serviceMonitorNamespaceSelector: {}        # {} = all namespaces; nil = own namespace only
  podMonitorSelector: {}
  ruleSelector: {matchLabels: {release: kube-prometheus-stack}}
  scrapeConfigSelector: {}
  enforcedSampleLimit: 50000        # global cap on scraped samples per scrape; overrides larger per-monitor sampleLimit values
  externalLabels: {cluster: prod-eu}
  remoteWrite:
  - url: https://mimir.example.com/api/v1/push
    queueConfig: {maxSamplesPerSend: 2000, capacity: 10000}
  walCompression: true
```
Selector gotcha: an **empty selector `{}` matches all**, an **unset selector matches none**
(for serviceMonitorSelector in the CR). Helm chart values `*SelectorNilUsesHelmValues: false`
make the chart select everything.

Sizing: memory grows with active series. Check `prometheus_tsdb_head_series` and
`topk(10, count by (__name__)({__name__=~".+"}))` before adding RAM.
Sharding spreads targets over shards; the API reference warns that increasing or reducing shards does
not reshard existing data.

## ScrapeConfig CRD (targets outside Kubernetes)
```yaml
apiVersion: monitoring.coreos.com/v1alpha1
kind: ScrapeConfig
metadata: {name: bare-metal-nodes, namespace: monitoring, labels: {release: kube-prometheus-stack}}
spec:
  staticConfigs:
  - targets: ["10.0.5.11:9100", "10.0.5.12:9100"]
    labels: {job: baremetal-node}
  # fileSDConfigs / httpSDConfigs / consulSDConfigs / ec2SDConfigs ...
  metricRelabelings:
  - {action: drop, sourceLabels: [__name__], regex: "node_scrape_collector_.*"}
```
Older/escape hatch: `spec.additionalScrapeConfigs` referencing a Secret with raw Prometheus
`scrape_configs` YAML; the API reference recommends it over the unmanaged-configuration mode, and a bad
entry can break config reload (check `prometheus_config_last_reload_successful`). Prefer ScrapeConfig.

## Verify
- [ ] `kubectl -n monitoring get prometheus k8s -o jsonpath='{.status.conditions}'` Available/Reconciled True.
- [ ] Targets page shows ScrapeConfig jobs up; `prometheus_config_last_reload_successful == 1`.

## Checked
2026-10-28. Confirmed against the Prometheus Operator API reference: `shards` and `replicas` semantics,
`retention`, `retentionSize`, `retentionPercentage`, selector semantics (empty matches all, null matches
none; namespace selector null means own namespace), `enforcedSampleLimit`, `walCompression`, `remoteWrite`
`queueConfig` (`capacity`, `maxSamplesPerSend`), `scrapeConfigSelector`, `additionalScrapeConfigs`, ScrapeConfig
`staticConfigs` / `metricRelabelings`, and the `Reconciled` and `Available` conditions; the
`*SelectorNilUsesHelmValues` behaviour against the chart README; `prometheus_tsdb_head_series` (Prometheus
TSDB source) and `prometheus_config_last_reload_successful` (Prometheus mixin alerts). Removed: the
"4-8 KB per series" figure, the "PVC size * 0.85" rule, the hashmod description of sharding and the
claim that the Secret route is unvalidated. Example values (`gp3`, sizes, `mimir.example.com`, node IPs)
are placeholders to adapt.
Method: documentation only; no commands were run.
