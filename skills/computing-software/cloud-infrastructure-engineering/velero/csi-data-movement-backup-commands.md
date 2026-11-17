---
id: computing-software.cloud-infrastructure-engineering.velero.csi-data-movement-backup-commands
name: csi-data-movement-backup-commands
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [snapshot-move-data, data-mover, backup-type, dataupload, incremental-backup]
level: practitioner
status: docs-checked
description: "Run Velero data movement backups with --snapshot-move-data, choose --data-mover and --backup-type, and watch DataUpload progress."
sources:
  - https://velero.io/docs/main/csi-snapshot-data-movement/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Select the mover per backup with `--data-mover`: `velero` (default, currently `velero-fs`), `velero-block`, `velero-fs`, or a custom mover name. Select the type with `--backup-type`: `Incremental` (default) or `Full`.

```bash
velero backup create NAME --snapshot-move-data --data-mover velero-block
velero backup create NAME --snapshot-move-data --data-mover velero-block --backup-type Full
velero backup create NAME --snapshot-move-data --data-mover velero-fs
```

Incremental for `velero-block` backs up only changed blocks reported by the CSI SnapshotMetadataService; for `velero-fs` it uploads new or modified files. Full for block backs up all allocated blocks, treating unallocated regions as zeroes.

Fallback: an incremental block backup falls back to full when the metadata service errors, critical parent information is missing, or the parent snapshot is gone from the repository. The description then shows `Backup Type: Incremental (fallen back to Full)` and the reason is in `status.activities` of the DataUpload.

Progress:

```bash
kubectl -n velero get datauploads -o wide -l velero.io/backup-name=NAME -w
velero backup describe NAME --details
```

`-o wide` adds `INCREMENTAL BYTES`. Phases end in `Completed`, `Failed` or `Cancelled`. Snapshots and helper pods disappear after completion.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/csi-snapshot-data-movement/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
