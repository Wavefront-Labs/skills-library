---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pdb-for-quorum-systems
name: pdb-for-quorum-systems
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, pdb, quorum-pdb, minavailable, statefulset, etcd]
level: practitioner
status: docs-checked
description: "Size PodDisruptionBudgets for quorum-based systems (etcd, ZooKeeper, Kafka controllers, Elasticsearch masters) so voluntary disruptions never break quorum."
sources: ["https://kubernetes.io/docs/tasks/run-application/configure-pdb/#think-about-how-your-application-reacts-to-disruptions", "https://kubernetes.io/docs/tutorials/stateful-application/zookeeper/#tolerating-node-failure", "https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#maximum-unavailable-pods", "https://etcd.io/docs/latest/metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PDBs for quorum systems

## Rule
Quorum for N members is `floor(N/2) + 1`. The PDB must keep at least quorum available while
also leaving room for one unplanned failure during maintenance:
| Members | Quorum | Tolerates | PDB |
|---|---|---|---|
| 3 | 2 | 1 | `maxUnavailable: 1` |
| 5 | 3 | 2 | `maxUnavailable: 1` (keeps one spare for a surprise failure) |
| 7 | 4 | 3 | `maxUnavailable: 1` or 2 |

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata: {name: zk}
spec:
  maxUnavailable: 1
  selector: {matchLabels: {app: zk}}
  unhealthyPodEvictionPolicy: IfHealthyBudget
```

## Availability is not the same as in-quorum
A pod can be Ready while the member is still catching up (syncing log, rebalancing shards). If
readiness passes too early, the drain evicts the next member while the cluster is effectively
down one. Make readiness reflect "member caught up and in quorum" (for example a ZooKeeper
`ruok` check, as in the Kubernetes ZooKeeper tutorial, or the member health endpoint your system
provides).

## Interaction with other controls
- StatefulSet rolling updates are not limited by the PDB; the StatefulSet's own
  `.spec.updateStrategy.rollingUpdate.maxUnavailable` (beta, on by default, default 1) controls
  them, so keep it at 1 for quorum systems.
- Evictions go through the PDB; spread members across nodes and zones (anti-affinity) so one node
  drain affects one member.
- `unhealthyPodEvictionPolicy: IfHealthyBudget` (default) only evicts a running-but-unhealthy pod
  when the budget is healthy, which protects quorum while members are down; `AlwaysAllow` lets
  drains proceed past crash-looping pods (the Kubernetes docs recommend it generally), which is
  riskier for a quorum system that is already degraded.

## Verify
During a test drain, monitor the system's own quorum signal (for etcd, the `etcd_server_has_leader`
metric) alongside `kubectl get pdb` ALLOWED DISRUPTIONS.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website commit 2026-10-25) and kubernetes/kubernetes master (eviction and kubectl drain source, 2026-10-24). Confirmed: the docs suggest `maxUnavailable: 1` (works with varying scale) or `minAvailable` equal to the quorum size for multi-instance stateful applications such as ZooKeeper and etcd; PDBs do not limit StatefulSet rolling updates; StatefulSet `maxUnavailable` is beta, enabled by default, default 1; `unhealthyPodEvictionPolicy` semantics; the ZooKeeper tutorial uses `ruok`; `etcd_server_has_leader` is an etcd metric; quorum for N members is a majority (floor(N/2)+1). Removed as unconfirmed: the ZooKeeper `zk_quorum_size` metric, the etcd `/health` and Elasticsearch readiness examples, and the node-autoscaler claim.

Method: documentation only; no commands were run.
