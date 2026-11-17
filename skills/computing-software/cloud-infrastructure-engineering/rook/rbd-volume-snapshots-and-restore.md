---
id: computing-software.cloud-infrastructure-engineering.rook.rbd-volume-snapshots-and-restore
name: rbd-volume-snapshots-and-restore
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [volumesnapshot, volumesnapshotclass, snapshotpolicy, csi-snapshotter, restore-pvc, encrypted-pvc]
level: practitioner
status: docs-checked
description: "Take RBD volume snapshots with the snapshot controller, snapshotPolicy and a VolumeSnapshotClass, then restore to a new PVC within encryption limits."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Ceph-CSI/ceph-csi-snapshot/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisite: install the Kubernetes snapshot controller and the snapshot v1 CRDs.

With the ceph-csi-operator (ceph-csi-drivers Helm chart), set `snapshotPolicy` on each driver that needs snapshots. The default is `none`, which disables the `csi-snapshotter` sidecar. Valid values are `none`, `volumeSnapshot` and `volumeGroupSnapshot` (use the last one for Volume Group Snapshots instead).

A `VolumeSnapshotClass` is needed:
- `csi.storage.k8s.io/snapshotter-secret-name` must reference the secret created for the rbdplugin, with the pool name matching your Ceph pool.
- `clusterID` must match the namespace Rook runs in, default `rook-ceph`. The operator maintains a ConfigMap keyed by it.

Create a `VolumeSnapshot` whose `volumeSnapshotClassName` is that class and `persistentVolumeClaimName` is an existing RBD PVC. The snapshot is ready to restore when `READYTOUSE` is true in `kubectl get volumesnapshot`.

Restore by creating a new PVC with `dataSource` of kind `VolumeSnapshot` naming the snapshot; `storageClassName` can be any RBD storage class. Rules:
- The provisioner must be the same for the parent PVC and the restored PVC.
- Encrypted to encrypted and non-encrypted to non-encrypted are possible.
- Encrypted to non-encrypted, or the reverse, is not possible.

## Checked

2026-11-03. Confirmed against the Ceph-CSI snapshot page: snapshotPolicy values and default none, the VolumeSnapshotClass requirements, the READYTOUSE check and the restore rules including encrypted to non-encrypted being impossible. Removed: nothing.

Method: documentation only; no commands were run.
