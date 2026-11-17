---
id: computing-software.database-administration.sql-server.automatic-seeding-and-adding-databases-to-an-ag
name: automatic-seeding-and-adding-databases-to-an-ag
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, always-on, availability-group, automatic-seeding, seeding-mode, join-only, add-database-to-ag, sys-dm-hadr-automatic-seeding, direct-seeding]
level: advanced
status: docs-checked
description: "Add databases to a SQL Server availability group with automatic seeding or manual backup/restore, monitor seeding, and fix the common stuck states."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/automatically-initialize-always-on-availability-group
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/availability-group-add-a-database
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-set-hadr
  - https://docs.dbatools.io/Add-DbaAgDatabase.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automatic seeding and adding databases to an AG

## Prerequisites for any database
FULL recovery model and a current full backup plus log backup (not used by automatic seeding, but required before the database can be added). On SQL Server 2016 automatic seeding needs identical data and log paths on every replica; 2017 and later can differ, but Microsoft recommends identical paths when all replicas run on the same OS platform.

## Automatic seeding (2016+)
The primary streams the database to secondaries over the database mirroring endpoint (open its port, commonly 5022, in firewalls) using a VDI backup, so no backup share is needed.
```sql
-- on the primary, per replica (also settable at CREATE AVAILABILITY GROUP)
ALTER AVAILABILITY GROUP ag1 MODIFY REPLICA ON N'SQL2' WITH (SEEDING_MODE = AUTOMATIC);
-- on each secondary: allow the AG to create databases
ALTER AVAILABILITY GROUP ag1 GRANT CREATE ANY DATABASE;
-- on the primary
ALTER AVAILABILITY GROUP ag1 ADD DATABASE appdb;
```
Monitor:
```sql
SELECT ag.name, adc.database_name, s.current_state, s.failure_state_desc,
       s.performed_seeding, s.start_time, s.completion_time
FROM sys.dm_hadr_automatic_seeding s
JOIN sys.availability_groups ag ON ag.group_id = s.ag_id
JOIN sys.availability_databases_cluster adc ON adc.group_database_id = s.ag_db_id
ORDER BY s.start_time DESC;
SELECT local_database_name, transferred_size_bytes/1048576 AS mb, database_size_bytes/1048576 AS total_mb,
       transfer_rate_bytes_per_second/1048576 AS mb_s
FROM sys.dm_hadr_physical_seeding_stats;
```
Speed: trace flag 9567 on the primary compresses the seeding stream (more CPU, less transfer time). Seeding is a backup over the network and the primary's log cannot truncate while it runs, so for very large databases or distant replicas prefer manual seeding.

## Manual seeding (backup/restore, or JOIN_ONLY)
```sql
-- primary
BACKUP DATABASE appdb TO DISK = '\\fs\seed\appdb.bak' WITH COMPRESSION, CHECKSUM;
BACKUP LOG appdb TO DISK = '\\fs\seed\appdb.trn';
ALTER AVAILABILITY GROUP ag1 ADD DATABASE appdb;
-- secondary
RESTORE DATABASE appdb FROM DISK = '\\fs\seed\appdb.bak' WITH NORECOVERY;
RESTORE LOG appdb FROM DISK = '\\fs\seed\appdb.trn' WITH NORECOVERY;
ALTER DATABASE appdb SET HADR AVAILABILITY GROUP = ag1;
```
Restore WITH NORECOVERY from recent backups ending with a log backup recent enough to catch up, and apply any log backups taken since, or the join fails. dbatools: `Add-DbaAgDatabase -SqlInstance sql1 -AvailabilityGroup ag1 -Database appdb -SeedingMode Manual -SharedPath \\fs\seed`.

## Stuck states
- Secondary database missing: query `sys.dm_hadr_automatic_seeding` (`failure_state_desc`, `error_code`) on both replicas. Check that `GRANT CREATE ANY DATABASE` was run on the secondary, that it has enough free disk space, and that paths suit its SQL Server version.
- `NOT SYNCHRONIZING` after join: endpoint connect permission for the replica's service account, firewall on the mirroring endpoint port, or a log chain gap.
- Restart failed seeding (for example after adding disk space): rerun `ALTER AVAILABILITY GROUP ag1 MODIFY REPLICA ON N'SQL2' WITH (SEEDING_MODE = AUTOMATIC);` on the primary. `SEEDING_MODE = MANUAL` cancels replicas currently seeding; `DENY CREATE ANY DATABASE` on a secondary stops the primary seeding more databases to it.

## Verify
- [ ] `sys.dm_hadr_database_replica_states` shows SYNCHRONIZED (sync) or SYNCHRONIZING (async) for the new DB on all replicas.
- [ ] Logins/jobs for the new database exist on all replicas.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: automatic seeding article (introduced in SQL Server 2016, prerequisites and path rule, backups required but unused, mirroring endpoint, GRANT/DENY CREATE ANY DATABASE, MODIFY REPLICA SEEDING_MODE restarts or stops seeding, sys.dm_hadr_automatic_seeding and sys.dm_hadr_physical_seeding_stats columns, trace flag 9567 on the primary, when not to use it), add-a-database page (ALTER AVAILABILITY GROUP ADD DATABASE), ALTER DATABASE SET HADR page (AVAILABILITY GROUP = syntax, NORECOVERY prerequisite), dbatools Add-DbaAgDatabase (-SeedingMode, -SharedPath). Removed as unconfirmed: the 'Seeding check message timeout' text, the SET HADR OFF re-seed recipe, the TDE note and the not-in-another-AG and AUTO_CLOSE prerequisites.
Method: documentation only; no commands were run.
