---
id: computing-software.cloud-infrastructure-engineering.observability.multi-cluster-and-cross-region-telemetry
name: multi-cluster-and-cross-region-telemetry
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [multi-cluster-collector, cross-cluster-telemetry, collector-deployment, otel-collector, multi-tenancy]
level: advanced
status: draft
description: "Design telemetry pipelines across many clusters and regions: per-cluster agents and gateways, cluster identity, secure export, egress cost, regional backends."
sources: ["https://opentelemetry.io/docs/collector/deployment/gateway/", "https://opentelemetry.io/docs/platforms/kubernetes/collector/components/", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/bearertokenauthextension"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-cluster and cross-region telemetry

## Reference topology
Per cluster: node agents (DaemonSet) -> in-cluster gateway (Deployment, 2+ replicas) -> **regional** backend
(Mimir/Loki/Tempo or vendor region). Global view via query-time federation (Grafana data sources per region, or
Mimir/Thanos querying multiple stores) rather than shipping everything to one region.

## Cluster identity
Stamp every signal with `k8s.cluster.name` (and `cloud.region`) at the cluster gateway:
```yaml
processors:
  resource/cluster:
    attributes:
      - {key: k8s.cluster.name, value: "${env:CLUSTER_NAME}", action: upsert}
      - {key: cloud.region, value: "${env:REGION}", action: insert}
```
Prometheus-scraped metrics need it as an external label too (`external_labels: {cluster: ...}`) or series from two
clusters collide.

## Secure cross-cluster export
- TLS everywhere; authenticate gateways to the central endpoint with `bearertokenauth`, `oauth2client`, or mTLS.
- Tenant header per cluster/team: `headers: {X-Scope-OrgID: ${env:TENANT}}` or `headers_setter` extension for dynamic.
- Central receivers behind an L7 load balancer that handles gRPC; restrict source IPs.

## Cost and resilience
- Cross-region/cloud egress is often the largest telemetry cost: sample and filter at the cluster gateway before
  it leaves the region; compress (`compression: zstd`).
- Persistent sending queue (`file_storage`) on gateways to survive WAN outages; size for the outage you accept.
- Keep alerting regional: rules evaluated next to the data, so a WAN partition does not blind each region.

## Fleet config
Same collector config per cluster rendered with per-cluster values (Helm values, Kustomize overlays, Argo CD
ApplicationSet), or OpAMP for central management.

## Verify
`count by (k8s_cluster_name) (target_info)` (or `group by (cluster) (up)`) lists every cluster; no series without a
cluster label.
