---
id: computing-software.cloud-infrastructure-engineering.velero.in-place-volume-restore
name: in-place-volume-restore
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [existing-volume-data-policy, in-place-restore, delete-extra-files, allow-existing-volume-mismatch, incremental-restore]
level: advanced
status: docs-checked
description: "Restore backup data into an existing bound PVC with --existing-volume-data-policy full or incremental, and which backup methods support it."
sources:
  - https://velero.io/docs/main/volume-data-inplace-restore/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Velero restores PV data only when it provisions a new PVC; an existing PVC is left untouched. In-place restore overwrites an existing bound PVC and PV without deleting them. Always take a safety backup first, for example a CSI snapshot backup without data movement.

Supported: CSI snapshot with `velero-block`, CSI snapshot with `velero-fs`, and File System Backup, each for full and incremental. Not supported: CSI snapshot without data movement, and native cloud snapshots.

`--existing-volume-data-policy` (Restore field `existingVolumeDataPolicy`): `none` or empty (default, no in-place restore), `full` (overwrite all data), `incremental` (restore only changed or missing data). If the target PVC does not exist, Velero provisions normally.

```bash
velero restore create NAME --from-backup BACKUP --existing-volume-data-policy=incremental --delete-extra-files --wait
```

Incremental detail: `velero-block` takes a temporary CSI snapshot of the target as baseline and uses CBT to compute deltas, falling back to a full in-place restore if CBT or the baseline snapshot is unavailable. File system restores compare file metadata and never need CBT.

`--delete-extra-files` (`uploaderConfig.deleteExtraFiles: true`) removes files absent from the backup, for file system restores only, and is ignored when the policy is none.

`--allow-existing-volume-mismatch` lets the restore proceed when the PVC volume handle differs from the backup, logging a warning. `--existing-resource-policy=update` alone does not restore data.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/volume-data-inplace-restore/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
