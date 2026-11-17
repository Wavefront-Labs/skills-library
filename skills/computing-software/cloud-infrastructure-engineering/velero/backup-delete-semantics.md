---
id: computing-software.cloud-infrastructure-engineering.velero.backup-delete-semantics
name: backup-delete-semantics
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [backup-delete, velero-backup-delete, orphaned-backup-cr, repository-maintenance, kubectl-delete-backup]
level: practitioner
status: docs-checked
description: "Delete Velero backups correctly: what velero backup delete removes versus kubectl delete backup, and why space frees later."
sources:
  - https://velero.io/docs/main/backup-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two commands delete backups, with very different effects.

`velero backup delete <backupName>` does three things:
- Immediately deletes the resource backup data from backup storage.
- Immediately deletes volume snapshots associated with the backup, if any (CSI snapshot backup or native snapshots).
- Triggers deletion of volume backup data persisted in the backup repository (CSI snapshot data movement or fs-backup). Storage space is not released at once: backup repository maintenance jobs garbage-collect the data and finally release the space.

Deletion itself needs extra space in backup storage. Make sure the storage is not full during deletion, otherwise the deletion or the following repository maintenance jobs may fail.

`kubectl delete backup <backupName> -n <veleroNamespace>` deletes only the backup custom resource and does not delete any associated data from backup storage. Use it for limited purposes only, for example when all the backup data has already been deleted from storage and you just need to clear orphaned CRs.

## Checked

Checked 2026-11-08 against the Velero Backup Reference page ("Deleting Backups", read in full). Removed unsourced claims: the `--ttl` expiry paragraph, the `velero.io/gc-failure` label and the Kopia bucket-usage gotcha.

Method: documentation only; no commands were run.
