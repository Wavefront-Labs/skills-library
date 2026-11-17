---
id: computing-software.database-administration.cloudnative-pg.recovery-application-database-and-empty-archive-check
name: recovery-application-database-and-empty-archive-check
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [recovery, application-database, skipemptywalarchivecheck, servername, wal-archive, safety-check]
level: advanced
status: docs-checked
description: "Set the app database, owner and password after recovery; handle the Expected empty archive check and skipEmptyWalArchiveCheck."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/recovery.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Application database.** Recovery copies the database name and owner from the backup. To change them:

```yaml
spec:
  bootstrap:
    recovery:
      database: app
      owner: app
      secret:
        name: app-secret
```

Only **after recovery completes**: the database and user are created if missing, ownership is granted if needed, and if `owner` matches the Secret `username` the password is set from the Secret. During recovery roles remain as in the source cluster.

**What happens.** The operator injects an init container into the first instance that restores the base backup (duration depends on backup size and network/storage speed, using `barman-cloud-restore`). Then PostgreSQL starts in recovery mode, healthy for liveness but not accepting connections, fetching WAL through `restore_command` (`barman-cloud-wal-restore`; speed up with `maxParallel`). It stops at the end of WAL or the target. The operator then sets the superuser password, the new primary starts and other instances join as replicas. If unsure about PITR, give the recovery cluster the same `.spec.postgresql.parameters` as the original, then change them afterwards.

**Backup section in the restored cluster.** A restored cluster can immediately archive and back up, but avoid reusing the same `ObjectStore` for backup and recovery; if you must, use a unique `serverName` per cluster.

A safety check refuses to overwrite data in a shared bucket. The cluster stays in `Setting up primary` and pods log `ERROR: WAL archive check failed for server recoveredCluster: Expected empty archive`. Bypass only as an expert, with annotation `cnpg.io/skipEmptyWalArchiveCheck: enabled`; misuse can cause severe data loss.

## Checked

2026-11-08. Post-recovery database configuration, phase description, shared bucket safety check and annotation confirmed on the Recovery page.

Method: documentation only; no commands were run.
