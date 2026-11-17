---
id: computing-software.cloud-infrastructure-engineering.rook.rook-ceph-cluster-helm-chart
name: rook-ceph-cluster-helm-chart
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [helm, ceph-cluster-chart, cephclusterspec, operatornamespace, toolbox-enabled, ingress]
level: practitioner
status: docs-checked
description: "Install the rook-ceph-cluster Helm chart that creates CephCluster, pools, filesystem and object store plus storage classes, and set monitoring and toolbox values."
sources:
  - https://rook.io/docs/rook/latest-release/Helm-Charts/ceph-cluster-chart/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The cluster chart packages templates that optionally create the CephCluster, CephFilesystem and CephObjectStore CRs, storage classes for RBD, CephFS and RGW buckets, an ingress for the dashboard, and the toolbox. It needs Helm 3.13+ and the operator chart installed first.

Before installing, review `values.yaml`:
- If the operator is outside `rook-ceph`, set `operatorNamespace`.
- Set `cephClusterSpec` for your cluster; its defaults are only an example.
- Remove the `monitoring` section from `cephClusterSpec`, because monitoring is configured separately in the Helm settings.
- Default `cephBlockPools`, `cephFileSystems` and `cephObjectStores` each create one resource and its storage class.
- All Ceph components carry default pod resources; adjust them for production load or disable them for test clusters.

The docs tip: write a small `values.yaml` containing only your overrides instead of copying the whole default file.

Selected values:
- `clusterName`: the CephCluster `metadata.name`, default same as the namespace.
- `monitoring.enabled` (false) needs Prometheus pre-installed; `monitoring.createPrometheusRules` (false); `monitoring.metricsDisabled` (false).
- `monitoring.rulesNamespaceOverride`: set the same namespace for all clusters in one Kubernetes cluster to avoid duplicate alerts.
- `toolbox.enabled`: false by default.
- `ingress.dashboard` and `route.dashboard` expose the dashboard (an HTTPRoute for the latter).

## Checked

2026-11-03. Confirmed against the Ceph Cluster Helm chart page: Helm 3.13+, the values.yaml review list, clusterName, monitoring values, toolbox.enabled default false and the dashboard ingress and route. Removed: nothing.

Method: documentation only; no commands were run.
