---
id: computing-software.database-administration.cloudnative-pg.scheduledbackup-cron-immediate-suspend
name: scheduledbackup-cron-immediate-suspend
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [scheduledbackup, cron, backup-schedule, backupownerreference, immediate, suspend, rto]
level: practitioner
status: docs-checked
description: "Write a ScheduledBackup with the six-field cron format, run it immediately, suspend it, set backupOwnerReference, weigh RTO."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/backup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`ScheduledBackup` is the recommended way to get reliable backups. The `schedule` field is a **six-field** cron expression with *seconds first* (Go `cron` package), unlike Unix crontab:

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: ScheduledBackup
metadata:
  name: backup-example
spec:
  schedule: "0 0 0 * * *"  # At midnight every day
  backupOwnerReference: self
  cluster:
    name: pg-backup
  # method: plugin, volumeSnapshot, or barmanObjectStore (default)
```

The Kubernetes CronJob equivalent of that schedule is `0 0 * * *`. `spec.cluster` is immutable; to target another `Cluster` create a new `ScheduledBackup`.

Other fields:

```yaml
spec:
  immediate: true   # also run a backup as soon as the object is created
  suspend: true     # temporarily stop scheduled backups
```

`backupOwnerReference` decides who owns the generated `Backup` objects: `none` (legacy, no owner), `self` (the `ScheduledBackup`) or `cluster` (the PostgreSQL cluster).

Frequency drives RTO: restore time depends on base backup size and the number of WAL files to fetch and replay. Test restores regularly and time a full recovery. A weekly base backup is usually enough, and full backups more often than daily are rare.

## Checked

2026-11-08. Six-field cron, example manifest, immediate/suspend and owner reference options confirmed on the Backup page, section Scheduled Backups.

Method: documentation only; no commands were run.
