---
id: computing-software.cloud-infrastructure-engineering.longhorn.system-backup
name: system-backup
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [system-backup, systembackup, volume-backup-policy, recurring-job, backup-target]
level: advanced
status: docs-checked
description: "Back up the Longhorn system resource bundle with the SystemBackup CRD or a system-backup recurring job, volumeBackupPolicy values and the limits."
sources:
  - https://longhorn.io/docs/1.13.0/advanced-resources/system-backup-restore/backup-longhorn-system/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: capture Longhorn resources so a cluster can be rebuilt.

A system backup creates a resource bundle and uploads it to the `default` backup target. The feature is available since v1.4.0. A backup target must be set or creation fails; unsetting it clears the existing `SystemBackup` CR. Optionally back up all volumes first so volume data matches.

`volumeBackupPolicy`:
- `if-not-present`: back up volumes with no backup or an outdated latest backup
- `always`: back up all volumes
- `disabled`: create no volume backups

```yaml
apiVersion: longhorn.io/v1beta2
kind: SystemBackup
metadata:
  name: demo
  namespace: longhorn-system
spec:
  volumeBackupPolicy: if-not-present
```

Check with `kubectl -n longhorn-system get systembackup`; ready when STATE is `Ready`. UI: Backup and Restore, System Backups, Create.

Recurring: a `RecurringJob` with `task: system-backup`, `cron`, `retain` and `parameters.volume-backup-policy`.

Delete with `kubectl -n longhorn-system delete systembackup/<name>`; this also deletes it from the backup store.

Limits:
- Only resources operated by Longhorn are included.
- `Nodes` are not backed up; the target cluster's manager creates its own.
- V2 backing images are not backed up.
- Bare `Pod` workloads are excluded, though their PVC, PV and Volume are collected.

## Checked

2026-11-08. Read in full against https://longhorn.io/docs/1.13.0/advanced-resources/system-backup-restore/backup-longhorn-system/ : volumeBackupPolicy values, SystemBackup and RecurringJob manifests, default target, limits. Nothing else was removed.

Method: documentation only; no commands were run.
