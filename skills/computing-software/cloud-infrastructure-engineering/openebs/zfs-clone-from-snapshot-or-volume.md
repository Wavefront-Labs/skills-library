---
id: computing-software.cloud-infrastructure-engineering.openebs.zfs-clone-from-snapshot-or-volume
name: zfs-clone-from-snapshot-or-volume
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, zfs, clone, snapshot, datasource, zpool, volumesnapshotdatasource]
level: advanced
status: docs-checked
description: "Create a Local PV ZFS clone from a snapshot or a live volume with a PVC dataSource, and respect the same-size, same-pool, same-node constraints."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-zfs/advanced-operations/zfs-clone
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cloning needs `VolumeSnapshotDataSource` support, which is beta in Kubernetes 1.23; on older clusters enable that feature gate at kubelet and kube-apiserver.

Two ways to clone, both done with a new PVC that sets `dataSource`:

- **From a snapshot.** Name the VolumeSnapshot (the guide's is `zfspv-snap`). The clone has the properties the snapshot had when taken, and its ZFSVolume resource carries a `Snapname` field.
- **From a volume.** Name the source PVC (the guide uses `zfspv-pvc`) as the data source. The clone takes the source's properties at clone time. The driver creates an internal snapshot on the source with the same name as the clone and clones from that, so `Snapname` points at that internal snapshot.

Constraints stated in the guide:

- the clone is created **on the same node** as the original volume;
- the clone PVC must be **the same size** as the original (for snapshot clones the guide says resize is not currently supported);
- the **pool name must be the same**, because cloning across zpools is not supported; if you use a different StorageClass for the clone it must reference the same pool.

Verify by checking that the claim is Bound and by running `zfs list -t all` on the node, where the clone appears. For a volume clone the page's example shows the internal snapshot on the source named after the clone volume, and the clone's ZFSVolume carries an `openebs.io/source-volume` label.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for zfs-clone) in full. Removed the claim that clones are ZFS-only among the Local PV engines, which the page does not state. The constraints and examples otherwise match the page.
