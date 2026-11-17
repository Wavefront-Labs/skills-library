---
id: computing-software.cloud-infrastructure-engineering.velero.fs-backup-limitations
name: fs-backup-limitations
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [fsb-limitations, emptydir, orphan-pvc, vcluster, incremental-backup]
level: advanced
status: docs-checked
description: "Know File System Backup limits: hostPath, static encryption key, emptyDir full backups, large files, orphan PVCs and non-standard mounts."
sources:
  - https://velero.io/docs/main/file-system-backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Limitations listed for File System Backup:

- hostPath volumes are unsupported; local persistent volumes are supported.
- Velero uses a static, common encryption key for every repository it creates, so anyone with access to backup storage can decrypt the data. Limit access to the storage.
- The incremental chain survives pod reschedules for PVCs. For non-PVC pod volumes such as emptyDir, a deleted and recreated pod (for example from a ReplicaSet) makes the next backup full, because the pod volume lifecycle follows the pod.
- For a single file, FSB relies on deduplication to find differences, so large files (database files) take a long time to scan even if little changed.
- FSB reads the node filesystem, so it can only back up volumes mounted by a pod, not a PVC directly. For orphan PVC/PV pairs, users run a staging pod (a busybox or alpine container with an infinite sleep) that mounts them before the backup.
- Volumes must be mounted under `<hostPath>/<pod UID>`. Systems that do not do this, such as vCluster, do not work with FSB.
- A file system restore for a pod does not start until all the volumes of that pod are bound, even if some are ready. If other volumes restore by another type (for example CSI snapshot restore), the fs restores wait for them.

Restore workflow for in-place data: pass `--existing-volume-data-policy=full` or `incremental` to restore into an existing bound PVC.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/file-system-backup/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
