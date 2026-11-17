---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-create-role-imperative
name: kubectl-create-role-imperative
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, rbac, kubectl-create-role, kubectl-create-rolebinding, clusterrole, kubectl-create]
level: practitioner
status: docs-checked
description: "Create Roles, ClusterRoles and bindings imperatively with kubectl create, including resource-names, subresources and aggregation flags, fast and correct."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/kubectl_create_role/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/kubectl_create_rolebinding/", "https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/kubectl/pkg/cmd/create", "https://kubernetes.io/docs/reference/access-authn-authz/rbac/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Imperative RBAC with kubectl create

## Roles
```bash
kubectl -n dev create role pod-reader --verb=get,list,watch --resource=pods
kubectl -n dev create role log-reader --verb=get --resource=pods/log           # subresource
kubectl -n dev create role cm-one --verb=get,update --resource=configmaps --resource-name=app-config
kubectl create clusterrole node-reader --verb=get,list,watch --resource=nodes
kubectl create clusterrole metrics --verb=get --non-resource-url=/metrics
kubectl create clusterrole deploy-mgr --verb='*' --resource=deployments.apps   # group-qualified
kubectl create clusterrole monitoring-agg --aggregation-rule="rbac.example.com/aggregate-to-monitoring=true"
```
Repeat `--verb` and `--resource` or use commas. Resource with a group: `deployments.apps`,
`ingresses.networking.k8s.io`.

## Bindings
```bash
kubectl -n dev create rolebinding alice-read --role=pod-reader --user=alice
kubectl -n dev create rolebinding team-view --clusterrole=view --group=dev-team    # ClusterRole scoped to ns
kubectl -n dev create rolebinding ci --clusterrole=edit --serviceaccount=build:ci
kubectl create clusterrolebinding ops-nodes --clusterrole=node-reader --group=ops
```

## Generate YAML for review
```bash
kubectl -n dev create role pod-reader --verb=get,list --resource=pods --dry-run=client -o yaml > role.yaml
```

## Gotchas
- `--resource=pods` does not include `pods/log` or `pods/exec`; list subresources explicitly.
- `create` fails if the object exists; for idempotence pipe through
  `--dry-run=client -o yaml | kubectl apply -f -`.
- `roleRef` is immutable; to change it delete and recreate the binding.
- You can create or update a Role or ClusterRole only if you already hold all the permissions it contains (at the same scope) or have the `escalate` verb on `roles`/`clusterroles`; for bindings you need the permissions in the referenced role or the `bind` verb on it.

## Verify
```bash
kubectl -n dev describe role pod-reader
kubectl auth can-i list pods -n dev --as=alice
```

## Checked
Checked 2026-10-24 against the kubectl create role, clusterrole and rolebinding source (main) and the RBAC documentation (v1.37): flags `--verb`, `--resource` (resource.group/subresource), `--resource-name`, `--non-resource-url`, `--aggregation-rule`, `--role`, `--clusterrole`, `--user`, `--group`, `--serviceaccount=<namespace>:<name>`; subresources are listed explicitly; immutable `roleRef`; `escalate` and `bind` verbs; a RoleBinding may reference a ClusterRole; `kubectl auth can-i --as`.
Method: documentation only; no commands were run.
