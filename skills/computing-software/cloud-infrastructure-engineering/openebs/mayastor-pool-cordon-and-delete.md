---
id: computing-software.cloud-infrastructure-engineering.openebs.mayastor-pool-cordon-and-delete
name: mayastor-pool-cordon-and-delete
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [replicated-pv-mayastor, pool, cordon, delete, purge, diskpool, maintenance, decommission]
level: advanced
status: docs-checked
description: "Cordon a Mayastor pool with replica, snapshot, restore and import flags, then delete pools: online empty pools versus the irreversible offline purge for unrecoverable pools."
sources:
  - https://openebs.io/docs/user-guides/replicated-storage-user-guide/replicated-pv-mayastor/advanced-operations/cordon-pools
  - https://openebs.io/docs/user-guides/replicated-storage-user-guide/replicated-pv-mayastor/advanced-operations/delete-pools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Pool cordon** temporarily stops new replicas, snapshots, restores or imports from being scheduled on a pool. Use it for planned maintenance, hardware investigation or controlled decommissioning. Existing data stays available until you migrate or remove it. It needs a Mayastor version that supports pool cordoning and the `kubectl-mayastor` or `kubectl-openebs` plugin with admin access.

You choose what to block with flags; **a flag's presence sets that resource type to cordoned**, and omitted types stay uncordoned: `--replicas`, `--snapshots`, `--restores`, `--imports`. Uncordon uses the same flags to re-enable the selected types selectively.

**Deleting pools** has two routes:

- **Online delete**: only for a reachable pool that is **empty**, with no volume replicas or snapshots. Deletion is blocked while dependent resources exist. Use the plugin or delete the DiskPool custom resource.
- **Offline delete (purge)**: removes the pool from the control plane **without deleting any data left on the device**. It is for failure cases where the pool is irrecoverably lost: the host is permanently gone and replaced, the device is inaccessible, or hardware or infrastructure failure makes recovery impossible. It is **not part of the normal lifecycle** and is irreversible; if the purged pool held the last healthy replicas, access to volume or snapshot data may be permanently lost.

Before a purge, cordon the pool so nothing new is scheduled on it. A sound order is to cordon, migrate or scale away replicas, confirm the pool is empty, then delete; purge only after you are certain recovery is impossible.

## Checked

2026-11-04. Confirmed against the Cordon Pools and Delete Pools pages: what cordon blocks and the four flags, flag-presence semantics, uncordon, online delete limited to empty pools, purge scenarios and irreversibility, and cordoning before purge. Nothing removed.

Method: documentation only; no commands were run.
