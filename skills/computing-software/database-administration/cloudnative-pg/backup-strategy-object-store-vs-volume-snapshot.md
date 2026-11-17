---
id: computing-software.database-administration.cloudnative-pg.backup-strategy-object-store-vs-volume-snapshot
name: backup-strategy-object-store-vs-volume-snapshot
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [backup, wal-archive, hot-backup, cold-backup, volume-snapshot, object-store, cnpg-i, physical-backup]
level: practitioner
status: docs-checked
description: "Choose a physical backup approach: Barman Cloud plugin object store versus CSI volume snapshots, hot versus cold backups."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/backup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CloudNativePG backs up **physically**; `pg_dump` logical backups are not managed and are unsuitable for business continuity. Since 1.26 native backup is being phased out into CNPG-I plugins; the Barman Cloud Plugin is the officially supported one. Native choices are Barman Cloud object storage (deprecated, last in 1.31, removed from 1.32.0) and Kubernetes volume snapshots.

A backup infrastructure has a **WAL archive** (continuous backup; enables hot backups and PITR; gives RPO of 5 minutes or less out of the box, even across regions) and **physical base backups**. A WAL archive alone is useless: without a base backup you cannot restore. Always set up the archive in production.

Hot backups run online and need the archive. **Cold backups** are taken with PostgreSQL shut down, are consistent by definition and restart without an archive, which suits RPOs of one hour or a day.

| Feature | Object store | Volume snapshots |
|---|---|---|
| WAL archiving | Required | Recommended |
| Cold backup | no | yes |
| Hot backup | yes | yes |
| Incremental / differential | no | yes, per storage class |
| Retention policies | yes | no |
| Snapshot recovery | no (emulate with `recoveryTarget.targetImmediate`) | yes |

Decide on object store reachability, CSI snapshot support, database size (for very large databases snapshots are generally preferred because copy-on-write gives faster recovery and better RTO), data mobility across regions, and team familiarity. Object store backups always need WAL archiving, hot only, no incremental.

## Checked

2026-11-08. Concepts, comparison table and the plugin transition (native Barman Cloud removed from 1.32.0) confirmed on the Backup page.

Method: documentation only; no commands were run.
