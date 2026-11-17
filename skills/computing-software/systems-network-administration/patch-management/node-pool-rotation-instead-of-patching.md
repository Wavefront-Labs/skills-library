---
id: computing-software.systems-network-administration.patch-management.node-pool-rotation-instead-of-patching
name: node-pool-rotation-instead-of-patching
category: computing-software
field: systems-network-administration
product: patch-management
tags: [node-rotation, node-pool-upgrade, immutable-infrastructure, kubectl-drain, instance-refresh, karpenter, image-patching]
level: advanced
status: docs-checked
description: "Patch Kubernetes nodes and auto-scaled fleets by replacement: AKS/EKS/GKE node image upgrades, drains with PDBs, surge, Karpenter drift and ASG instance refresh."
sources:
  - https://learn.microsoft.com/en-us/azure/aks/node-image-upgrade
  - https://learn.microsoft.com/en-us/cli/azure/aks/nodepool
  - https://docs.aws.amazon.com/eks/latest/userguide/update-managed-node-group.html
  - https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/
  - https://docs.aws.amazon.com/cli/latest/reference/autoscaling/start-instance-refresh.html
  - https://karpenter.sh/docs/concepts/disruption/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rotating nodes instead of patching in place

**Goal:** apply OS patches to cattle nodes by rolling in new nodes built from patched images.

## Kubernetes managed node pools
```bash
# AKS: node OS image only (no Kubernetes version change); set surge first, because
# --max-surge cannot be combined with --node-image-only on the upgrade command
az aks nodepool update -g rg -n np1 --cluster-name aks1 --max-surge 33%
az aks nodepool upgrade -g rg -n np1 --cluster-name aks1 --node-image-only
# EKS managed node group to the latest AMI release
aws eks update-nodegroup-version --cluster-name eks1 --nodegroup-name ng1
# GKE: enable auto-upgrade with maintenance windows, or
gcloud container clusters upgrade gke1 --node-pool pool-1 --location <location>
```
Automatic options: AKS node OS auto-upgrade channel (`NodeImage` or `SecurityPatch`), GKE auto-upgrade, EKS with Karpenter.

## What happens per node
Surge node added, old node cordoned and drained, pods rescheduled, old node deleted. Manual equivalent:
```bash
kubectl cordon node-a
kubectl drain node-a --ignore-daemonsets --delete-emptydir-data --timeout=10m
```

## Make it safe
- **PodDisruptionBudgets** for every replicated workload (`minAvailable` or `maxUnavailable`); a PDB allowing zero disruptions blocks the drain (drains that would breach the budget are blocked).
- At least two replicas spread across nodes/zones (topology spread constraints).
- Readiness probes so traffic only reaches ready pods.
- Surge sized for capacity: higher surge = faster but more temporary nodes.

## Karpenter
Nodes are replaced when they **drift** from their desired specification or reach `spec.template.spec.expireAfter` on the NodePool (default 720h); `spec.disruption.budgets` rate-limits disruption.

## Non-Kubernetes auto-scaling groups
```bash
aws autoscaling start-instance-refresh --auto-scaling-group-name web-asg \
  --preferences '{"MinHealthyPercentage":90,"InstanceWarmup":300}'
```
Azure VM Scale Sets: automatic OS image upgrades (see the VM Scale Sets documentation).

## Gotchas
- Stateful pods with local storage lose data on node deletion; use persistent volumes.
- Long-running jobs block drains; set termination grace and schedule rotations around batch windows.

## Verify
All nodes report the new image version (`kubectl get nodes -o wide`, OS image column) and no workload had more unavailable replicas than its PDB allowed.

## Checked
Date: 2026-10-27. Documentation checked: AKS node image upgrade page and `az aks nodepool` reference (`--node-image-only`, `--max-surge` is mutually exclusive with `--node-image-only`; surge is set with `nodepool update`), AKS node OS auto-upgrade channels (None, Unmanaged, SecurityPatch, NodeImage), AWS CLI references for `eks update-nodegroup-version` and `autoscaling start-instance-refresh` (`MinHealthyPercentage`, `InstanceWarmup`), GKE upgrade page (`--node-pool`), Kubernetes safely-drain page and `kubectl drain` reference (`--ignore-daemonsets`, `--delete-emptydir-data`, `--timeout`), Karpenter disruption and NodePool pages (drift, `expireAfter` default 720h, budgets). The AKS command in the earlier text was invalid and is corrected.

Method: documentation only; no commands were run.
