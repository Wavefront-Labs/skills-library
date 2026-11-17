---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-deploy-prometheus-with-rbac
name: prometheus-operator-deploy-prometheus-with-rbac
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [deploy-prometheus, serviceaccount, clusterrole, clusterrolebinding, prometheus-rbac, platform-guide]
level: intro
status: docs-checked
description: "Deploy a first Prometheus with its ServiceAccount, ClusterRole and ClusterRoleBinding, and explain why it needs read access to the API."
sources:
  - https://prometheus-operator.dev/docs/platform/platform-guide/
  - https://prometheus-operator.dev/docs/platform/rbac/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Prometheus instance needs RBAC to discover and scrape targets. Create three objects, then the `Prometheus` resource.

1. `ServiceAccount` named `prometheus`.
2. `ClusterRole` named `prometheus`:
   - `get`, `list`, `watch` on core `nodes`, `nodes/metrics`, `services`, `endpoints`, `pods`;
   - `get` on `configmaps` (the sidecar pulls rule files from ConfigMaps);
   - `get`, `list`, `watch` on `discovery.k8s.io` `endpointslices` and `networking.k8s.io` `ingresses`;
   - `get` on non-resource URL `/metrics` (to scrape the API server).
3. `ClusterRoleBinding` binding the role to the ServiceAccount in its namespace.

Then:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: prometheus
spec:
  serviceAccountName: prometheus
```
Watch it come up with `kubectl get -n default prometheus prometheus -w`.

## Notes
Prometheus only reads objects, hence read verbs only. The ServiceAccount is named in the `Prometheus` object, and it is the cluster admin who must create the ClusterRole and binding. The ClusterRole is reusable by many instances, so a ClusterRoleBinding is used rather than a RoleBinding. Without `serviceMonitorSelector` or `podMonitorSelector` the instance scrapes nothing from monitors; see the resource selectors skill.

## Checked

2026-11-08. Read the platform guide and the RBAC page in full. ClusterRole rules, binding and Prometheus manifest match; no changes needed.

Method: documentation only; no commands were run.
