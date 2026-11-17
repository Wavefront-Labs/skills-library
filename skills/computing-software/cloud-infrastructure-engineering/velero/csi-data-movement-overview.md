---
id: computing-software.cloud-infrastructure-engineering.velero.csi-data-movement-overview
name: csi-data-movement-overview
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [csi-snapshot-data-movement, velero-fs, velero-block, changed-block-tracking, cbt]
level: advanced
status: docs-checked
description: "Compare Velero block data mover, file system data mover and fs-backup, and know when to choose each."
sources:
  - https://velero.io/docs/main/csi-snapshot-data-movement/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CSI Snapshot Data Movement takes a CSI snapshot, then reads the snapshot data with a data mover and writes it to the backup repository, then deletes the snapshot. Prefer it over File System Backup whenever CSI snapshots exist, because it is consistent (crash-consistent) rather than read from a live volume.

Built-in data movers:
- `velero-fs`: file system mover using Kopia. The default when `--data-mover velero` or no value is given. Use for file storage (EFS, Azure Files, CephFS, NFS) or storage without Changed Block Tracking. Linux and Windows nodes, FileSystem volumeMode only.
- `velero-block`: reads raw blocks and uses the Kubernetes CSI Changed Block Tracking API (`SnapshotMetadataService`) for allocated and changed blocks. Block storage only (EBS, Azure Disk, Ceph RBD, CNS), handles both Block and FileSystem volume modes, Linux nodes only. Best for large database files and for huge numbers of small files.

Use `fs-backup` only when CSI snapshots are unavailable: local, emptyDir, hostPath, non-CSI NFS.

Incremental efficiency: file-based movers must re-read an entire modified file; the block mover reads only changed blocks. Dedup is fixed-size for block, variable-size for the file movers.

Data mover pods must run as root because the built-in movers restore data and metadata. Both movers use the Unified Repository (Kopia) and require the node agent.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/csi-snapshot-data-movement/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
