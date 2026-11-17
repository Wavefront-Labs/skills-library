---
id: computing-software.cloud-infrastructure-engineering.kubernetes.owner-reference-rules-and-terminated-pod-gc
name: owner-reference-rules-and-terminated-pod-gc
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, garbage-collection, cross-namespace-owner, invalid-ownerreference, terminated-pod-gc-threshold, pod-gc, ttlsecondsafterfinished, ownerreferences]
level: advanced
status: docs-checked
description: "Apply ownerReference scoping rules (no cross-namespace owners, cluster-scoped owner limits) and clean up terminated pods and finished Jobs with PodGC thresholds and Job TTLs."
sources: ["https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-garbage-collection", "https://kubernetes.io/docs/concepts/workloads/controllers/ttlafterfinished/", "https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/", "https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#ownerreferencespermissionenforcement"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ownerReference rules and terminated pod GC

## ownerReference scoping rules
- A **namespaced** dependent may only have owners in the **same namespace** or cluster-scoped
  owners.
- A **cluster-scoped** dependent may only have cluster-scoped owners.
- Cross-namespace owner references are disallowed by design: the owner reference is treated as
  absent, and the dependent is subject to deletion once all owners are verified absent. Since
  v1.20 the garbage collector also reports a warning Event with reason `OwnerRefInvalidNamespace`
  (a cluster-scoped dependent that names a namespaced owner kind is never garbage collected).
```bash
kubectl get events -A --field-selector=reason=OwnerRefInvalidNamespace
```
Operators that "own" objects in other namespaces must use labels/annotations + finalizers or
a cluster-scoped owner (e.g. a cluster-scoped CR), not ownerReferences.
- `blockOwnerDeletion: true` makes foreground deletion wait for the dependent. With the
  `OwnerReferencesPermissionEnforcement` admission controller enabled, changing it requires
  `update` permission on the `finalizers` subresource of the referenced owner.

## Terminated pod garbage collection
Failed/Succeeded pods remain (for logs/debugging) until:
- **PodGC** in kube-controller-manager deletes the oldest terminated pods once their count exceeds
  `--terminated-pod-gc-threshold` (default **12500**; a value of 0 or less disables the
  terminated-pod collector). Lower it on batch-heavy clusters that accumulate many terminated pods.
  PodGC also cleans up orphan pods (bound to a node that no longer exists), unscheduled terminating
  pods, and terminating pods on a non-ready node tainted `node.kubernetes.io/out-of-service`.
- **Jobs**: `ttlSecondsAfterFinished` makes a finished (`Complete` or `Failed`) Job eligible for
  cascading deletion (its dependents go with it) N seconds after it finishes (stable since v1.23):
```yaml
spec:
  ttlSecondsAfterFinished: 3600
```
  CronJobs: `successfulJobsHistoryLimit` (default 3) / `failedJobsHistoryLimit`.
- Failed pods stay in the API until a person or controller removes them; delete them
  explicitly if needed, for example `kubectl delete pods --all-namespaces --field-selector=status.phase=Failed`.
Managed clusters may not expose the controller-manager flag; rely on Job TTLs and history limits there.

## Verify
- [ ] The number of pods in phase `Succeeded` or `Failed` (`kubectl get pods -A --field-selector=status.phase=Failed`) stays bounded.
- [ ] No `OwnerRefInvalidNamespace` events.

## Checked
Checked 2026-10-24 against the kubernetes/website Owners and Dependents page (scoping rules, event
reason), Pod lifecycle (PodGC conditions), the kube-controller-manager flag reference
(`--terminated-pod-gc-threshold`, default 12500), TTL-after-finished (stable v1.23), CronJob history
limits (successful default 3), and the OwnerReferencesPermissionEnforcement admission controller.
Method: documentation only; no commands were run.
