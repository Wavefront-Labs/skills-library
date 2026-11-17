---
id: computing-software.cloud-infrastructure-engineering.openebs.mayastor-replica-placement-rules-and-recovery
name: mayastor-replica-placement-rules-and-recovery
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [replicated-pv-mayastor, replica, nexus, faulted, degraded, placement, reconciliation, scale, rebuild]
level: advanced
status: docs-checked
description: "Predict Mayastor replica behaviour from the three placement rules: one replica per node, faulted replicas retired first, and how failed replicas are replaced and repl scaled."
sources:
  - https://openebs.io/docs/user-guides/replicated-storage-user-guide/replicated-pv-mayastor/advanced-operations/replica-operations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With `repl` above one, the control plane keeps that many identical replicas of a volume using a Kubernetes-like reconciliation loop. Reads are distributed round-robin across replicas; writes must go to all of them. If I/O to a replica fails, because of a network blip, node reboot or disk failure, the child enters `Faulted` and the volume becomes `Degraded`.

Recovery: the control plane **retires** the faulted replica, which then becomes eligible for garbage collection if its pool is still viable. It then restores the replica count by creating a new replica under the placement rules, and the nexus **rebuilds** it with a full copy from a healthy `Online` replica while the volume keeps serving I/O. After a graceful io-engine restart, the nexus recomposes itself by re-attaching its previous healthy replicas and tries to reuse and rebuild previously faulted ones that are Online again.

**Scaling.** Change a provisioned volume's replica count with the kubectl plugin `scale` subcommand; `num_replicas` can go up or down **by one**, and the control plane creates or destroys replicas under the same rules.

**The three rules:**

1. A volume can be provisioned only if its StorageClass replica count and capacity can be satisfied at creation.
2. Every replica must sit on a **different io-engine node**. So two replicas of the same volume can never live in different pools on the same node.
3. `Faulted` children are retired in preference to `Online` ones.

The page's scenarios show a failed disk or a detached SAN LUN leading to a replica being replaced on another pool or node with enough capacity (rule 2 means the replacement cannot share a node with surviving replicas). If no eligible node and pool exist, the volume stays degraded.

## Checked

Method: 2026-11-08 read the raw markdown of the cited replica operations page in full; the reconciliation behaviour, retire and rebuild sequence, scaling by one and the three placement rules match. The degraded-when-no-node claim is from Scenario Four. Unchanged.
