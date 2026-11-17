---
id: computing-software.database-administration.database-backup-recovery.storage-snapshots-and-crash-consistency
name: storage-snapshots-and-crash-consistency
category: computing-software
field: database-administration
product: database-backup-recovery
tags: [database-administration, backup-strategy, point-in-time-recovery, crash-consistent-snapshot, application-consistent-snapshot, ebs-snapshot, lvm-snapshot, multi-volume-consistency, fsfreeze, vss]
level: advanced
status: draft
description: "Use disk/volume snapshots as database backups correctly: crash-consistent vs application-consistent, multi-volume consistency groups, and the backup-mode hooks per engine."
sources:
  - https://www.postgresql.org/docs/current/backup-file.html
  - https://docs.aws.amazon.com/ebs/latest/userguide/ebs-create-snapshots.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/create-a-transact-sql-snapshot-backup
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Storage snapshots and crash consistency

**Goal:** volume snapshots that restore to a working database every time.

## Crash-consistent is usually enough, if atomic
A snapshot taken at one instant of **all** database files (data + WAL/redo/log)
looks like a power cut: the engine runs crash recovery on start and is
consistent. Requirements:
- every volume the database uses (data, WAL, tablespaces, redo, undo) in the
  same atomic snapshot: one volume, or a **multi-volume consistency group**
  (EBS multi-volume snapshots, LVM on one VG, SAN consistency groups);
- fsync and full_page_writes/doublewrite left on.
Separate per-volume snapshots taken seconds apart are **not** consistent.

## Application-consistent (when multi-volume atomicity isn't available, or for PITR bases)
| Engine | Hook |
|---|---|
| PostgreSQL | `SELECT pg_backup_start('snap', true);` ... snapshot ... `SELECT * FROM pg_backup_stop();` and store the returned `backup_label` content with the snapshot (same session must stay open) |
| MySQL InnoDB | `FLUSH TABLES WITH READ LOCK` briefly, or `LOCK INSTANCE FOR BACKUP` (8.0) + note binlog position; crash-consistent snapshot is fine with InnoDB-only |
| SQL Server 2022 | `ALTER DATABASE appdb SET SUSPEND_FOR_SNAPSHOT_BACKUP = ON;` snapshot, then `BACKUP DATABASE appdb TO DISK='appdb.bkm' WITH METADATA_ONLY;` (older: VSS writer) |
| Oracle | `ALTER DATABASE BEGIN BACKUP;` ... `END BACKUP;` (or Storage Snapshot Optimization 12c+, no backup mode needed if snapshots are atomic and ordered) |
Filesystem freeze (`fsfreeze -f`, VSS on Windows) makes the filesystem
consistent but not the database by itself.

## PITR with snapshots
A snapshot is a base backup; add continuous WAL/binlog/log archiving to roll
forward to any point after it.

## Gotchas
- Snapshots on the same storage array/account are not offsite; copy them to
  another region/account (and protect against deletion: object lock / backup vault lock).
- Restored cloud volumes may be lazily loaded from object storage: first reads
  are slow (EBS initialization / fast snapshot restore).
- Snapshot schedules don't verify anything: restore-test them.

## Verify
Restore a snapshot to a new host, start the database, see crash recovery (or
backup_label recovery) complete, run engine checks (`pg_amcheck`, `CHECK TABLE`,
`DBCC CHECKDB`, `RMAN VALIDATE`).
