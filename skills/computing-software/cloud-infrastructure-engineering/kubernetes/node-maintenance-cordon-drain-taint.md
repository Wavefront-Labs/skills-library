---
id: computing-software.cloud-infrastructure-engineering.kubernetes.node-maintenance-cordon-drain-taint
name: node-maintenance-cordon-drain-taint
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cordon, drain, taint, toleration, node-maintenance, poddisruptionbudget, pdb, eviction, graceful-shutdown, daemonset, node-lifecycle, drain-flags, delete-emptydir-data, ignore-daemonsets, taint-based-eviction, uncordon, kubectl-taint]
level: practitioner
status: docs-checked
description: "Take a node out of service for maintenance without an outage: cordon vs drain, PDB-aware eviction, taints/tolerations, and what still runs during a drain."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/", "https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/", "https://kubernetes.io/docs/concepts/scheduling-eviction/api-eviction/"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Node maintenance: cordon, drain, taint

**Goal:** remove a node from the scheduling pool and evacuate its workloads for
maintenance (kernel patch, instance replacement, decommission) without violating a
PodDisruptionBudget or dropping traffic. This is the routine counterpart to
`computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-cluster-upgrade-sequencing`,
which drains as one step in a bigger sequence.

## 1. Cordon vs drain — they do different things
- `kubectl cordon <node>` sets `spec.unschedulable: true`. **Nothing currently running
  is touched** — it only stops *new* pods from scheduling there. Use this alone when you
  want to stop the bleeding (a node showing early hardware warning signs) without yet
  forcing a workload migration.
- `kubectl drain <node>` cordons **and** evicts existing pods, respecting
  PodDisruptionBudgets:
  ```bash
  kubectl drain <node> --ignore-daemonsets --delete-emptydir-data --timeout=300s
  ```
  - `--ignore-daemonsets`: DaemonSet pods are not evicted (they're meant to run on every
    node) — without this flag, drain refuses to proceed past them.
  - `--delete-emptydir-data`: required if any pod uses an `emptyDir` volume, since that
    data is node-local and genuinely lost on eviction — drain refuses without this flag
    as an explicit acknowledgment, not a default-on data-loss.
  - Without `--force`, drain refuses to evict pods not managed by a
    ReplicaSet/Job/DaemonSet/StatefulSet (bare pods) — there's nothing to reschedule them.

## 2. Eviction respects PodDisruptionBudgets — and can hang because of it
- Drain calls the **Eviction API**, not a hard delete; the API server checks the
  relevant PDB before allowing each eviction. If a PDB's `minAvailable`/`maxUnavailable`
  would be violated, the eviction is refused and drain **retries** rather than failing
  outright — this is why a drain can hang indefinitely on a workload with
  `replicas: 2` and `minAvailable: 2`: there's no way to evict either pod without
  breaking the budget, and drain will wait forever unless you intervene.
- Diagnose a stuck drain: `kubectl get pdb -n <ns>` for `ALLOWED DISRUPTIONS` of 0 (drain prints
  "error when evicting ... (will retry after ...)" and `--timeout` defaults to infinite). Fix by
  scaling the Deployment up temporarily, relaxing the PDB, or accepting the outage and
  force-deleting — don't just raise `--timeout` and hope.
- A `minAvailable: 100%` or equivalent PDB is a common anti-pattern that makes every
  drain on that workload a manual intervention; it should mean "I've accepted I can
  never drain a node this pod is on without a manual step," which is rarely intended.

## 3. What keeps running during a drain
- DaemonSet pods (with `--ignore-daemonsets`), and mirror pods of static pods (drain filters
  mirror pods out; the kubelet owns static pods).
- Pods terminate via normal `terminationGracePeriodSeconds` + `preStop` hook, same as
  any delete — a drain is not instant; long grace periods extend drain time
  proportionally. Check `kubectl get pods -o wide --field-selector spec.nodeName=<node>`
  mid-drain to see what's still finishing.

## 4. Taints for longer-term exclusion
Beyond a temporary drain, a **taint** keeps a node excluded from scheduling until
explicitly removed, independent of cordon state:
```bash
kubectl taint nodes <node> maintenance=true:NoSchedule
# remove: kubectl taint nodes <node> maintenance=true:NoSchedule-
```
- `NoSchedule`: blocks new pods that do not tolerate it and doesn't touch running ones; it is visible
  in `kubectl describe node` and is separate from cordon (which sets `spec.unschedulable`).
- `NoExecute`: pods that do not tolerate the taint are evicted immediately — a much stronger
  action than drain's PDB-respecting eviction; use deliberately, not as a routine maintenance tool.
  Pods that tolerate it without `tolerationSeconds` stay bound forever.
- Built-in taints (`node.kubernetes.io/unreachable`, `node.kubernetes.io/not-ready`) are
  applied automatically by the node controller; pods get a default toleration with
  `tolerationSeconds=300` for them, which is what moves pods off a node that silently died,
  separate from any manual drain.

## 5. Bringing the node back
```bash
kubectl uncordon <node>
```
Does not re-schedule evicted pods back onto this specific node — the scheduler decides
fresh based on current pressure. If the goal was "move everything back after
maintenance," that's a scheduling preference (affinity/topology spread), not a `drain`/
`uncordon` guarantee.

## Gotchas
- Draining the last node in a nodegroup with no autoscaler headroom can leave pods
  `Pending` cluster-wide with nowhere to go — check capacity before draining, especially
  on a small cluster.
- Drain first and delete the Node object (or power down the machine) only after it is empty; the docs
  call it safe to remove the machine once `kubectl drain` returns successfully.
- Pods that tolerate `node.kubernetes.io/unschedulable`, and pods with `spec.nodeName` set directly, can
  still land on or stay on a drained node.
- A `NoExecute` taint evicts pods that do not tolerate it immediately.

## Verify
- [ ] `kubectl drain` completes without hanging, or the PDB blocking it is confirmed
      intentional before overriding it.
- [ ] `--ignore-daemonsets` and `--delete-emptydir-data` are deliberate choices per
      drain, not blind defaults in automation that could silently drop data.
- [ ] Post-drain, `kubectl get pods -o wide --field-selector spec.nodeName=<node>`
      shows only DaemonSet/static pods remaining.
- [ ] A maintenance taint is removed (`kubectl taint ... -`) once work is done — stale
      taints silently shrink the schedulable fleet.

## Checked
2026-10-23, against the Kubernetes website safely-drain-a-node task (cordon/uncordon, DaemonSet and nodeName caveats, unschedulable taint toleration), the taints and tolerations page (NoSchedule/NoExecute semantics, default tolerationSeconds=300 for not-ready and unreachable), and the kubectl drain source (flag help, DaemonSet and unmanaged-pod filters, mirror pod filter, eviction retry message). The nodeName, `kubectl delete node` and kubelet-restart remarks were corrected or removed.
Method: documentation only; no commands were run.
