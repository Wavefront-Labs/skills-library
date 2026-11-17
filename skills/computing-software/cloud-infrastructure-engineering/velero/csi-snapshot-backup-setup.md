---
id: computing-software.cloud-infrastructure-engineering.velero.csi-snapshot-backup-setup
name: csi-snapshot-backup-setup
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [csi, enablecsi, volumesnapshot, csi-snapshots, velero-install-features]
level: practitioner
status: docs-checked
description: "Enable Velero CSI snapshot backups with the EnableCSI feature flag, prerequisites, snapshot durability and the how-it-works flow."
sources:
  - https://velero.io/docs/main/csi/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Velero backs up CSI-backed volumes through the Kubernetes CSI snapshot APIs, so any volume provider with a CSI driver works without a Velero-specific plugin. From release 1.14 the CSI plugin is merged into the Velero repository; do not install it separately.

Prerequisites: Kubernetes 1.20 or later; a CSI driver supporting snapshots at the v1 API level; and, when restoring VolumeSnapshots across clusters, the same CSI driver name in the destination cluster.

Enable it on the server:

```bash
velero install --features=EnableCSI --plugins=<object storage plugin> ...
```

To show CSI object status in `velero backup describe`, also run `velero client config set features=EnableCSI`.

How it works: a BackupItemAction acts on PVCs bound to a CSI-backed PV and creates a VolumeSnapshot, in the PVC namespace, using the VolumeSnapshotClass of the same driver. The external-snapshotter creates a VolumeSnapshotContent, whose `status.snapshotHandle` and `status.readyToUse` are set when usable. Velero uploads the VolumeSnapshot and VolumeSnapshotContent objects to object storage; only Kubernetes objects, not snapshot data.

Gotcha: not every cloud CSI driver guarantees snapshot durability. The snapshot may live in the same place as the original volume and be lost with it, so check your provider documentation.

The VolumeSnapshot objects are removed from the cluster after the backup is uploaded.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/csi/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
