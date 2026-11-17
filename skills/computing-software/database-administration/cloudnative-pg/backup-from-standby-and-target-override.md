---
id: computing-software.database-administration.cloudnative-pg.backup-from-standby-and-target-override
name: backup-from-standby-and-target-override
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [backup, standby, prefer-standby, backup-target, primary, cold-backup, archive-timeout]
level: advanced
status: docs-checked
description: "Back up from the most up-to-date standby by default (prefer-standby), force primary per cluster or per backup, mind cold snapshots."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/backup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A base backup reads the whole data set, so it can cause I/O contention. CloudNativePG therefore backs up from a standby by default: with target `prefer-standby` it picks the **most up-to-date replica**, runs the backup there and falls back to the primary if no standby is available.

Caveat: like `pg_basebackup` from an online standby, no WAL switch is forced on the primary. In low-write deployments this can give unexpected short-term results before `archive_timeout` closes a segment. The standby lagging does not matter much in the span from first backup to last archived WAL, since the base backup is only the recovery starting point.

Force the primary cluster-wide:

```yaml
spec:
  backup:
    target: "primary"
```

Override per backup, in a `Backup` or `ScheduledBackup`:

```yaml
spec:
  cluster:
    name: [...]
  target: "primary"
```

This takes the backup from the primary even when the cluster default is `prefer-standby`.

Warning: with `primary` as the target for **cold backups using volume snapshots**, the primary must be shut down temporarily, interrupting all writes. The same applies to single-instance clusters even when you did not set the target.

## Checked

2026-11-08. prefer-standby behaviour, spec.backup.target and the per-resource override confirmed on the Backup page, section Backup from a Standby.

Method: documentation only; no commands were run.
