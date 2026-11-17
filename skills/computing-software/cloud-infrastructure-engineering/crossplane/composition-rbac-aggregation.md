---
id: computing-software.cloud-infrastructure-engineering.crossplane.composition-rbac-aggregation
name: composition-rbac-aggregation
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [rbac, clusterrole, aggregation, composed-resources]
level: advanced
status: docs-checked
description: "Grant Crossplane access to compose non-Crossplane Kubernetes kinds using an aggregating ClusterRole."
sources:
  - https://docs.crossplane.io/latest/composition/compositions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Crossplane's service account can already create, update and delete resources installed by providers or defined by XRDs (MRs and XRs), plus a few kinds it needs such as Deployments. Any other kind you want to compose needs an RBAC ClusterRole that aggregates to Crossplane's primary ClusterRole.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cnpg:aggregate-to-crossplane
  labels:
    rbac.crossplane.io/aggregate-to-crossplane: "true"
rules:
- apiGroups:
  - postgresql.cnpg.io
  resources:
  - clusters
  verbs:
  - "*"
```

The label `rbac.crossplane.io/aggregate-to-crossplane: "true"` is critical. Without it the role never reaches Crossplane's ClusterRole.

The RBAC manager grants access to MRs and XRs automatically, using the escalate verb. The RBAC manager is optional and enabled by default. If you disable it, you must manually grant Crossplane access to every kind you compose, including XRs and MRs.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Compositions page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the Operations/ingresses example and the closing paragraph about merging roles.

Method: documentation only; no commands were run.
