---
id: computing-software.database-administration.tidb.tidb-br-backup-restore-overview
name: tidb-br-backup-restore-overview
category: computing-software
field: database-administration
product: tidb
tags: [tidb, br, backup, restore, pitr, snapshot-backup, log-backup, rpo, check-requirements]
level: practitioner
status: docs-checked
description: "Plan TiDB backup and restore with BR: snapshot versus log backup, PITR, restrictions, performance impact, storage targets and version compatibility rules."
sources: ["https://docs.pingcap.com/tidb/stable/backup-and-restore-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tidb br backup restore overview

BR (Backup and Restore) is TiDB's last-resort data safety tool. It supports DR backups with an RPO as short as 5 minutes, rolling back after application mistakes, auditing historical data and cloning production for testing.

Two backup types:
- Snapshot backup: a transactionally consistent full backup at one point in time.
- Log backup: continuous KV change capture running on all TiKV nodes, flushed to storage every 3 to 5 minutes. Combined with regular snapshots it enables point-in-time recovery (PITR).

Restore options: full snapshot restore, restore of specific databases or tables, and PITR with `br restore point`, which picks the latest snapshot before the target time plus the log backup.

Restrictions: PITR restores only into an empty cluster; it cannot restore user tables or privilege tables from system tables; BR does not support multiple concurrent backup tasks on one cluster; avoid backing up tables that are being restored; when restoring with PITR you cannot run a log backup task or TiCDC replication to a downstream.

Tips: back up in off-peak hours and run tasks one at a time. Restore consumes as many target resources as it can, so restore into a new or offline cluster. Snapshot backup impact is generally below 20 percent when resources suffice, log backup about 5 percent. Restore runs around 1 GiB/s per TiKV node; PITR log restore about 30 GiB/h per TiKV node.

Targets: Amazon S3, GCS, Azure Blob Storage, NFS and S3-compatible stores. Ensure bandwidth and IOPS suffice. Use the BR version matching the cluster's major version; `--check-requirements=false` skips the version check but is risky.

## Checked

2026-11-09: use cases, RPO, restrictions, tips, impact figures, restore speeds, storage targets, `br restore point` and the version-check flag confirmed against the BR overview page (pingcap/docs br/backup-and-restore-overview.md, read in full).

Method: docs-checked 2026-11-09 against pingcap/docs br/backup-and-restore-overview.md
