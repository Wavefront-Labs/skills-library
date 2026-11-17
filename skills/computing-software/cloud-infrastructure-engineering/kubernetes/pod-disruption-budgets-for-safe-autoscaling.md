---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pod-disruption-budgets-for-safe-autoscaling
name: pod-disruption-budgets-for-safe-autoscaling
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, poddisruptionbudget, pdb, eviction, node-drain, voluntary-disruption, cluster-autoscaler, karpenter, minavailable, maxunavailable, disruptions-allowed]
level: advanced
status: docs-checked
description: "The PDB math that blocks or allows node drain/scale-down, where it does and doesn't apply, and the deadlocks it causes when misconfigured."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/disruptions/", "https://kubernetes.io/docs/tasks/run-application/configure-pdb/", "https://kubernetes.io/docs/concepts/scheduling-eviction/api-eviction/", "https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.15/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PodDisruptionBudgets for safe autoscaling

**Goal:** know exactly when a PDB blocks an autoscaler's node removal, when it doesn't, and how
to avoid the classic deadlock where autoscaling and availability requirements fight to a stalemate.

## 1. Voluntary vs involuntary — the one distinction that explains everything
A PDB **only** governs *voluntary* disruptions: node drain (`kubectl drain`), Cluster Autoscaler/
Karpenter removing a node for scale-down or consolidation, a cluster upgrade's node replacement.
It does **not** govern involuntary disruptions: a node dying, an OOM kill, a hardware failure, a
spot/preemptible reclaim. This is why a PDB cannot make your workload "safe" from a spot
interruption — that's an involuntary event; the PDB simply has no say.
Within voluntary disruptions, the mechanism is the **Eviction API**: a controller requesting to
evict a pod must succeed against `disruptionsAllowed` on the pod's matching PDB, or the eviction
is rejected with `429 Too Many Requests` (the Eviction API returns `500` instead if a
misconfiguration, such as multiple PDBs covering one pod, prevents it) — not silently ignored,
actually rejected, and tools such as `kubectl drain` retry.

## 2. The math
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata: {name: api}
spec:
  minAvailable: 2        # or maxUnavailable: 1 — pick one, not both
  selector: {matchLabels: {app: api}}
```
- `minAvailable: 2` with 3 replicas → `disruptionsAllowed: 1`. Check it live:
  `kubectl get pdb api -o jsonpath='{.status.disruptionsAllowed}'`.
- `minAvailable`/`maxUnavailable` can be a percentage (`"50%"`). Kubernetes rounds up in both
  cases: with 7 pods, `minAvailable: "50%"` means 4 must be available, and a `maxUnavailable`
  percentage rounds up the number of pods that may be disrupted, so a disruption can exceed
  the percentage you wrote. Only one of `minAvailable` and `maxUnavailable` may be set.
- `status.currentHealthy`, `.desiredHealthy`, `.disruptionsAllowed` on the PDB object show the
  live computed state — read these directly when debugging, don't just re-derive from replica
  count, because the PDB controller also accounts for pods not currently healthy.

## 3. Where this bites autoscaling specifically
- **Cluster Autoscaler**: scale-down's checklist (see the CA internals skill) explicitly includes
  "would this violate a PDB" — a node hosting a pod whose PDB is already at `disruptionsAllowed: 0`
  is permanently un-drainable by CA until something changes that count. CA does not force past this.
- **Karpenter consolidation**: its termination controller drains through the Eviction API, which
  respects PDBs, and Karpenter emits an `Unconsolidatable` event such as "pdb default/inflate-pdb
  prevents pod evictions". Its docs also warn that misconfigured PDBs and pods annotated
  `karpenter.sh/do-not-disrupt` may block draining indefinitely.
- **The classic deadlock**: `minReplicas: 1` on a Deployment plus `minAvailable: 1` (or
  `maxUnavailable: 0`) on its PDB means that single pod's node can **never** be drained
  voluntarily — `disruptionsAllowed` is permanently 0 (the Kubernetes docs note that zero
  voluntary evictions means a drain of that node never completes). This blocks node upgrades, CA/Karpenter consolidation, and any drain
  indefinitely. The fix is always at the replica-count/PDB design level (raise `minReplicas` so a
  disruption still leaves `minAvailable` satisfied), never by overriding the PDB mechanism.
- Autoscaled (HPA-driven) workloads make this worse under *low* load: if HPA scales a Deployment
  down to its `minReplicas` floor right as a node drain is attempted, a PDB sized for the
  *typical* replica count can accidentally become unsatisfiable at the floor — size PDBs relative
  to `minReplicas`, not to steady-state replica count.

## 4. What has no PDB by default
Pods not covered by any PDB you wrote are **not protected at all**. A PDB can select bare pods or
pods managed by an operator, but then only an integer `minAvailable` is allowed (no
`maxUnavailable`, no percentage), because Kubernetes cannot derive the total pod count. Separately
from PDBs, Cluster Autoscaler does not remove nodes that run pods without a controller unless
they are annotated `cluster-autoscaler.kubernetes.io/safe-to-evict: "true"`.

## Gotchas
- A PDB whose `selector` matches no pods protects nothing, so a typo in `matchLabels` fails open;
  an empty selector (`{}`) matches every pod in the namespace.
- The Eviction API refuses to evict a pod covered by multiple PDBs, so avoid overlapping selectors
  (the Kubernetes docs allow overlap only while pods move from one PDB to another).
- Directly deleting pods or Deployments does not go through the Eviction API; the Kubernetes docs
  tell cluster managers to use tools that call the Eviction API so that PDBs are respected.
- Pods that are unavailable during a rolling update count against the budget, but Deployments and
  StatefulSets are not limited by PDBs during their own rolling updates.

## Verify
- [ ] `kubectl get pdb -A` shows `disruptionsAllowed` > 0 for every workload that needs to survive
      routine node drains/upgrades, at both steady-state and `minReplicas` floor.
- [ ] A test `kubectl drain` (or forced Karpenter consolidation) on a node hosting a
      tightly-PDB'd pod is correctly blocked (429/retry), not force-evicted.
- [ ] No PDB's `selector` matches zero pods (check `.status.currentHealthy` isn't silently 0 for a
      workload you believe is protected).
- [ ] PDB `minAvailable`/`maxUnavailable` values are re-validated whenever a workload's
      `minReplicas` changes, not left at the original steady-state assumption.

## Checked

Checked 2026-10-24 against Kubernetes v1.37 documentation (kubernetes/website main, the latest published release on 2026-10-24) (Disruptions, Specifying a Disruption Budget, API-initiated eviction), the Cluster Autoscaler FAQ and the Karpenter v1.15 disruption docs source.
- PDBs cover voluntary disruptions only, involuntary ones count against the budget; Eviction API `429` and `500` responses; only one of `minAvailable` and `maxUnavailable`; percentage rounding (both round up); zero voluntary evictions blocks a drain; bare pod and operator restrictions (integer `minAvailable` only); empty selector matches all pods; multiple PDBs block eviction; rolling-update note; `disruptionsAllowed`, `currentHealthy`, `desiredHealthy` status fields: the Kubernetes pages above.
- Cluster Autoscaler treatment of bare pods and PDB-blocked pods: FAQ ("What types of pods can prevent CA from removing a node?").
- Karpenter `Unconsolidatable` event text, PDB-respecting termination and `karpenter.sh/do-not-disrupt`: Karpenter disruption docs.

Method: documentation only; no commands were run.
