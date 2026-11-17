---
id: computing-software.cloud-infrastructure-engineering.openebs.lvm-snapshots-snapsize-and-controller
name: lvm-snapshots-snapsize-and-controller
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, lvm, snapshot, volumesnapshotclass, snapsize, dm-snapshot, snapshot-controller, thin]
level: advanced
status: docs-checked
description: "Create Local PV LVM snapshots: dm-snapshot requirement, read-only snapshots sized like the origin, snapSize SnapshotClass rules, and using an existing snapshot controller."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-lvm/advanced-operations/lvm-snapshot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Snapshots of LVM volumes need the `dm-snapshot` kernel module. The driver changes LVM's defaults in two ways: snapshots are **read-only** (plain `lvcreate` makes read-write ones), and the snapshot size is set to the size of the origin volume.

**Snapshot controller.** Local PV LVM runs a `snapshot-controller` container by default. A cluster should run only one, so if the cluster already manages one, disable the bundled one through the chart values.

**Default SnapshotClass (no `snapSize`).** For thin volumes the driver creates a thin snapshot; for thick volumes it creates a thick snapshot and reserves a size equal to the volume.

**With `snapSize`.** The VolumeSnapshotClass parameter `snapSize` forces a **thick** snapshot of the given size, for thin and thick origins alike. Accepted values:

- a percentage with a trailing `%`, such as `50%`, between 1 and 100, applied to the origin capacity; values outside the range are rejected and no snapshot is made;
- an absolute quantity such as `10G` or `500Mi`, greater than 0. If it exceeds the origin volume, the driver reduces it to the origin size and still creates the snapshot, so the result can be smaller than configured.

Steps: create a VolumeSnapshotClass (a sample is in the lvm-localpv repository), apply it, then create a VolumeSnapshot for the PVC in the same namespace.

**Restore** works only for thin volumes created from snapshots on OpenEBS v4.4.0 or later; restoring from a snapshot of a thick-provisioned volume is not supported.

To disable the bundled controller the page uses `helm upgrade openebs openebs/openebs --namespace openebs --set lvm-localpv.lvmController.snapshotController.enabled=false`. Before using a snapshot, check that `readyToUse` is true on the VolumeSnapshot and that the `lvmsnapshot` resource in the `openebs` namespace has state `Ready`.

**Limitation:** resize is not supported for volumes that have a snapshot. The page says this is a deliberate driver choice, because LVM does not automatically resize snapshots when the origin is resized.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for lvm-snapshot) in full. Existing claims all match the page. Added the helm flag, readiness checks and the resize limitation from the page.
