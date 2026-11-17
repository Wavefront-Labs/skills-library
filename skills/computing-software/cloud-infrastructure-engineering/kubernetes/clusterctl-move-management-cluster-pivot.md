---
id: computing-software.cloud-infrastructure-engineering.kubernetes.clusterctl-move-management-cluster-pivot
name: clusterctl-move-management-cluster-pivot
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cluster-api, clusterctl-move, pivot, capi, clusterctl]
level: practitioner
status: docs-checked
description: "Pivot Cluster API management from a bootstrap kind cluster to a self-hosted management cluster with clusterctl move, with pre-checks and rollback."
sources: ["https://github.com/kubernetes-sigs/cluster-api/blob/main/docs/book/src/reference/clusterctl/commands/move.md", "https://github.com/kubernetes-sigs/cluster-api/blob/main/docs/book/src/reference/clusterctl/commands/init.md", "https://github.com/kubernetes-sigs/cluster-api/blob/main/docs/book/src/developer/providers/contracts/clusterctl.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# clusterctl move (bootstrap and pivot)

Documented flow ("Bootstrap and pivot"): create a temporary bootstrap cluster (kind or minikube), `clusterctl init` there, provision the target management cluster with `clusterctl generate cluster ... | kubectl apply -f -`, wait until it is up, get its kubeconfig, run `clusterctl init` against it, `clusterctl move` the Cluster API resources into it, delete the bootstrap cluster. The target needs at least one worker node, otherwise `clusterctl init` times out (the control plane node's NoSchedule taint blocks controllers).

## 1. Prepare the target
```bash
clusterctl get kubeconfig mgmt > mgmt.kubeconfig
clusterctl init --kubeconfig mgmt.kubeconfig --infrastructure aws
clusterctl upgrade plan
```
The provider versions in the target must be at least the versions of the corresponding providers in the source.

## 2. Pre-checks on the source
```bash
clusterctl describe cluster mgmt
clusterctl move --to-kubeconfig mgmt.kubeconfig --dry-run -v 5
```
`--dry-run` only prints logs. Move assumes the cluster is stable: possible races while upgrading, scaling or remediating have not been investigated.

## 3. Move
```bash
clusterctl move --to-kubeconfig mgmt.kubeconfig [--namespace <ns>]
```
Before moving a Cluster, clusterctl sets `Cluster.spec.paused: true` (stopping reconciliation in the source) and waits until the `clusterctl.cluster.x-k8s.io/block-move` annotation is absent from every targeted object. The Cluster created in the target is reconciled as soon as the move completes. Status subresources are never restored; controllers rebuild them.

## 4. Verify and clean up
```bash
KUBECONFIG=mgmt.kubeconfig clusterctl describe cluster mgmt
KUBECONFIG=mgmt.kubeconfig kubectl get machines -A
kind delete cluster --name bootstrap
```

## Gotchas
- The only use case verified by the project's end-to-end tests is the bootstrap scenario; anywhere else, build a validation pipeline first.
- Move is not a backup/restore solution. `clusterctl backup` and `restore` were removed; `clusterctl move --to-directory` and `--from-directory` exist with the same limitations.
- Objects outside the Cluster API object graph move only if they carry the `clusterctl.cluster.x-k8s.io/move` label or are linked to an object with the `clusterctl.cluster.x-k8s.io/move-hierarchy` label (see the provider contract).
- MachineHealthCheck skips Machines of a paused Cluster, so remediation does not fight a move.

## Checked

Checked 2026-10-26 against Cluster API book (main branch, latest commit 2026-10-22; latest release v1.14.3). Confirmed: bootstrap and pivot procedure, pause and block-move behaviour, provider version requirement (at least the source version, not identical), dry-run, move labels, backup limitations.

Method: documentation only; no commands were run.
