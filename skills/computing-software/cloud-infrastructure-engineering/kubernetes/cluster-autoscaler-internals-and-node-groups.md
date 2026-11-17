---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cluster-autoscaler-internals-and-node-groups
name: cluster-autoscaler-internals-and-node-groups
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cluster-autoscaler, ca, node-groups, asg, scale-up, scale-down, expander, simulation, scale-down-utilization-threshold, pdb, taints, overprovisioning, bin-packing, safe-to-evict, scale-down-blockers, nottriggerscaleup]
level: advanced
status: docs-checked
description: "Cluster Autoscaler's scale-up simulation, expander strategies, and the scale-down safety checks that make nodes refuse to drain."
sources: ["https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md", "https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/README.md", "https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#what-are-expanders"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Cluster Autoscaler internals and node groups

**Goal:** understand *why* CA added or refused to remove a node, not just that it did — the
scheduling simulation and the scale-down checklist are both deterministic and debuggable.

## 1. Scale-up: it's a scheduler simulation, not a metric
CA does not read CPU/memory utilisation to decide scale-up. Every loop (default 10s) it looks at
**unschedulable pods** (`status.conditions[].reason == Unschedulable`) and, for each configured
node group template, simulates whether a hypothetical new node of that shape would let the pod
schedule. The FAQ calls this simulation "quite simplified" compared with the real scheduler, so
it may need several iterations before every pod is scheduled. When several node groups would
help, the **expander** chooses.
- A pod counts as unschedulable once the scheduler has set its PodScheduled condition to false
  with reason `Unschedulable`; CA checks every `--scan-interval` (default 10s).
  `--new-pod-scale-up-delay` (default 0s) makes CA ignore pods younger than a given age.
- Pods that don't fit **any** configured node group's template are never scaled for — CA records
  `NotTriggerScaleUp` on the pod and does nothing; check node group templates (and the pod's
  nodeSelector and required node affinity, which CA respects) rather than metrics.

## 2. Expanders — the ranking strategy when multiple node groups fit
Set via `--expander` (default `least-waste`; from 1.23.0 several can be given, comma-separated,
each filtering the previous output; an expander may not appear twice, and ties left at the end
are broken randomly):
- `least-waste` — selects the group that will have the least idle CPU (then unused memory) after
  scale-up. Useful with different classes of nodes (high-CPU, high-memory).
- `most-pods` — selects the group that can schedule the most pending pods when scaled up;
  useful with nodeSelector. It does not prefer bigger nodes over smaller ones.
- `least-nodes` — selects the group that will use the fewest nodes after scale-up.
- `priority` — selects the group with the highest priority assigned by you (configured through
  the priority expander's ConfigMap).
- `price` — selects the cheapest group; currently works only for GCE, GKE and Equinix Metal.
- `random` — picks any node group.
- Chaining, for example `--expander=priority,least-waste`, uses `least-waste` as the fallback when
  `priority` selects several groups.

## 3. Scale-down: the checklist a node must pass
A node becomes a scale-down candidate only after ALL of these hold for
`--scale-down-unneeded-time` (default 10m) continuously:
1. The larger of (sum of CPU requests / allocatable CPU) and (sum of memory requests / allocatable
   memory) on the node is below `--scale-down-utilization-threshold` (default 0.5). DaemonSet and
   mirror pods are included unless `--ignore-daemonsets-utilization` or
   `--ignore-mirror-pods-utilization` is set.
2. No pod on it is missing a controller (bare pods block scale-down unless annotated
   `cluster-autoscaler.kubernetes.io/safe-to-evict: "true"`).
3. No pod has `cluster-autoscaler.kubernetes.io/safe-to-evict: "false"`.
4. No pod has a restrictive **PodDisruptionBudget**.
5. No pod uses local storage: `hostPath` and `emptyDir` without `medium: Memory` count as local
   (ConfigMaps, Secrets, projected volumes and memory-backed `emptyDir` do not), unless the pod
   is annotated `safe-to-evict: "true"` or lists the volumes in
   `cluster-autoscaler.kubernetes.io/safe-to-evict-local-volumes`.
6. kube-system pods (other than DaemonSet or mirror pods) block removal unless a PDB covers
   them (`--skip-nodes-with-system-pods`, default true).
7. Every pod can be moved to another node in CA's scheduling simulation, and the node does not
   carry the `scale-down-disabled` annotation.
- When the checklist passes, CA drains the node and terminates it. Pods get at most
  `--max-graceful-termination-sec` (default 600s) to stop; after that the node is terminated
  anyway. CA terminates one non-empty node at a time.
- `--scale-down-delay-after-add` (default 10m) is how long after a scale-up scale-down evaluation
  resumes; tune it down if your batch workload churn is faster than that.

## 4. Node group balancing and `--balance-similar-node-groups`
The flag detects similar node groups and balances the number of nodes between them. The FAQ
recommends separate node groups per zone (so CA knows which group creates nodes in a given zone)
together with `--balance-similar-node-groups` to keep nodes balanced across zones.

## Gotchas
- CA does not enforce node group size by default: below the configured minimum it scales up
  only when unschedulable pods exist, and above the maximum it scales down only through its normal
  scale-down logic (see the FAQ question on clusters below minimum or above maximum).
- Pending pods that need a **specific zone** (via a PV's `nodeAffinity`) can only trigger scale-up in
  node groups in that zone; check `kubectl describe pod` for the exact unschedulable reason before
  blaming CA.
- Since Kubernetes 1.12 the CA version number matches the Kubernetes minor release, and the README
  recommends using the CA release meant for your control plane version.
- Pod priority matters: pods with priority below `--expendable-pods-priority-cutoff` (default -10)
  do not trigger scale-up, and CA does not scale up for an unschedulable pod that is already
  waiting for a lower-priority pod to be preempted.

## Verify
- [ ] The cluster-autoscaler log (`kubectl -n kube-system logs deploy/cluster-autoscaler`) shows the
      node group decision matching the expander you configured.
- [ ] A deliberately oversized pod request (bigger than any node group's max shape) produces
      a `NotTriggerScaleUp` event on the pod, not a silent hang with no diagnostic.
- [ ] An idle node below the utilization threshold drains and terminates within
      `scale-down-unneeded-time` + drain time, with no PDB violations in events.
- [ ] Multi-AZ node groups scale together when `--balance-similar-node-groups` is set; test by
      forcing load that only one zone's group would otherwise absorb.

## Checked

Checked 2026-10-24. The documentation checked is the Cluster Autoscaler FAQ and provider READMEs in kubernetes/autoscaler (master, 2026-10-24); the autoscaler binary source now lives in kubernetes-sigs/cluster-autoscaler.
- Scale-up flow, 10s `--scan-interval`, simplified simulation, `--new-pod-scale-up-delay`, expander list, default `least-waste`, chaining from 1.23.0, `price` limited to GCE, GKE and Equinix Metal: FAQ.
- Scale-down conditions and flag defaults (`--scale-down-utilization-threshold` 0.5 as the larger of CPU and memory request ratios against allocatable, `--scale-down-unneeded-time` 10m, `--scale-down-delay-after-add` 10m, `--max-graceful-termination-sec` 600, `--skip-nodes-with-system-pods` true), local-storage definition and the safe-to-evict annotations: FAQ.
- Version matching and the control-plane recommendation: README. `--expendable-pods-priority-cutoff` default -10: FAQ.

Method: documentation only; no commands were run.
