---
id: computing-software.cloud-infrastructure-engineering.kubernetes.statefulset-troubleshooting-stuck-pods
name: statefulset-troubleshooting-stuck-pods
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, statefulset, statefulset-troubleshooting, statefulset-stuck-pod, pvc-pending, orderedready, force-delete, statefulset-forced-rollback]
level: practitioner
status: docs-checked
description: "Unstick StatefulSets: ordinal blocked by an unready predecessor, PVC Pending or zone-locked volumes, stuck rolling update, and when force-deleting a pod is (un)safe."
sources: ["https://kubernetes.io/docs/tasks/run-application/force-delete-stateful-set-pod/", "https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#forced-rollback", "https://kubernetes.io/docs/tasks/debug/debug-application/debug-statefulset/", "https://kubernetes.io/docs/concepts/cluster-administration/node-shutdown/#non-graceful-node-shutdown"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# StatefulSet troubleshooting: stuck pods and PVC binding

## Triage
```bash
kubectl get sts db -o wide; kubectl describe sts db | tail -20
kubectl get pods -l app=db -o wide
kubectl get pvc -l app=db                      # volumeClaimTemplate PVCs: data-db-0, data-db-1...
kubectl get events --sort-by=.lastTimestamp | grep -E 'db-|data-db'
```

## Case 1: db-2 never created
`podManagementPolicy: OrderedReady` (default) creates `db-N` only after `db-(N-1)` is Running
and Ready. Fix the lowest unready pod first. For apps that don't need ordering use
`podManagementPolicy: Parallel`, which launches or terminates all pods without waiting.

## Case 2: Pod Pending, PVC Pending
- PVC stays Pending with no matching PV and no StorageClass set → no default
  StorageClass / wrong `storageClassName` in the template.
- A `WaitForFirstConsumer` volume binding mode keeps the PVC Pending until the pod is scheduled.
- Scheduler event `node(s) didn't match PersistentVolume's node affinity` → the PV exists in
  zone a, the pod can only schedule in b (node pool lost zone a, or taints). Restore capacity
  in that zone; do not delete the PVC unless data is expendable.

## Case 3: rolling update stuck
A broken revision with `OrderedReady` stops at the first pod that never becomes Ready, and
**reverting the template does not replace that pod** (known behaviour: "forced rollback").
After fixing the template, delete the stuck pod manually so it is recreated at the good
revision:
```bash
kubectl rollout undo sts/db      # or apply the fixed template
kubectl delete pod db-2
kubectl rollout status sts/db
```
`updateStrategy.rollingUpdate.partition` set high also "stalls" updates by design — check it.

## Case 4: pod stuck Terminating on a dead node
The StatefulSet will **not** create a replacement `db-1` until the old one is confirmed gone
(at-most-one semantics). Options in order of safety:
1. Recover/power off the node and delete the Node object (`kubectl delete node`), which lets
   the pod be garbage-collected.
2. Apply `node.kubernetes.io/out-of-service=nodeshutdown:NoExecute` taint (non-graceful node
   shutdown, GA in v1.28) after confirming the node is down — volumes detach and pods are removed;
   remove the taint yourself afterwards.
3. `kubectl delete pod db-1 --grace-period=0 --force` — only if you are **certain** the old
   process is dead; otherwise two writers on one volume/identity = split brain.

## Verify
- [ ] `kubectl get sts db` READY = replicas; `currentRevision == updateRevision`.
- [ ] All `data-db-*` PVCs Bound in the zones of their pods.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- `OrderedReady` default and `Parallel` pod management, partitioned rolling updates, forced rollback behaviour:
  StatefulSet concept page.
- At-most-one semantics, pod stuck on an unreachable node until the Node object is deleted or the pod is force deleted:
  force-delete StatefulSet pod task page.
- Out-of-service taint and its manual removal: node-shutdown page; stable in v1.28 per the feature-gate page.
- Scheduler message `node(s) didn't match PersistentVolume's node affinity` and `node(s) didn't find available persistent
  volumes to bind`: scheduler `volumebinding/binder.go` v1.37.1.
- Removed: the immutability claims for `podManagementPolicy` and `volumeClaimTemplates`, and the quoted PVC events, which
  the checked sources do not state.

Method: documentation only; no commands were run.
