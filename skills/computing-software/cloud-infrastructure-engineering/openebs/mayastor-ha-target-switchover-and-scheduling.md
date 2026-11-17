---
id: computing-software.cloud-infrastructure-engineering.openebs.mayastor-ha-target-switchover-and-scheduling
name: mayastor-ha-target-switchover-and-scheduling
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [replicated-pv-mayastor, high-availability, nexus, switchover, multipath, nvme-core, scheduling, volume-target]
level: advanced
status: docs-checked
description: "Mayastor HA target switch-over (HA node agent plus cluster agent), the nvme_core.multipath=Y requirement, the RHEL 10 limit, and where targets and replicas are scheduled."
sources:
  - https://openebs.io/docs/user-guides/replicated-storage-user-guide/replicated-pv-mayastor/advanced-operations/ha
  - https://openebs.io/docs/user-guides/replicated-storage-user-guide/replicated-pv-mayastor/advanced-operations/volume-scheduling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**HA switch-over.** If a volume target fails, Mayastor detects it and creates a new nexus so I/O continues. Two components do this: the **HA node agent** in each CSI node pod watches for I/O path failures between applications and their targets and tells the **cluster agent**, which runs alongside agent-core and creates a new target on a different live node. The node agent then sets up a new path from the application. The volume must have more than one replica for a new target to be created.

Requirements and limits:

- The kernel parameter **`nvme_core.multipath=Y` is mandatory**; without it, target failover is not possible.
- HA is **not supported on RHEL 10 and derivatives**, which removed that parameter, so OpenEBS cannot tell whether multipath is enabled.
- HA is on by default. It can be disabled with `--set=agents.ha.enabled=false` on `helm install`, but the docs strongly recommend leaving it on.
- Applications pinned to nodes labelled `openebs.io/engine=mayastor` get the nexus preferably on the same node, unless that node's io-engine pod is unhealthy.

**Scheduling.** Volume targets may be placed on any io-engine node; replicas only on io-engine nodes that have Mayastor disk pools. When a PV is created, only replicas are created and the control plane picks their pools. The target is created when a pod is assigned the PVC:

- single-replica volume: the target is always on the replica's node;
- multi-replica volume with the pod on an online io-engine node: target on the pod's node;
- multi-replica volume with the pod on a non-io-engine node: target placed optimally on any io-engine node.

The multi-replica initial placement is not fixed: if HA triggers, the target may move.

## Checked

Method: 2026-11-08 read the raw markdown of the HA and volume-scheduling pages in full; switch-over components, multipath requirement, RHEL 10 limit, disable flag and placement rules match. Unchanged.
