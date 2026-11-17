---
id: computing-software.cloud-infrastructure-engineering.kubernetes.fleet-wide-observability
name: fleet-wide-observability
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, multi-cluster, fleet-observability, prometheus, thanos, mimir]
level: practitioner
status: docs-checked
description: "Observe many clusters as one fleet: per-cluster Prometheus with cluster labels, remote write or Thanos, central Grafana and Alertmanager, cluster-tagged logs and traces."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/", "https://prometheus-operator.dev/docs/api-reference/api/", "https://grafana.com/docs/mimir/latest/references/http-api/", "https://grafana.com/docs/mimir/latest/configure/about-tenant-ids/", "https://thanos.io/tip/components/receive.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fleet-wide observability

## Metrics: collect locally, query centrally
Each cluster runs Prometheus (or an agent-mode Prometheus / OTel collector) with a unique
external label:
```yaml
# kube-prometheus-stack values
prometheus:
  prometheusSpec:
    externalLabels: {cluster: prod-eu-1, env: prod}
    remoteWrite:
    - url: https://mimir.example.com/api/v1/push
      headers: {X-Scope-OrgID: platform}
```
Options:
- Remote write to Mimir (`POST /api/v1/push`; with multi-tenancy on, requests need the `X-Scope-OrgID`
  tenant header) or Thanos Receive (implements the Prometheus Remote Write API): central storage.
- Thanos sidecar plus a central Thanos Query: sidecars upload blocks to object storage and queries fan out
  across StoreAPIs. See `long-term-metrics-storage-thanos-and-mimir`.
Without a distinguishing external label, series from different clusters collide.

## Dashboards and alerts
- Put a Grafana `cluster` variable (from `label_values(up, cluster)`) on every dashboard.
- Group alerts by `cluster` in Alertmanager.
- A meta-alert per cluster, for example `absent(up{cluster="prod-eu-1",job="kubelet"})`, catches a cluster that
  stopped sending.

## Logs and traces
Add the cluster name as a static label in your log shipper and as a resource attribute in the OTel
collector. Keep Loki label sets small and low-cardinality (see `loki-log-aggregation-in-kubernetes`).

## Cost control
Drop high-cardinality series before remote write with `write_relabel_configs` (`writeRelabelConfigs` in the
Prometheus Operator `remoteWrite` spec).

## Verify
`count by (cluster) (up{job="kubelet"})` in central Grafana lists every cluster with its node count.

## Checked

2026-10-26, against Prometheus configuration docs (external_labels, write_relabel_configs), Prometheus Operator API reference (externalLabels, remoteWrite), Mimir HTTP API and tenant ID docs (grafana/mimir, latest commit 2026-10-24), Thanos receive docs. Confirmed: `externalLabels` and `remoteWrite` with `headers` and write relabeling in the Prometheus Operator spec, Prometheus `write_relabel_configs` and `external_labels`, Mimir `POST /api/v1/push` and the `X-Scope-OrgID` tenant header, Thanos Receive remote write, Thanos sidecar uploads. Removed unconfirmed claims about Cortex, kubernetes-mixin cluster-label config, ruler placement, Fluent Bit/Vector label syntax, and `k8s.cluster.name` as a resource processor attribute.

Method: documentation only; no commands were run.
