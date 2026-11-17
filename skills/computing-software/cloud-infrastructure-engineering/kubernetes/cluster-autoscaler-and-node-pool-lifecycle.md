---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cluster-autoscaler-and-node-pool-lifecycle
name: cluster-autoscaler-and-node-pool-lifecycle
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cluster-autoscaler, karpenter, node-pool, scale-down, scale-up, poddisruptionbudget, scale-down-disabled, node-group, autoscaling, bin-packing, consolidation]
level: advanced
status: docs-checked
description: "How cluster-autoscaler decides to scale node pools up and down, what blocks a scale-down, and how it differs from Karpenter's node-level bin-packing."
sources: ["https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md", "https://kubernetes.io/docs/concepts/cluster-administration/node-autoscaling/", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.15/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster autoscaler and node pool lifecycle

**Goal:** understand why a node pool scales up or refuses to scale down, so "why is
this node still here" or "why didn't this pod get a node" stops being a mystery. This
sits alongside manual node lifecycle
(`computing-software.cloud-infrastructure-engineering.kubernetes.node-maintenance-cordon-drain-taint`)
as the automated version of taking nodes in and out of service.

## 1. Scale-up: triggered by unschedulable pods, not utilization
- cluster-autoscaler (CA) watches for `Pending` pods with a scheduling failure
  (`FailedScheduling` event citing insufficient resources, taints, or affinity it can
  fix by adding a node) and simulates whether adding a node from a configured node
  group would let the pod schedule. It does **not** scale up based on aggregate CPU/
  memory utilization alone — a cluster at 95% utilization with no pending pods doesn't
  trigger scale-up; a single pending pod that fits nowhere does.
- It picks **which** node group to expand by simulating each candidate and choosing by
  configured expander strategy (`least-waste` is the default — least idle CPU and then memory
  after scale-up; `most-pods`, `least-nodes`, `price`, `priority` and `random` are alternatives) — the choice matters when
  multiple node groups could satisfy a pending pod differently.
- A pod that's unschedulable for a reason CA can't fix by adding capacity (missing
  PVC, bad nodeSelector matching nothing, a pod that simply won't fit any configured
  node group's instance type) stays `Pending` forever with no scale-up attempt — check
  `kubectl describe pod` for the actual `FailedScheduling` reason before assuming CA
  should have acted.

## 2. Scale-down: the much more conservative half
A node is a scale-down candidate only if, for a sustained period (`--scale-down-
unneeded-time`, default 10m), **all** of these hold:
- Utilization below `--scale-down-utilization-threshold` (default 0.5), measured as the larger
  of the CPU-request and memory-request ratios against the node's allocatable.
- No pod on it blocks eviction: no pod with a restrictive PDB, no pod using local storage
  (`hostPath`, or `emptyDir` without `medium: Memory`) unless annotated
  `safe-to-evict: "true"` or `safe-to-evict-local-volumes`, no pod lacking a controller (bare pod)
  unless annotated `safe-to-evict: "true"`, no kube-system pod without a PDB (unless annotated
  `safe-to-evict: "true"`), and no pod annotated `cluster-autoscaler.kubernetes.io/safe-to-evict: "false"`.
- The node doesn't have the `cluster-autoscaler.kubernetes.io/scale-down-disabled:
  "true"` annotation.
- Even then, CA drains and removes the node the same way a manual drain would —
  respecting PDBs — so a node "stuck" and never scaling down is almost always one of
  the above conditions, not a bug. Check `kubectl describe configmap cluster-
  autoscaler-status -n kube-system` for CA's own reasoning on why a specific node
  wasn't removed.

## 3. Karpenter contrast (node-level, not pool-level)
- Cluster-autoscaler scales **predefined node groups** (ASGs, managed node pools) up
  and down — the instance types/sizes within a group are fixed ahead of time.
- **Karpenter** (and similar just-in-time provisioners) provisions individual nodes
  matching a pod's actual requirements directly, from a flexible instance-type
  selection, with no pre-defined node group to scale — it can right-size per pending
  pod rather than picking from a small number of fixed shapes.
- Karpenter's **consolidation** is configured per NodePool (`consolidationPolicy`,
  `consolidateAfter`); with `WhenEmptyOrUnderutilized` it considers any node that can be removed
  or replaced to reduce cost, which is a broader test than CA's utilization threshold. Nodes
  can therefore churn more; workloads sensitive to rescheduling need PDBs sized accordingly.
- Both respect PDBs when draining, but the annotations differ: Karpenter uses
  `karpenter.sh/do-not-disrupt` rather than the CA `safe-to-evict` annotations.

## Gotchas
- `scale-down-disabled: "true"` on a node is sticky and easy to forget — set during a
  troubleshooting session and never removed, it silently exempts that node from
  cost-saving scale-down indefinitely.
- A Deployment relying on local `emptyDir` cache data (not marked safe via
  config) will quietly pin its node against scale-down — intentional sometimes, an
  accident other times; check it's deliberate.
- Multiple node groups with overlapping capability but different cost (spot vs
  on-demand): the default `least-waste` expander does not look at price, and `price` works only
  on GCE, GKE and Equinix Metal, so use the `priority` expander to prefer the cheaper group.

## Verify
- [ ] `kubectl describe configmap cluster-autoscaler-status -n kube-system` is checked
      before assuming a stuck scale-up/down is a bug rather than a documented
      precondition not met.
- [ ] No node carries `scale-down-disabled: "true"` without a currently-valid reason.
- [ ] kube-system pods that are genuinely safe to evict are covered by a PDB (or carry the
      `safe-to-evict: "true"` annotation), rather than blocking scale-down by omission.
- [ ] Node-group expander strategy is a deliberate choice (`least-waste`/`priority`/
      etc.), not left at default without considering cost implications across mixed
      instance types.

## Checked

Checked 2026-10-24. The documentation checked is the Cluster Autoscaler FAQ and provider READMEs in kubernetes/autoscaler (master, 2026-10-24); the autoscaler binary source now lives in kubernetes-sigs/cluster-autoscaler. Karpenter statements were checked against the Karpenter v1.15 docs source (aws/karpenter-provider-aws, website/content/en/v1.15 concepts/disruption.md).
- Scale-up trigger, expander list and default, scale-down utilization definition, blockers (PDBs, local storage, bare pods, kube-system pods) and the `safe-to-evict`, `safe-to-evict-local-volumes` and `scale-down-disabled` annotations, `price` expander limits: CA FAQ.
- Karpenter `consolidationPolicy` / `consolidateAfter`, `WhenEmptyOrUnderutilized` meaning, PDB-respecting drain and the `karpenter.sh/do-not-disrupt` annotation: Karpenter disruption docs.

Method: documentation only; no commands were run.
