---
id: computing-software.cybersecurity-defensive.dex.dex-storage-kubernetes-crd
name: dex-storage-kubernetes-crd
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [kubernetes, crd, storage, rbac]
level: practitioner
status: docs-checked
description: "Run Dex on Kubernetes CRDs with storage type kubernetes and inCluster true, including the ClusterRole it needs to create CRDs."
sources:
  - https://dexidp.io/docs/configuration/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
On Kubernetes, Dex can store state in custom resource definitions, so no external database is needed. Resources live in the `dex.coreos.com` API group.

```yaml
storage:
  type: kubernetes
  config:
    inCluster: true
```

Dex finds its namespace by parsing the service account token mounted into its pod.

RBAC: Dex needs access to the non-namespaced CustomResourceDefinition type so it can create its own CRDs:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: dex
rules:
- apiGroups: ["dex.coreos.com"]
  resources: ["*"]
  verbs: ["*"]
- apiGroups: ["apiextensions.k8s.io"]
  resources: ["customresourcedefinitions"]
  verbs: ["create"]
```

Bind the role to the service account assigned to the Dex pod with a ClusterRoleBinding.

Gotchas:

- Admins should not edit these resources except while debugging. They only store state and are not meant for end users.
- Third party resource (TPR) support was removed. The last version supporting it was v2.17.0, so migrate to CRDs first if you still use TPRs.
- Resources can be queried with `kubectl`, for example the `authcodes.dex.coreos.com` CRD.

(The docs show the RBAC objects with an older beta API version; use the version your cluster serves.)

## Checked

2026-11-08: Read the Dex Storage page in full. Confirmed the CRD storage purpose, the dex.coreos.com group, the `kubernetes` type with `inCluster: true`, namespace detection from the service account token, the ClusterRole rules, the debugging-only warning, TPR removal after v2.17.0 and kubectl access. The page shows the RBAC objects as v1beta1; the skill uses v1 and says so.
Method: documentation only; no commands were run.
