---
id: computing-software.cloud-infrastructure-engineering.openebs.mayastor-snapshot-restore-and-restore-policy
name: mayastor-snapshot-restore-and-restore-policy
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [replicated-pv-mayastor, snapshot, restore, datasource, snapshotrestorepolicy, strict, besteffort, replicas]
level: advanced
status: docs-checked
description: "Restore a Mayastor volume from a snapshot via a PVC dataSource, keep the replica count within the replica snapshots, and set snapshotRestorePolicy to strict or bestEffort."
sources:
  - https://openebs.io/docs/user-guides/replicated-storage-user-guide/replicated-pv-mayastor/advanced-operations/snapshot-restore
  - https://openebs.io/docs/user-guides/replicated-storage-user-guide/replicated-pv-mayastor/configuration/rs-storage-class-parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A restore creates a new volume that is an exact copy of the source at snapshot time. Because snapshotting a volume snapshots each of its replicas (a `repl=3` source yields three replica snapshots), there is a hard rule: **the replica count of the new volume must be less than or equal to the available replica snapshot count of the source** at restore time. The page shows how to list a volume's available replicas and its replica snapshot information through the plugin.

Requirements: an existing volume snapshot, and a compatible StorageClass for the restore.

To restore, create a PVC whose `dataSource` names the VolumeSnapshot. The page's skeleton uses a PVC called `restore-pvc`, a class named `mayastor-3-restore` and a snapshot called `mayastor-pvc-snap`; replace them with your own names.

**`snapshotRestorePolicy`** in the StorageClass controls what happens when not every replica pool can host a clone of the snapshot:

- **`strict`** (default): every requested replica must be cloned. If any snapshot replica pool cannot host a clone, for example a source pool is out of space, the restore fails.
- **`bestEffort`**: the restore proceeds if at least one clone succeeds. The volume comes up under-replicated and the remaining replicas are made by a normal rebuild. Until those rebuilds finish, it does not tolerate as many node failures as its `repl` value implies.

The two commands the page gives for checking replica counts are `kubectl mayastor get volume-replica-topology <volume-id>` and `kubectl mayastor get volume-snapshot-topology --volume <volume-id>`. With bestEffort, the trade-off is stated plainly: the restored volume does not tolerate the node failures its `repl` value implies until the outstanding rebuilds complete.

## Checked

Method: 2026-11-08 read the raw markdown of the snapshot-restore and StorageClass parameters pages in full; replica-count rule, PVC dataSource example and strict/bestEffort policy match. Replaced an unsupported strict-versus-bestEffort recommendation with the page's own trade-off note and the plugin commands.
