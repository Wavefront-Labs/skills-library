---
id: computing-software.cloud-infrastructure-engineering.kubernetes.poddisruptionbudget-mechanics
name: poddisruptionbudget-mechanics
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, poddisruptionbudget, pdb, minavailable, maxunavailable, voluntary-disruption, disruptionscontroller, allowed-disruptions, unhealthypodevictionpolicy, overlapping-selectors, cluster-autoscaler, karpenter-disruption-budgets, quota-for-disruption, disruptionsallowed]
level: advanced
status: docs-checked
description: "PodDisruptionBudget budget math (minAvailable vs maxUnavailable, percent rounding, expected-pods tracking), overlapping PDBs, and the unhealthy-pod eviction policy edge cases."
sources: ["https://kubernetes.io/docs/tasks/run-application/configure-pdb/", "https://kubernetes.io/docs/concepts/workloads/pods/disruptions/", "https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# PodDisruptionBudget mechanics — doing the arithmetic the disruption controller does

**Goal:** set a PDB that actually protects capacity without silently blocking every drain
forever. How eviction calls a PDB (and differ from plain delete) is in
`computing-software.cloud-infrastructure-engineering.kubernetes.graceful-termination-and-node-drain`;
this is the budget math and multi-PDB edge cases underneath that check.

## 1. minAvailable vs maxUnavailable: pick one
A PDB specifies only one of the two, each as an integer or a percentage of total pods:
- `minAvailable` is how many pods of the selected set must still be available after the
  eviction, even in the absence of the evicted pod.
- `maxUnavailable` is how many may be unavailable after the eviction.
The "total" is the intended number of pods, computed from the `scale` (for example
`.spec.replicas`) of the workload resource that owns the pods, which the control plane finds
through the pods' `metadata.ownerReferences`. `maxUnavailable` can only be used when all the pods
have the same controlling workload; for bare pods or an arbitrary controller only an integer
`minAvailable` works.

Percentages round **up** in both cases (docs): 7 pods with `minAvailable: "50%"` means 4 must be
available; `maxUnavailable` as a percentage rounds up the number of pods that may be disrupted, so
a disruption can exceed your percentage. For example `maxUnavailable: "50%"` on 3 replicas allows
2, and `maxUnavailable: "30%"` on a single replica still allows that one pod (100% unavailable).
Work these out by hand for small replica counts.

## 2. Scaling and the PDB status
Percentages and `maxUnavailable` follow the controller's desired replicas, so they track scaling;
the docs recommend `maxUnavailable` because it responds automatically to changes in replica count.
A fixed `minAvailable: 2` stays 2 whatever the scale. The status fields are `expectedPods`,
`currentHealthy`, `desiredHealthy` and `disruptionsAllowed`; a pod counts as healthy when its
`Ready` condition is `True`.

## 3. Overlapping PDBs on the same pod
The eviction API disallows eviction of any pod covered by more than one PDB, so avoid overlapping
selectors (one reasonable use is while moving pods from one PDB to another). An empty selector
`{}` matches every pod in the namespace. To find the PDBs that apply to a pod, compare the pod's
labels with each PDB's `.spec.selector` (`kubectl get pdb -A -o yaml`).

## 4. unhealthyPodEvictionPolicy (stable since v1.31)
The default, `IfHealthyBudget`, lets a running-but-not-healthy pod be evicted only if the
application is not already disrupted (`currentHealthy` is at least `desiredHealthy`); a
crash-looping pod can therefore block a node drain. `AlwaysAllow` treats running-but-unhealthy
pods as disrupted and evictable regardless of the budget. Pods in `Pending`, `Succeeded` or
`Failed` phase are always considered for eviction. The disruptions page recommends setting
`AlwaysAllow` so misbehaving applications can be evicted during a drain.

## Gotchas
- `maxUnavailable: 0`, `minAvailable: 100%`, or `minAvailable` equal to the replica count requires
  zero voluntary evictions: a node drain that hits such a pod never completes. This is
  permitted by PDB semantics, so it is often an accidental typo.
- PDBs govern voluntary disruption through the Eviction API. Involuntary disruptions cannot be
  prevented by a PDB but they count against the budget. Deployment and StatefulSet rolling
  updates are not limited by PDBs. Deleting pods directly (including
  `kubectl drain --disable-eviction`) bypasses them.
- Cluster managers and hosting providers should use tools that evict through the Eviction API;
  `kubectl drain` retries rejected evictions until the pods are gone or its timeout expires.

## Verify
- [ ] `kubectl get pdb <name> -o yaml` shows `currentHealthy`, `desiredHealthy`,
      `disruptionsAllowed` and `expectedPods` matching hand-computed expectations for the
      current replica count.
- [ ] No pod is matched by more than one PDB unless the overlap is a deliberate transition.
- [ ] A percentage-based PDB's absolute floor (rounded up) is checked by hand at the minimum and
      maximum replica counts.
- [ ] Workloads whose stuck-unhealthy pods must not block drains set
      `unhealthyPodEvictionPolicy: AlwaysAllow`.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website commit 2026-10-25) and kubernetes/kubernetes master (eviction and kubectl drain source, 2026-10-24) (`configure-pdb.md`, `disruptions.md`) and the feature gate page. Confirmed: only one of `minAvailable` and `maxUnavailable`; percentages of total desired pods; rounding up for both fields; the intended count derives from the owning workload's scale via ownerReferences; restrictions for arbitrary controllers; the eviction API disallows pods covered by multiple PDBs; `unhealthyPodEvictionPolicy` values and semantics, with the feature gate stable from v1.31; status fields; zero-eviction PDBs block drains; rolling updates are not limited by PDBs. Wrong and fixed: the skill said `maxUnavailable` percentages round down, that the PDB counts the selector's current matches rather than the controller's scale, and that the controller enforces every overlapping PDB (the eviction API refuses instead). Removed as unconfirmed: the claims about Cluster Autoscaler, Karpenter and the descheduler, and that `kubectl describe pod` does not list PDBs.

Method: documentation only; no commands were run.
