---
id: computing-software.cloud-infrastructure-engineering.kubernetes.statefulset-safe-horizontal-scaling
name: statefulset-safe-horizontal-scaling
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, statefulset, ordinal, scale-down, pdb, sharding, quorum, kafka, cassandra, elasticsearch, hpa, persistentvolumeclaim, podmanagementpolicy]
level: advanced
status: docs-checked
description: "Why HPA on a StatefulSet is riskier than on a Deployment: ordinal scale-down order, quorum math, PVC retention, and safe automation patterns."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#deployment-and-scaling-guarantees", "https://kubernetes.io/docs/tasks/run-application/scale-stateful-set/", "https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#persistentvolumeclaim-retention", "https://kubernetes.io/docs/concepts/workloads/pods/disruptions/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Scaling StatefulSets safely

**Goal:** scale a stateful, ordinal-aware workload (Kafka, Cassandra, Elasticsearch, etcd-style
quorum systems, sharded Postgres) up and down without breaking quorum, losing data, or evicting
the wrong replica.

## 1. Why this isn't "HPA but for StatefulSets"
A Deployment's pods are interchangeable; a StatefulSet's are not. Each pod has a stable identity
(`<name>-0`, `<name>-1`, ...), a stable network identity, and often a 1:1 bound PersistentVolumeClaim.
Scaling always happens by ordinal:
- **Scale up**: pods are created sequentially from ordinal 0 to N-1. Before a scaling operation is
  applied to a pod, all its predecessors must be Running and Ready (or available, if
  `minReadySeconds` is set). `podManagementPolicy: Parallel` launches or terminates all pods
  without waiting.
- **Scale down**: pods are terminated in reverse order, N-1 down to 0, and before a pod is
  terminated all its successors must be completely shut down. `replicas: 5` -> `replicas: 3`
  removes `-4` then `-3`; you cannot choose which replica leaves.
- **Unhealthy pods block scale-down**: the scale task page says you cannot scale down while any
  of the set's pods is unhealthy; it only proceeds once they are Running and Ready.
Many clustered systems assign special roles (leader, coordinator, primary shard holder) that are
not ordinal-aware; if `-4` holds the role your app cares about, scale-down removes it anyway and
the app must handle role handoff. Kubernetes has no concept of "don't remove the leader."

## 2. Quorum math before touching replica count
For any consensus-based system, work out the quorum (`floor(N/2) + 1`) for the current and target
size, and do not cross a quorum boundary mid-operation:
- A rapid, uncontrolled scale-down (for example a bad autoscaler target reacting to a metric
  blip) can remove several members before the application rebalances, taking the remaining set
  below quorum during the transition even if the final count is safe.
- The docs say it is better to reason about scaling at the application level and to scale only
  when the stateful application cluster is completely healthy, because some distributed
  databases have problems when nodes join and leave at the same time.
- For ring-style datastores, follow that datastore's own decommission procedure before the pod is
  removed; Kubernetes itself has no pre-scale-down hook. An operator that handles scale events is
  one way to automate it.

## 3. Safe automation patterns
- **Don't point an HPA at a quorum-sensitive StatefulSet** unless the operator managing it
  supports autoscaling. An HPA with `scaleTargetRef` pointing at a StatefulSet works mechanically
  but skips every safety step above. If an HPA manages the set, do not set `.spec.replicas` in
  your manifest (applying a manifest overwrites manual scaling).
- **Partitioned rollout** (`spec.updateStrategy.rollingUpdate.partition: N`) is not a scaling
  feature, but uses the same ordinal mechanism: pods with ordinal >= partition are updated, lower
  ordinals are not and are recreated at the previous version if deleted. Use it to stage a canary
  on the highest ordinals first.
- **PVC retention policy** (`persistentVolumeClaimRetentionPolicy`, stable since 1.32, beta from
  1.27): `whenScaled: Delete` deletes only the PVCs of replicas being scaled down, after their
  pods are deleted; the default `Retain` keeps them, so scaling back up reuses the same volume
  and its data. Replacement pods after a node failure always keep their existing PVC.
- **PodDisruptionBudget** constrains evictions (voluntary disruptions). The disruptions page
  notes that not all voluntary disruptions are constrained by PDBs, for example deleting pods or
  deployments bypasses them; a deliberate replica decrease deletes pods, so do not rely on a PDB
  to stop an over-aggressive autoscaler.

## Gotchas
- `podManagementPolicy: Parallel` speeds up scale-up and scale-down but removes the ordinal wait
  guarantee; it is only safe for workloads with no startup dependency on lower ordinals.
- Pod DNS names (`<pod>.<service>.<ns>.svc.cluster.local`) follow the ordinal, so they stay
  stable across pod recreation; clients that cache the set of all replica names need refreshing
  after a resize.
- Aggregate CPU/memory metrics say nothing about per-shard load: which ordinal is removed is
  fixed by the highest-ordinal rule, not by load.
- A new ordinal often needs an application-level rebalance before it carries traffic; "pod Ready"
  does not mean it serves its share.

## Verify
- [ ] A test scale-down removes the highest ordinal only, and the cluster's own health check
      (quorum status, replication factor) stays green throughout, not just before and after.
- [ ] For ring or quorum stores, the datastore's decommission step happens before Kubernetes
      removes the pod.
- [ ] `persistentVolumeClaimRetentionPolicy` matches intent (Retain for real data, Delete only for
      disposable ordinals), verified by scaling down then back up and checking data presence.
- [ ] An HPA, if used at all, targets only workloads whose operator explicitly supports it.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the StatefulSet concept page, the scale-stateful-set task and the disruptions page: ordered creation and reverse-order termination with the predecessor and successor rules; `Parallel` pod management; scale-down blocked while any pod is unhealthy and the advice to reason at application level; partition semantics; `persistentVolumeClaimRetentionPolicy` (whenScaled and whenDeleted, Retain default; StatefulSetAutoDeletePVC beta 1.27, stable 1.32); replacement pods keep their PVC; do not set `.spec.replicas` when an HPA manages the set; PDBs do not constrain every voluntary disruption (deleting pods bypasses them).
Removed: named operators and `nodetool decommission` (not checked), and speculation about which ordinals hold special roles.

Method: documentation only; no commands were run.
