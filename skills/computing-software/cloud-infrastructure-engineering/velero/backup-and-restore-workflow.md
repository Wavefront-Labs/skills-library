---
id: computing-software.cloud-infrastructure-engineering.velero.backup-and-restore-workflow
name: backup-and-restore-workflow
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [backup-workflow, restore-workflow, backupcontroller, restorecontroller, crd]
level: practitioner
status: docs-checked
description: "How Velero processes a backup and a restore: CRD objects, controllers, snapshots, non-destructive restore and the preferred API version rule."
sources:
  - https://velero.io/docs/main/how-velero-works/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every Velero operation (on-demand backup, schedule, restore) is a custom resource stored in etcd and processed by a controller.

Backup workflow for `velero backup create test-backup`: the client creates a `Backup` object, the `BackupController` validates it, queries the API server for resources, then uploads the tarball to object storage. Persistent volumes are snapshotted by default; disable with `--snapshot-volumes=false`. Backups are not atomic: objects changed during the backup may be missed.

Restore workflow for `velero restore create`: the client creates a `Restore` object, the `RestoreController` validates it, fetches the backup from object storage, preprocesses resources (for example checking backed-up API versions against the target cluster), then restores eligible resources one at a time. Default name is `<BACKUP NAME>-<TIMESTAMP>` (YYYYMMDDhhmmss) and restored objects carry the label `velero.io/restore-name`.

Restores are non-destructive: existing resources are skipped. Set `--existing-resource-policy` to `update` to patch existing ones.

Gotcha: Velero backs up each resource at the API server's preferred group/version. The target cluster must serve that same group/version, though it need not be preferred there.

Restores can use namespace remapping, for example "abc" to "def", in one restore. Set the storage location read-only during a restore so no backup is created or deleted by accident.

## Checked

2026-11-08. Read in full: the How Velero Works page. Every remaining claim was confirmed there. Removed or reworded: nothing.

Method: documentation only; no commands were run.
