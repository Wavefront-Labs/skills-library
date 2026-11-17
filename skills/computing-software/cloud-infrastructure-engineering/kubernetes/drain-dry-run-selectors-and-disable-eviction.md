---
id: computing-software.cloud-infrastructure-engineering.kubernetes.drain-dry-run-selectors-and-disable-eviction
name: drain-dry-run-selectors-and-disable-eviction
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, drain, disable-eviction, drain-flags, cordon, eviction-api]
level: practitioner
status: docs-checked
description: "Advanced kubectl drain flags: --dry-run to preview, --pod-selector to drain subsets, --disable-eviction to bypass PDBs, --chunk-size and --skip-wait-for-delete-timeout."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_drain/", "https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Advanced kubectl drain flags

## Preview
```bash
kubectl drain node-7 --ignore-daemonsets --delete-emptydir-data --dry-run=client
kubectl drain node-7 --ignore-daemonsets --dry-run=server     # server-side dry run
```
`--dry-run=client` prints "evicting pod ... (dry run)" for the pods it would evict instead of evicting;
neither mode changes the node or pods.

## Drain a subset
```bash
kubectl drain node-7 --pod-selector='app!=critical-agent' --ignore-daemonsets
```
`--pod-selector` is a label selector that filters the pods on the node. Useful to move only specific
workloads off a node. The node is still cordoned.

## Bypassing PDBs (break glass)
```bash
kubectl drain node-7 --ignore-daemonsets --delete-emptydir-data --disable-eviction
```
Uses DELETE instead of the Eviction API, so PodDisruptionBudgets are **not** checked. Use only
when the node is dying anyway and a misconfigured PDB (for example minAvailable 100%) blocks
recovery. Communicate it; the protected app may lose availability.

## Other flags
| Flag | Use |
|---|---|
| `--timeout=10m` | how long to wait before giving up; zero means infinite |
| `--grace-period=30` | seconds given to each pod to terminate; negative uses the pod's own value |
| `--force` | continue even if there are pods that do not declare a controller (they are gone for good) |
| `--skip-wait-for-delete-timeout=60` | skip waiting for a pod whose DeletionTimestamp is older than N seconds (must be greater than 0) |
| `--chunk-size` | page size used when listing pods |

## Workflow
```bash
kubectl drain node-7 --ignore-daemonsets --delete-emptydir-data --timeout=15m
kubectl get pdb -A                         # ALLOWED DISRUPTIONS of 0 blocks eviction
```
Fix the budget or scale the workload rather than reaching for `--disable-eviction` by default.

## Checked
2026-10-23, against the kubectl drain command source on the main branch (flag names, help text, dry-run handling, disable-eviction bypasses PodDisruptionBudgets) and the Kubernetes website safely-drain-a-node task.
Method: documentation only; no commands were run.
