---
id: computing-software.cloud-infrastructure-engineering.kubernetes.statefulset-start-ordinal-migration
name: statefulset-start-ordinal-migration
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, statefulset, start-ordinal, startordinal, cross-cluster-migration, ordinals]
level: advanced
status: docs-checked
description: "Use StatefulSet spec.ordinals.start to split one StatefulSet's replicas across clusters or namespaces, migrating pods one ordinal at a time without renumbering identities."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#start-ordinal", "https://kubernetes.io/blog/2023/04/28/statefulset-start-ordinal/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# StatefulSet start ordinal for slice migration

`spec.ordinals.start` (stable since 1.31) makes a StatefulSet number its pods from N instead of 0:
replicas 2 with start 3 → `db-3`, `db-4`. That lets two StatefulSets with the same name in
different clusters/namespaces own **disjoint slices** of one logical ordinal range.

## Migrate a 3-member StatefulSet from cluster A to cluster B, one pod at a time
Prereqs: pods can reach each other across clusters (flat network / MCS / mesh), stable DNS
for peers, data replication handled by the app (e.g. Redis Cluster, Cassandra, etcd member
add) or PVs that can be re-attached.

1. **Cluster A**: scale down from the top: `db` replicas 3 → 2,
   freeing ordinal 2. (Pods are removed in reverse ordinal order.)
2. **Cluster B**: create the same StatefulSet with
   ```yaml
   spec:
     replicas: 1
     ordinals: {start: 2}
   ```
   → `db-2` starts in B and joins the application cluster (app-level member add / rebalance).
3. Wait for the app to be healthy (replication caught up).
4. Repeat: A `replicas: 1`; B `replicas: 2, ordinals.start: 1`; then A `replicas: 0`; B
   `replicas: 3, ordinals.start: 0`.
5. Delete the empty StatefulSet in A.

At every step the union of A's `[0, replicasA)` and B's `[start, start+replicasB)` covers each
ordinal exactly once.

## Gotchas
- Pods get ordinals from `start` through `start + replicas - 1`; the StatefulSet treats that range as the desired set, so changing `start` on a running set changes which pods exist.
- With the default `OrderedReady` pod management a pod must be Running and Ready before the next is created; a pod that cannot become Ready until the app reconfigures blocks the next step.
- Headless Service DNS names differ per cluster (`db-2.db.ns.svc.clusterB...`); apps must use
  addresses resolvable from both sides.

## Verify
- [ ] At each step `kubectl get pods -l app=db` in both clusters shows non-overlapping ordinals.
- [ ] App-level membership (using the datastore's own status command) shows the expected members after each move.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the StatefulSet page: `.spec.ordinals.start` assigns ordinals from `start` through `start + replicas - 1` (feature gate StatefulSetStartOrdinal beta 1.27, stable 1.31); scale-down removes the highest ordinal first; default OrderedReady waits for predecessors to be Running and Ready; pod DNS names derive from the governing headless Service.
The Kubernetes blog post on StatefulSet start ordinal describes the same cross-cluster procedure (scale the source down from the top, scale the destination up with the complementary range) and its prerequisites: same StorageClass reachable from both clusters, a flat network between pods, and a gate-enabled destination cluster.
Removed: an uncorroborated description of what happens when `start` is lowered or raised on a running set, a "set reclaim policy to Retain" step, a `redis-cli` command, and the earlier source URL migrate-replicated-application (page does not exist).

Method: documentation only; no commands were run.
