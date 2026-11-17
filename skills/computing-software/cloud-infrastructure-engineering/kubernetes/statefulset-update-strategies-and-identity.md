---
id: computing-software.cloud-infrastructure-engineering.kubernetes.statefulset-update-strategies-and-identity
name: statefulset-update-strategies-and-identity
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, statefulset, ondelete, partition, rollingupdate, podmanagementpolicy, ordinal, pod-identity, scale-down, quorum, persistentvolumeclaimretentionpolicy, headless-service, dns-caching, maxunavailable]
level: advanced
status: docs-checked
description: "StatefulSet update strategy mechanics beyond basic partitioning: OnDelete control, ordinal identity reuse across restarts, scale-down ordering guarantees, and quorum-app gotchas."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#update-strategies", "https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#forced-rollback", "https://kubernetes.io/docs/tasks/run-application/scale-stateful-set/", "https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/stateful-set-v1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# StatefulSet update strategies and identity — the ordinal is the whole point

**Goal:** change a StatefulSet's pods without losing the per-pod identity its apps (etcd,
Kafka, Zookeeper, most databases) depend on for quorum and data placement. Storage/PVC
basics and simple `partition` usage are in
`computing-software.cloud-infrastructure-engineering.kubernetes.statefulsets-and-persistent-storage`;
this is the deeper update/identity mechanics.

## 1. OnDelete — full manual control
`updateStrategy.type: OnDelete` means the controller does not automatically update pods when
`.spec.template` changes; you delete a specific pod and the controller recreates it from the new
template at the same ordinal. Use it for quorum-sensitive apps where the operator (human or a
database operator) must drive the order and pace explicitly, rather than trusting
`RollingUpdate`'s highest-ordinal-first order.

## 2. Partitioned RollingUpdate as a canary, not just a pause
`rollingUpdate.partition: N` means only pods with ordinal >= N are updated when the template
changes; lower ordinals are not updated and, even if deleted, are recreated at the previous
version. A partition greater than `replicas` means template updates are not propagated at all.
The docs list staged updates, canaries and phased rollouts as the uses: set `partition` to
`replicas - 1` to update only the highest ordinal, verify it, then decrement. Pods are
individually addressable (`db-2.db-headless.ns.svc`), so you can point a client at the one
updated pod before widening.
- `maxUnavailable` on `rollingUpdate` (beta, feature-state v1.35 in the docs; gate
  `MaxUnavailableStatefulSet`, default value varies by patch release, see the
  `statefulset-rolling-update-maxunavailable` skill) lets more than one pod be unavailable
  during an update; the default is 1, which is why StatefulSet rollouts are slower than
  Deployment rollouts of the same size.
- With the default `OrderedReady` pod management, a new template that never becomes Running and
  Ready stops the rollout and it waits. Reverting the template is not enough because of a known
  issue (kubernetes/kubernetes#67250): you must also delete the pods that were created with the
  bad template.
- StatefulSet has no `progressDeadlineSeconds` field (not in `StatefulSetSpec` in apps/v1), so
  there is no `ProgressDeadlineExceeded` signal; watch `kubectl rollout status sts/<name>` with
  your own timeout.

## 3. Identity is reused, not reassigned
- A replacement pod for ordinal `N` (crash, eviction, node loss) gets the same name and keeps the
  existing PVC; the docs state that the StatefulSet retains the existing PVC and the cluster
  attaches it where the new pod launches. A quorum member rejoining sees its own prior data.
- A pod whose PV is restricted to certain nodes or zones can only schedule where that volume can
  be attached, so a StatefulSet pod can stay `Pending` for reasons a stateless pod never hits.
  Check the StorageClass `volumeBindingMode` and the PV node affinity before blaming the scheduler.
- `podManagementPolicy: Parallel` mainly affects creation and scaling. The docs also say that for
  rolling updates with `maxUnavailable` above 1 the controller terminates and creates up to that
  many pods at once, so pods can become ready out of order.

## 4. Scale-down order and quorum math
- Scale-down removes the highest ordinals first, one at a time under `OrderedReady`, each waiting
  for its successors to be completely shut down. For a quorum system, scale one ordinal at a time
  and let the application's own membership settle between steps; the scale task page says to
  scale only when the application cluster is completely healthy.
- Scaling down does not delete the PVC for the removed ordinal unless
  `persistentVolumeClaimRetentionPolicy.whenScaled: Delete` (default `Retain`). Scaling back up
  reuses the old PVC with whatever data it holds. For most databases that means a fast resync;
  for some it is wrong, so know your app's behaviour before relying on either default.

## Gotchas
- DNS for a given ordinal (`db-1.db-headless...`) resolves to whichever pod currently holds that
  ordinal; clients that cache DNS can keep using a terminated pod's IP across a rolling update.
- `volumeClaimTemplates` (like `selector`, `serviceName` and `podManagementPolicy`) is immutable
  on an existing StatefulSet; changing it needs a delete with `--cascade=orphan` and a recreate
  (see `statefulset-safe-deletion`).
- `kubectl rollout undo` accepts statefulsets (kubectl lists deployment, daemonset and
  statefulset as valid types) and StatefulSets keep revision history (`revisionHistoryLimit`),
  but the broken-template case above still needs the manual pod deletion.

## Verify
- [ ] `kubectl rollout status sts/<name>` completes and the pods' `controller-revision-hash`
      label shows one hash across all pods once settled.
- [ ] A pod deleted mid-cycle is recreated with the identical name and reattaches the same
      PVC (`kubectl get pvc` shows no new claim created).
- [ ] Scaling down one ordinal at a time, the app's own quorum/membership view updates
      cleanly between steps (checked via the app's own status, not just pod count).
- [ ] `persistentVolumeClaimRetentionPolicy` is set deliberately, not left at the default
      when your use case needs `Delete`.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the StatefulSet concept page, scale task, kubectl source and the apps/v1 Go types: OnDelete, RollingUpdate and partition semantics; the forced rollback known issue (kubernetes/kubernetes#67250); maxUnavailable beta, default 1; bursting with maxUnavailable above 1; retained PVC on replacement pods; `persistentVolumeClaimRetentionPolicy` default Retain; scale-down order and the advice to scale only when healthy; StatefulSetSpec has no progressDeadlineSeconds but has revisionHistoryLimit; kubectl rollout undo and status accept statefulset; selector, volumeClaimTemplates, serviceName and podManagementPolicy are immutable (apps validation source).
Removed: the claim that StatefulSets have no `kubectl rollout undo`, the claim that Parallel has no effect on updates, cloud-specific volume names, JVM DNS-caching remarks, and the "observed behaviour on 1.28-1.31 clusters" source.

Method: documentation only; no commands were run.
