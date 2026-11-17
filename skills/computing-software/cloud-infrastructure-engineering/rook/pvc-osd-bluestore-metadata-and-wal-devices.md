---
id: computing-software.cloud-infrastructure-engineering.rook.pvc-osd-bluestore-metadata-and-wal-devices
name: pvc-osd-bluestore-metadata-and-wal-devices
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [bluestore, block-db, block-wal, metadata-device, wal-device, volumeclaimtemplates]
level: advanced
status: docs-checked
description: "Add a separate metadata or WAL volume to PVC-based OSDs using the data, metadata and wal volumeClaimTemplate names."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/pvc-cluster/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
BlueStore normally uses one primary device as a whole. It can also span extra devices. A DB device stores BlueStore's internal metadata (RocksDB), and metadata spills back to the primary device if the DB device fills. A DB device only helps if it is faster than the primary device.

In a device set you can list several `volumeClaimTemplates`, each representing a device or a metadata device. Rook supports only three template names:
- `data`: the main OSD block device where data is stored.
- `metadata`: the device for the BlueStore database (`block.db` and `block.wal`).
- `wal`: the device for `block.wal`. If set, `metadata` then refers specifically to `block.db`.

Use a faster storage class for the metadata or wal template and a slower one for data. Otherwise a separate metadata device will not improve performance.

Combinations supported by ceph-volume that the page lists include:
- data plus metadata: block.db on the metadata volume
- data plus wal: block.wal on the wal volume, with the block.db staying on the data device and no separate metadata device
- data plus metadata plus wal

Each template sets its own `storageClassName`, a size request and `volumeMode: Block`, and the example comments remind you to change the storage class for your environment (for example local-storage, gp2 or io1).

## Checked

2026-11-03. Confirmed against the PVC Storage Cluster page: the data, metadata and wal template names, the block.db and block.wal roles, the faster-device advice and the supported combinations. Removed: nothing.

Method: documentation only; no commands were run.
