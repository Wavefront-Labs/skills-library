---
id: computing-software.cloud-infrastructure-engineering.openebs.zfs-snapshot-volumesnapshotclass
name: zfs-snapshot-volumesnapshotclass
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, zfs, snapshot, volumesnapshotclass, deletionpolicy, zfssnapshot, snapshot-controller]
level: practitioner
status: docs-checked
description: "Take a Local PV ZFS snapshot with a VolumeSnapshotClass (deletionPolicy Retain or Delete), confirm readyToUse and the ZFSSnapshot status, and handle a second snapshot controller."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-zfs/advanced-operations/zfs-snapshot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A ZFS volume snapshot can later seed a clone or a backup. First create a **VolumeSnapshotClass**, much like a StorageClass, where you set `deletionPolicy` to `Retain` or `Delete`. Then create a VolumeSnapshot that names the class and the PVC to capture, and apply it.

Rules from the guide:

- Create the snapshot **in the same namespace as the PVC**.
- Wait until `readyToUse` is true before using the snapshot for anything.
- Local PV ZFS runs a `snapshot-controller` container by default. A cluster should run only one such controller, so if a cluster-level one already exists, disable the bundled one in the chart values.

Verification has two layers. The OpenEBS resource for the snapshot, a **ZFSSnapshot**, should show status `Ready`. On the node, go to the node and confirm the snapshot exists in the pool.

## Checked

2026-11-04. Confirmed against the Local PV ZFS Snapshot page: VolumeSnapshotClass with `deletionPolicy` Retain or Delete, same-namespace and `readyToUse` notes, the bundled snapshot-controller, the ZFSSnapshot `Ready` state, and the on-node check. Removed the Velero backup and restore paragraph and its version numbers, which are not on this page.

Method: documentation only; no commands were run.
