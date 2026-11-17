---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-create-pdb
name: kubectl-create-pdb
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, pdb, kubectl-create-pdb, minavailable, poddisruptionbudget]
level: practitioner
status: docs-checked
description: "Create PodDisruptionBudgets with kubectl create pdb using counts or percentages, pick min-available versus max-unavailable, and check the result."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/kubectl_create_poddisruptionbudget/", "https://kubernetes.io/docs/tasks/run-application/configure-pdb/", "https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/kubectl/pkg/cmd/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl create pdb

```bash
kubectl create pdb web --selector=app=web --min-available=2
kubectl create pdb web --selector=app=web --max-unavailable=1
kubectl create pdb web --selector=app=web --max-unavailable=25%
kubectl create pdb web --selector=app=web --min-available=50% --dry-run=client -o yaml > pdb.yaml
```
Specify exactly one of `--min-available` / `--max-unavailable`. Use the workload controller's `.spec.selector` as the PDB selector.

## Which to use
- `maxUnavailable: 1` (or a percentage) scales with replica changes. A common choice for Deployments.
- `minAvailable: N` for quorum systems where the absolute number matters (3 of 5).
- `maxUnavailable: 0` (or `minAvailable: 100%`) permits no voluntary evictions of those pods, so node drains that must evict them cannot proceed.

Percentages are rounded up for both `minAvailable` and `maxUnavailable` (so `maxUnavailable: 10%`
of 3 pods allows 1). `kubectl create pdb --selector` accepts only equality-based requirements.

## Check it
```bash
kubectl get pdb web
# NAME  MIN AVAILABLE  MAX UNAVAILABLE  ALLOWED DISRUPTIONS  AGE
kubectl describe pdb web       # expected pods, current healthy, desired healthy
```
`ALLOWED DISRUPTIONS 0` with all pods healthy means the budget is too strict for the replica count.

## Gotchas
- Follow the Kubernetes PDB page for how a PDB's selector relates to the controller's selector.

## Checked
Checked 2026-10-24 against the kubectl create pdb source (main) and the PodDisruptionBudget task page (v1.37): flags `--selector`, `--min-available`, `--max-unavailable`; exactly one of the two is required; percentages round up for both; the PDB selector comes from the controller's `.spec.selector`. Removed unconfirmed claims about shared labels, deletion and autoscaler behaviour.
Method: documentation only; no commands were run.
