---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-aggregate-crd-clusterroles
name: prometheus-operator-aggregate-crd-clusterroles
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [aggregated-clusterroles, rbac-view-edit-admin, crd-permissions, multi-tenant, aggregate-to-edit]
level: practitioner
status: docs-checked
description: "Give namespace users view, edit and admin access to Prometheus Operator CRDs by aggregating ClusterRoles into the built-in Kubernetes roles."
sources:
  - https://prometheus-operator.dev/docs/platform/rbac-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To let tenants manage monitoring objects with the standard roles, define aggregated ClusterRoles labelled for the built-in `view`, `edit` and `admin` roles (Kubernetes 1.9 and later).

```yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: prometheus-crd-view
  labels:
    rbac.authorization.k8s.io/aggregate-to-admin: "true"
    rbac.authorization.k8s.io/aggregate-to-edit: "true"
    rbac.authorization.k8s.io/aggregate-to-view: "true"
rules:
- apiGroups: ["monitoring.coreos.com"]
  resources: ["alertmanagers", "alertmanagerconfigs", "prometheuses", "prometheusrules", "servicemonitors", "podmonitors", "probes"]
  verbs: ["get", "list", "watch"]
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: prometheus-crd-edit
  labels:
    rbac.authorization.k8s.io/aggregate-to-edit: "true"
    rbac.authorization.k8s.io/aggregate-to-admin: "true"
rules:
- apiGroups: ["monitoring.coreos.com"]
  resources: ["alertmanagers", "alertmanagerconfigs", "prometheuses", "prometheusrules", "servicemonitors", "podmonitors", "probes"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
```

Effect: users with `view` can read the CRDs in their namespaces; users with `edit` or `admin` can create, change and delete them. The example lists seven resources; add `scrapeconfigs`, `prometheusagents` and `thanosrulers` yourself if your tenants should manage those too.

## Checked

2026-11-08. Read the RBAC for CRDs page in full. ClusterRole labels, resources and verbs match; the Kubernetes 1.9 note matches. Removed an unsourced sentence about selectors.

Method: documentation only; no commands were run.
