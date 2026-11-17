---
id: computing-software.cloud-infrastructure-engineering.kubernetes.overlapping-pdbs-eviction-errors
name: overlapping-pdbs-eviction-errors
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, pdb, multiple-pdbs, eviction-api, node-drain, troubleshooting]
level: practitioner
status: docs-checked
description: "Find pods covered by more than one PodDisruptionBudget, which makes the eviction API fail and drains hang, and fix the selectors."
sources: ["https://kubernetes.io/docs/tasks/run-application/configure-pdb/", "https://kubernetes.io/docs/concepts/scheduling-eviction/api-eviction/", "https://github.com/kubernetes/kubernetes/blob/master/pkg/registry/core/pod/storage/eviction.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overlapping PDBs

If a pod matches more than one PDB, the eviction API refuses it:
```
error when evicting pods/"web-6d8f-abc12" -n "shop": This pod has more than one
PodDisruptionBudget, which the eviction subresource does not support.
```
`kubectl drain` keeps retrying a rejected eviction until the pods are gone or its `--timeout`
expires (default: no timeout), so the drain appears to hang.

## Find overlaps
```bash
kubectl get pdb -n shop -o yaml            # read each .spec.selector
kubectl get pods -n shop -l <selector-of-pdb-1> -o name
kubectl get pods -n shop -l <selector-of-pdb-2> -o name
```
A pod name that appears in the output for more than one PDB is covered twice (an empty selector
`{}` matches every pod in the namespace; `matchExpressions` selectors need the same comparison).

## Typical causes
- A chart-level PDB (`app=web`) plus a team-added one (`tier=frontend`).
- An "all pods in namespace" PDB with `selector: {}` added for safety.
- Two releases of one chart with label collisions.

## Fix
One PDB per workload, selecting exactly that workload's pods (use the same labels as the
Deployment selector). Delete or narrow the broad one.

## Verify
```bash
kubectl get pdb -n shop
```
Each PDB shows the expected number of pods and a sensible `ALLOWED DISRUPTIONS`; a later
`kubectl drain <node> --ignore-daemonsets --delete-emptydir-data` in a maintenance window prints
no "more than one PodDisruptionBudget" errors.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website commit 2026-10-25) and kubernetes/kubernetes master (eviction and kubectl drain source, 2026-10-24). Confirmed: the eviction API refuses pods covered by multiple PDBs and the exact error text (source `eviction.go`); `kubectl drain` retries failed evictions (source `drain.go` prints "will retry after") and `--timeout` defaults to zero, meaning infinite; an empty selector matches every pod in the namespace; overlap is reasonable only while transitioning between PDBs. Removed as unconfirmed: the claims about the cluster autoscaler and Karpenter, the `jq` and `awk` pipeline, and the server-side dry-run drain.

Method: documentation only; no commands were run.
