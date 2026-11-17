---
id: computing-software.devops-ci-cd.flux.kustomization-service-account-impersonation
name: kustomization-service-account-impersonation
category: computing-software
field: devops-ci-cd
product: flux
tags: [kustomization, serviceaccountname, rbac, impersonation, multitenancy]
level: sme
status: docs-checked
description: "Restrict what a Flux Kustomization may change by impersonating a namespaced ServiceAccount via spec.serviceAccountName."
sources:
  - https://fluxcd.io/flux/components/kustomize/kustomizations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default a Kustomization applies as cluster admin and can touch cluster-scoped and namespaced objects. To limit it, set `.spec.serviceAccountName`; the controller then impersonates that ServiceAccount, and Kubernetes RBAC decides what it may create, change or delete.

Example confining reconciliation to one namespace:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: flux
  namespace: webapp
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: webapp-reconciler
  namespace: webapp
rules:
  - apiGroups: ['*']
    resources: ['*']
    verbs: ['*']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: webapp-reconciler
  namespace: webapp
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: webapp-reconciler
subjects:
  - kind: ServiceAccount
    name: flux
    namespace: webapp
```

Then reference it from the Kustomization:

```yaml
spec:
  serviceAccountName: flux
```

The ServiceAccount is looked up in the Kustomization namespace. With `.spec.kubeConfig` (remote cluster) the impersonated account must exist in the same-named namespace on the target cluster.

For multi-tenant clusters, enforce this for every tenant with the kustomize-controller flag `--default-service-account=<name>`, so a Kustomization without the field cannot run with admin rights.

## Checked

2026-11-03. Read the Kustomization reference (fluxcd.io/flux/components/kustomize/kustomizations/): default cluster-admin apply, `.spec.serviceAccountName` impersonation, RBAC example, `--default-service-account` and the remote-cluster namespace rule. Nothing removed.

Method: documentation only; no commands were run.
