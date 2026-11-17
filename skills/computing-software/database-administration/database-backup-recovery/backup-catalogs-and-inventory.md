---
id: computing-software.database-administration.database-backup-recovery.backup-catalogs-and-inventory
name: backup-catalogs-and-inventory
category: computing-software
field: database-administration
product: database-backup-recovery
tags: [database-administration, database-backup-recovery, backup-catalog, backup-inventory, rman-catalog, backup-metadata, backup-strategy]
level: practitioner
status: draft
description: "Keep a reliable backup catalog and inventory: what was backed up, where, with which keys and tools, using RMAN catalog, msdb history, pgBackRest info and a cross-engine register."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/managing-recovery-catalog.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/backup-history-and-header-information-sql-server
  - https://pgbackrest.org/command.html#command-info
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Backup catalogs and inventory

**Goal:** during an incident, answer in minutes: which backups exist for this database, where they are, whether they are complete, and what is needed to restore them.

## Tool-level catalogs
- **Oracle RMAN**: control file records (limited by `CONTROL_FILE_RECORD_KEEP_TIME`) or a **recovery catalog** database (`CREATE CATALOG`, `REGISTER DATABASE`) for long history, stored scripts and multiple databases. `LIST BACKUP SUMMARY`, `REPORT NEED BACKUP`, `CROSSCHECK BACKUP` (marks missing pieces EXPIRED), `DELETE EXPIRED`.
- **SQL Server**: `msdb.dbo.backupset`, `backupmediafamily` record every backup:
```sql
SELECT bs.database_name, bs.type, bs.backup_finish_date, bmf.physical_device_name, bs.is_copy_only, bs.encryptor_type
FROM msdb.dbo.backupset bs JOIN msdb.dbo.backupmediafamily bmf ON bs.media_set_id = bmf.media_set_id
ORDER BY bs.backup_finish_date DESC;
```
`RESTORE HEADERONLY / FILELISTONLY / VERIFYONLY` inspect a file without msdb. Purge old history with `sp_delete_backuphistory` (msdb bloat).
- **pgBackRest**: `pgbackrest info --stanza=main --output=json` (backups, WAL ranges, sizes, repo); Barman `barman list-backups`, `barman check`; WAL-G `backup-list --detail`.
- **MongoDB Ops Manager/Atlas**: snapshot lists via API.

## Cross-engine inventory (register)
A simple table or CMDB entry per protected database:
| Field | Example |
|---|---|
| Database / cluster | orders-prod (PG 16) |
| Owner / tier | payments, tier 1 |
| Method | pgBackRest full weekly, diff daily, WAL continuous |
| Repositories | s3://bk-prod-syd (Object Lock), s3://bk-dr-mel |
| RPO / RTO target | 5 min / 2 h |
| Encryption / key location | aes-256, Vault path secret/pgbackrest/orders |
| Retention | 35 d + 12 monthly |
| Last successful backup / last restore test | auto-filled by monitoring |
| Runbook link | wiki/runbooks/orders-restore |

Populate "last successful" automatically from the tools (JSON output, msdb queries) and alert when missing.

## Hygiene
- Crosscheck catalogs against storage regularly (pieces deleted by lifecycle rules but still listed are worse than useless).
- Back up the catalog itself (RMAN catalog DB, msdb, pgBackRest config + repo metadata).
- Keep tool versions recorded; restoring may require the same backup tool version.

## Verify
Monthly report: every database in the inventory has a backup within its RPO, a catalog entry that crosschecks AVAILABLE, and a restore test within its required interval.
