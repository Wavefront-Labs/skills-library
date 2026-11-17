---
id: computing-software.cloud-infrastructure-engineering.kubernetes.namespace-full-object-inventory
name: namespace-full-object-inventory
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, namespaces, namespace-inventory, api-resources, kubectl, cleanup]
level: practitioner
status: docs-checked
description: "List every object in a namespace across all namespaced API types, including custom resources, for audits, migrations and stuck namespace deletion."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_api-resources/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/", "https://kubernetes.io/docs/tasks/administer-cluster/namespaces/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Listing every object in a namespace

`kubectl get all` covers only the kinds in the `all` category
(`kubectl api-resources --categories=all`). To see everything:

```bash
NS=shop
kubectl api-resources --verbs=list --namespaced -o name \
  | xargs -n1 -I{} kubectl get {} -n $NS --ignore-not-found --show-kind --no-headers 2>/dev/null
```
Names only, skipping core events:
```bash
for r in $(kubectl api-resources --verbs=list --namespaced -o name | grep -v '^events'); do
  out=$(kubectl get "$r" -n $NS -o name 2>/dev/null); [ -n "$out" ] && echo "$out"
done
```

## Uses
- Audit what a tenant owns before deleting the namespace.
- Find leftovers keeping a namespace `Terminating` (deletion is asynchronous, and a finalizer
  nobody handles leaves it stuck); objects with finalizers show up here:
  ```bash
  for r in $(kubectl api-resources --verbs=list --namespaced -o name); do
    kubectl get "$r" -n $NS -o json 2>/dev/null | jq -r '.items[] | select(.metadata.finalizers) | "\(.kind)/\(.metadata.name) \(.metadata.finalizers)"'
  done
  ```
- Export for migration: add `-o yaml` and strip status and server fields (or use Velero).

## Gotchas
- Errors for one API group often mean its aggregated APIService is unavailable; check
  `kubectl get apiservices` and fix or remove the stale one before deleting the namespace.
- `events` and `events.events.k8s.io` are noisy; skip them.
- RBAC: you see only what you can list; run as cluster-admin for a complete audit.

## Verify
The count of objects matches what deletion would remove; nothing unexpected (old CRs,
leftover PVCs) remains.

## Checked
2026-10-27, against kubernetes/website main (v1.38 dev tree): `kubectl api-resources` and `kubectl get` references and "Share a Cluster with Namespaces". Confirmed: `api-resources --verbs`, `--namespaced` (default true), `-o name`, `--categories`; `get --ignore-not-found`, `--show-kind`; namespace phases `Active`/`Terminating`, asynchronous deletion, and namespaces stuck in `Terminating` on an unhandled finalizer.
Method: documentation only; no commands were run.
