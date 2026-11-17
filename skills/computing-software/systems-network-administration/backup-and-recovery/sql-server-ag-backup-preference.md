---
id: computing-software.systems-network-administration.backup-and-recovery.sql-server-ag-backup-preference
name: sql-server-ag-backup-preference
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-preference, sql-server, always-on-availability-groups, database-backup, copy-only, backup-priority]
level: advanced
status: docs-checked
description: "Run SQL Server backups on Always On availability group secondaries: automated backup preference, backup priority, fn_hadr_backup_is_preferred_replica, and copy-only rules."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/active-secondaries-backup-on-secondary-replicas-always-on-availability-groups
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-functions/sys-fn-hadr-backup-is-preferred-replica-transact-sql
  - https://ola.hallengren.com/sql-server-backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backups on AG secondary replicas

**Goal:** offload backups from the primary while keeping one unbroken log chain across all replicas.

## What secondaries can do
| Backup type | On secondary |
|---|---|
| Full | `COPY_ONLY`; SQL Server 2025 and later also allow regular full backups |
| Differential | not supported before SQL Server 2025; allowed from 2025 |
| Log | regular only (`COPY_ONLY` is not supported for log backups on secondaries); one consistent chain across all replicas |
The secondary must be able to communicate with the primary and be SYNCHRONIZED or SYNCHRONIZING. Concurrent backups (a log backup on the primary while a full backup runs on a secondary) are not supported. A copy-only backup on a secondary can raise error 9019 and stall synchronisation to that secondary until it finishes; if so, run the full backup on the primary.

## Configure preference
```sql
ALTER AVAILABILITY GROUP [AG1] SET (AUTOMATED_BACKUP_PREFERENCE = SECONDARY);   -- PRIMARY | SECONDARY_ONLY | SECONDARY | NONE
ALTER AVAILABILITY GROUP [AG1] MODIFY REPLICA ON N'SQL2' WITH (BACKUP_PRIORITY = 80);
ALTER AVAILABILITY GROUP [AG1] MODIFY REPLICA ON N'SQL3' WITH (BACKUP_PRIORITY = 0);   -- 0 = never
```
SQL Server does **not** enforce this and it has no effect on ad hoc backups. Your jobs must check it. `BACKUP_PRIORITY` is 0 to 100: 0 means the replica is never chosen, 1 is lowest and 100 highest.

## Jobs on every replica
Deploy the same job on all replicas:
```sql
IF sys.fn_hadr_backup_is_preferred_replica(N'SalesDB') = 1
    BACKUP LOG [SalesDB] TO URL = N'https://acct.blob.core.windows.net/sql/SalesDB_log_...trn';
```
Ola Hallengren `DatabaseBackup` supports the AG backup preference (its `OverrideBackupPreference` option overrides it) and a `CopyOnly` option; read its documentation for how full backups on secondaries are handled. Write to a shared location reachable from every replica so a restore can find all files.

## Gotchas
- Before SQL Server 2025, differentials are not supported on secondaries, so run them on the primary (a copy-only full does not reset the differential base); many shops skip diffs on AGs.
- Log backups taken by different replicas form one chain; keep the files from all replicas together so a restore finds every one.
- Asynchronous DR replicas lag; backing up there raises effective RPO.

## Verify
Failover drill: after failover the jobs keep producing log backups from the new preferred replica, and a restore using files from both replicas succeeds.

## Checked
2026-10-28. Confirmed against Microsoft Learn: Offload supported backups to secondary replicas of an availability group (backup types, SYNCHRONIZED or SYNCHRONIZING requirement, error 9019, SQL Server 2025 change, log chain), ALTER AVAILABILITY GROUP (AUTOMATED_BACKUP_PREFERENCE values, BACKUP_PRIORITY 0 to 100, no enforcement), sys.fn_hadr_backup_is_preferred_replica, and the Ola Hallengren DatabaseBackup page (OverrideBackupPreference, CopyOnly). Removed: msdb history claim, LOG_BACKUP log reuse claim, and the claim that Hallengren always uses COPY_ONLY on secondaries.
Method: documentation only; no commands were run.
