---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.kubernetes-cost-estimation
name: kubernetes-cost-estimation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, planning-and-estimating, kubernetes-cost-estimation, cluster-sizing, bin-packing, node-allocatable, cost-estimation]
level: advanced
status: docs-checked
description: "Estimate Kubernetes node count from pod requests and node allocatable (capacity minus kube-reserved, system-reserved, eviction), then price the nodes."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Estimating Kubernetes node count

## What the Kubernetes docs confirm
- **Allocatable** is the amount of compute resources available for pods on a node; the
  scheduler does not over-subscribe it. CPU, memory and ephemeral-storage are supported.
  It is shown by `kubectl describe node` and in the `v1.Node` object.
- Resources can be reserved for two categories of system daemons in the kubelet:
  `kubeReserved` (Kubernetes system daemons) and `systemReserved` (OS system daemons).
  Example values in the docs are `{cpu: 100m, memory: 100Mi, ephemeral-storage: 1Gi, pid=1000}`
  for each; these are examples, not defaults.
- Hard eviction thresholds (`evictionHard`) also reduce what pods can use; the docs' example
  is `memory.available: "<500Mi"`.

## Steps
1. List workloads with replica counts and CPU and memory requests. The scheduler packs by
   requests, so pods without requests make the estimate meaningless.
2. Add per-node DaemonSet requests multiplied by node count.
3. Read allocatable per node from `kubectl describe node` on a node of the candidate shape
   (managed services set their own reservations).
4. Choose a node shape, divide total requests by allocatable per node for CPU and for memory,
   and take the larger count. Add headroom for node failure and rolling updates; the
   packing target and headroom are your own choice, the docs give none.
5. Price the nodes at your purchase mix and add non-node lines: control plane fee, load
   balancers, persistent volumes, egress, observability. Prices come from your provider's
   current pricing page.

## Verify
- [ ] Node count derived from requests, allocatable, packing target and failure headroom.
- [ ] Non-node lines are present.

## Checked
Method: docs-checked 2026-11-09 against the Kubernetes "Reserve Compute Resources for System Daemons" page (downloaded and read around the cited passages).
Removed as unconfirmed: provider pricing pages (EKS, GKE, AKS: unreadable hosts) and all price, free-tier and credit figures, DaemonSet sizing numbers, the 4 vCPU/16 GiB allocatable example, 70-80% packing target, N+1 per AZ, 1:4 and 1:8 ratios, Fargate/Autopilot formula, worked 13-node example, spot and small-cluster gotchas, VPA/Goldilocks.
