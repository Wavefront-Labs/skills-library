---
id: computing-software.cloud-infrastructure-engineering.kubernetes.serviceaccount-rbac-bindings
name: serviceaccount-rbac-bindings
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, rbac, serviceaccount-rolebinding, service-account, rolebinding]
level: practitioner
status: docs-checked
description: "Grant a ServiceAccount exactly the permissions it needs: subject syntax, cross-namespace bindings, the serviceaccounts group, and verification with can-i --as."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/rbac/#service-account-permissions", "https://kubernetes.io/docs/reference/access-authn-authz/rbac/#referring-to-subjects", "https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RBAC for ServiceAccounts

## Identity
A ServiceAccount `ci` in namespace `build` authenticates as user
`system:serviceaccount:build:ci`, with groups `system:serviceaccounts` and
`system:serviceaccounts:build`.

## Binding
```bash
kubectl -n build create serviceaccount ci
kubectl -n apps create role deployer --verb=get,list,watch,patch,update --resource=deployments
kubectl -n apps create rolebinding ci-deployer --role=deployer --serviceaccount=build:ci
```
YAML form of the subject:
```yaml
subjects:
- kind: ServiceAccount
  name: ci
  namespace: build        # required for ServiceAccount subjects
```
The RoleBinding lives in the namespace where access is granted (`apps`); the SA can live
elsewhere (`build`). Omitting `namespace` in the subject is a common silent failure.

## Groups of ServiceAccounts
```yaml
subjects:
- kind: Group
  name: system:serviceaccounts:monitoring   # every SA in the monitoring namespace
  apiGroup: rbac.authorization.k8s.io
```
Never bind anything meaningful to `system:serviceaccounts` (all SAs in the cluster).

## The default ServiceAccount
Every pod without `serviceAccountName` uses `default`. Granting permissions to `default`
grants them to every such pod in the namespace. Create one SA per workload instead.

## Verify
```bash
kubectl auth can-i patch deployments -n apps --as=system:serviceaccount:build:ci     # yes
kubectl auth can-i delete deployments -n apps --as=system:serviceaccount:build:ci    # no
kubectl auth can-i --list -n apps --as=system:serviceaccount:build:ci
```

## Gotchas
- Pod spec `serviceAccountName` must match an existing ServiceAccount; otherwise the admission
  controller rejects the Pod.
- Changing a RoleBinding's `roleRef` is forbidden; delete and recreate it.

## Checked

Checked 2026-10-27 against Kubernetes website content (main, v1.38 dev tree) and the v1.37 line (latest release at review time).

- ServiceAccount username `system:serviceaccount:<ns>:<name>` and groups `system:serviceaccounts` / `system:serviceaccounts:<ns>` confirmed in the RBAC page.
- `kubectl create rolebinding --serviceaccount=<ns>:<name>` syntax and the warning against binding to `system:serviceaccounts` confirmed in the RBAC page.
- `roleRef` immutability confirmed; missing ServiceAccount rejected by the admission controller confirmed in the service accounts admin page.
- `kubectl auth can-i --as=` and `--list` confirmed in the authorization page and kubectl source.

Method: documentation only; no commands were run.
