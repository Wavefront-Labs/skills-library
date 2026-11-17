---
id: computing-software.cloud-infrastructure-engineering.openebs.lvm-volume-restore-from-thin-snapshot
name: lvm-volume-restore-from-thin-snapshot
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, lvm, restore, snapshot, thin-provisioning, datasource, pvc, volgroup]
level: advanced
status: docs-checked
description: "Restore a Local PV LVM volume from a snapshot by meeting the thin-only requirements: thin snapshot, thin StorageClass, matching capacity and the same volume group."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-lvm/advanced-operations/lvm-volume-restore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Restoring creates a new volume holding the data of the origin at snapshot time. It is supported **only for thin volumes created from snapshots, using OpenEBS v4.4.0 or later**.

Check these requirements before you create the restore PVC:

- A VolumeSnapshot already exists (created as in the snapshot guide) and a compatible StorageClass is available.
- The snapshot must be **thin**. Describe the LVM snapshot custom resource and check `spec.thinProvision`.
- The StorageClass used for the restore must also set `thinProvision: "yes"`. A restore into a thick StorageClass is rejected even if the snapshot is thin.
- The requested capacity must **match the snapshot logical volume size**. Read it from `status.lvSize` in the LVM snapshot resource.
- The volume group must match the snapshot's (`spec.volGroup`).

To restore, write a PVC whose `dataSource` references the VolumeSnapshot, with a new name and the matching size and thin class. The guide calls the result a clone that contains the data as of the snapshot.

The page says the restored volume is scheduled on the same node as the original volume. To check the result, run `kubectl get pvc -n openebs` (restored PVC Bound) and `kubectl get lvmvolume -n openebs` (new volume Ready); the restored LVMVolume resource lists the snapshot as its `source` and `thinProvision: "yes"`.

The page also advises enabling `thin_pool_autoextend_threshold` and `thin_pool_autoextend_percent` in `lvm.conf` to avoid write failures when the thin pool fills, and keeping free capacity in the volume group, since auto-extend will not work without it.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for lvm-volume-restore) in full. Requirements match the page. Replaced the generic "verify each field" line with the page's own verification commands and added its thin-pool note.
