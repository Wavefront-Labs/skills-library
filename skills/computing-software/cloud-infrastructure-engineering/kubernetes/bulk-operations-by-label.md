---
id: computing-software.cloud-infrastructure-engineering.kubernetes.bulk-operations-by-label
name: bulk-operations-by-label
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, label-selectors, delete-by-label, kubectl, scale, bulk-operations]
level: practitioner
status: docs-checked
description: "Delete, scale, restart, annotate and patch many objects at once by label selector, with server dry-runs and set-based selectors to avoid mass accidents."
sources: ["https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_delete/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_scale/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_restart/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_api-resources/", "https://github.com/kubernetes/kubernetes/blob/master/pkg/registry/batch/job/strategy.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bulk operations by label

## Always preview first
```bash
kubectl get pods -l 'env in (dev,test),app!=db' -A
kubectl delete pods -l app=web -n shop --dry-run=server -o name
```

## Common operations
```bash
kubectl delete pods -l app=web -n shop                     # controller recreates them
kubectl delete all,cm,secret,pvc -l app.kubernetes.io/instance=old-release -n shop
kubectl scale deploy -l tier=batch -n jobs --replicas=0
kubectl rollout restart deploy -l team=payments -n shop
kubectl annotate pods -l app=web owner=team-a --overwrite
kubectl label nodes -l node.kubernetes.io/instance-type=m6i.large pool=general
kubectl delete jobs -n ci --field-selector status.successful=1   # exactly 1 succeeded pod
```
Set-based selectors: `-l 'tier in (web,api)'`, `-l '!canary'`, `-l 'release notin (stable)'`.

## Safety notes
- `all` is a resource category, not every kind; see what it covers with
  `kubectl api-resources --categories=all` and name other kinds explicitly.
- An unset variable silently changes the selector (`-l app=$APP` becomes `-l app=`; label
  values may be empty). Use `set -u` in scripts and preview with `--dry-run=server` first.
- `--all` deletes every object of the given types in the namespace, and `-A` ignores the
  current namespace; together they reach every namespace. Avoid both in scripts.
- `--cascade` defaults to `background`; `--cascade=orphan` leaves dependents behind.

## Verify
`kubectl get <kind> -l <selector> -A` returns only what you expect to remain.

## Checked
2026-10-27, against kubernetes/website main (v1.38 dev tree): "Labels and Selectors" and the `kubectl delete`, `scale`, `rollout restart` and `api-resources` references; the Job field selector against `pkg/registry/batch/job/strategy.go` (kubernetes/kubernetes master). Confirmed: equality and set-based selectors (`in`, `notin`, `!key`), empty label values allowed, `-l/--selector` on `scale` and `rollout restart`, `--dry-run=server`, `--all`, `-A`, `--cascade` default `background`, `api-resources --categories`, and that Jobs expose the `status.successful` field selector (the Succeeded count).
Method: documentation only; no commands were run.
