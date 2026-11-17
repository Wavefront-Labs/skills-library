---
id: computing-software.cloud-infrastructure-engineering.openebs.rawfile-snapshots-consistency-and-restore
name: rawfile-snapshots-consistency-and-restore
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, rawfile, snapshot, volumesnapshotclass, freezefs, restore, enable-distributed-snapshotting, cow]
level: advanced
status: docs-checked
description: "Take Local PV Rawfile snapshots: requirements, the required snapshot-controller flag when using your own, CoW versus freezeFs consistency, restoring to a new PVC on the same node."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-rawfile/advanced-operations/rawfile-snapshot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rawfile uses the standard Kubernetes `VolumeSnapshot` API. Snapshots are node-local and run as persistent background tasks that survive driver restarts and retry.

Requirements: snapshots enabled in the chart (default `capabilities.snapshots.enabled=true`), the VolumeSnapshot CRDs, a `VolumeSnapshotClass` for the rawfile driver, and a running snapshot controller. The driver deploys one by default.

**Using your own snapshot controller.** Only one should run in a cluster, so disable the bundled one in the chart values if you manage another. The remaining controller **must be started with `--enable-distributed-snapshotting=true`**. Without it, Rawfile snapshots are never provisioned and no error is reported at install time.

`deletionPolicy: Delete` removes snapshot data when the VolumeSnapshot object is deleted; `Retain` preserves it. A snapshot is complete when `ReadyToUse` is true.

**Consistency for active volumes.**

- Preferred: a pool on a reflink filesystem (btrfs or XFS) gives space-efficient, almost instant snapshots with no freeze.
- Otherwise set `freezeFs: "true"` in the StorageClass. The filesystem is frozen while the whole volume is copied to a new file, so all writes block for the entire duration.

**Restore** by creating a new PVC with the snapshot as `dataSource`. It is provisioned on the same node that holds the snapshot data. The page also describes a rollback pattern that starts by scaling the workload down to release the PVC, then creates the restored PVC, points the Deployment at it and scales back up.

**Chart value to disable the bundled controller:** `node.snapshotController.enabled: false`, applied with `helm upgrade rawfile-localpv rawfile-localpv/rawfile-localpv -n openebs -f values.yaml`.

**Capacity.** On reflink-capable pools a snapshot consumes only blocks changed after the snapshot point. On non-CoW pools each snapshot is a full copy and uses as much space as the original; `Insufficient disk space` means checking pool free capacity (`rawfile_pool_remaining_capacity_bytes`).

**Cleanup.** Delete all VolumeSnapshots before deleting the PVC or uninstalling the driver, to avoid leaked data on nodes.

**Troubleshooting from the page.** Snapshot stuck in `Pending`: check the node plugin logs (`kubectl -n openebs logs ds/<release>-node -c csi-driver`). `Snapshotting capabilities are disabled`: set `capabilities.snapshots.enabled=true` and upgrade. No VolumeSnapshotClass found: create one with `driver: rawfile.csi.openebs.io`.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for rawfile-snapshot) in full. Existing claims match the page; added the chart value, capacity, cleanup and troubleshooting items it states.
