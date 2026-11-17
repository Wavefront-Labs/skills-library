---
id: computing-software.database-administration.sql-server.contained-availability-groups
name: contained-availability-groups
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, contained-availability-group, availability-groups, sql-server-2022, contained-master, contained-msdb, logins, agent-jobs]
level: advanced
status: docs-checked
description: "Use SQL Server 2022 contained availability groups so logins, Agent jobs and permissions fail over with the AG, and manage objects through the listener."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/contained-availability-groups-overview
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/create-availability-group-transact-sql
  - https://docs.dbatools.io/Copy-DbaLogin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Contained availability groups (SQL Server 2022)

Classic AGs replicate user databases only; logins, Agent jobs, linked servers and credentials
must be copied to every replica by hand. A contained AG adds its own `master` and `msdb`
(named `<AG>_master`, `<AG>_msdb`) replicated with the group.

## Create
```sql
CREATE AVAILABILITY GROUP [CAG1]
WITH (CONTAINED, AUTOMATED_BACKUP_PREFERENCE = SECONDARY)
FOR DATABASE appdb
REPLICA ON
  N'sql01' WITH (ENDPOINT_URL = N'TCP://sql01.corp.example.com:5022', AVAILABILITY_MODE = SYNCHRONOUS_COMMIT,
                 FAILOVER_MODE = AUTOMATIC, SEEDING_MODE = AUTOMATIC),
  N'sql02' WITH (ENDPOINT_URL = N'TCP://sql02.corp.example.com:5022', AVAILABILITY_MODE = SYNCHRONOUS_COMMIT,
                 FAILOVER_MODE = AUTOMATIC, SEEDING_MODE = AUTOMATIC);
ALTER AVAILABILITY GROUP [CAG1] ADD LISTENER N'cag1-listener' (WITH IP ((N'10.1.0.60', N'255.255.255.0')), PORT = 1433);
-- on sql02
ALTER AVAILABILITY GROUP [CAG1] JOIN; ALTER AVAILABILITY GROUP [CAG1] GRANT CREATE ANY DATABASE;
```
`REUSE_SYSTEM_DATABASES` recreates the AG over its existing contained system databases (do not list them in the statement; SQL Server finds them). Contained system databases always seed automatically. SQL Server 2025 adds distributed AG support and `AUTOSEEDING_SYSTEM_DATABASES` for a contained AG used as a forwarder.

## Working inside it
Connect **through the listener**: the session sees the contained master/msdb as `master`/`msdb`.
```sql
-- connected to cag1-listener
CREATE LOGIN app_login WITH PASSWORD = '<SECRET>';      -- lands in CAG1_master, follows failover
EXEC msdb.dbo.sp_add_job @job_name = N'appdb nightly';   -- lands in CAG1_msdb
```
Connecting to the instance name gives the instance-level master/msdb; objects created there do
not move. Jobs in a contained AG run only on the primary replica. When the AG is created, sysadmin logins of the parent instance are copied into the contained master; other local logins lose access to databases once they join the AG, so recreate them inside the contained AG. A contained AG is not a security boundary.

## Rules and limits
- Instance-level settings stay per instance: `sp_configure` can be read from a contained connection but written only from an instance connection, most database, endpoint and AG operations need an instance connection, and server audits must be created inside each contained AG.
- Applications should use only listener connections; DBAs need instance logins for instance maintenance.
- Not supported: SQL Server replication of any type, log shipping with the target in a contained AG, and SSIS packages or maintenance plans. CDC needs the Agent running on every replica and must be configured through the listener; TDE needs the database master key installed in the contained master; resource governor on contained AG connections needs SQL Server 2022 CU18 or later.
- Backup: back up `CAG1_master` and `CAG1_msdb` along with user databases.

## Migrating from a classic AG
Script logins (with SIDs, e.g. dbatools `Copy-DbaLogin`) and jobs (e.g. `Export-DbaScript`), run them connected via
the new contained AG listener, repoint applications to the contained listener.

## Verify
Create a test login and job through the listener, fail over, and confirm both exist and work on the new primary.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: contained availability groups overview for SQL Server 2025 (SQL Server 2022 and later, <AG>_master and <AG>_msdb contained system databases, connect through the listener, jobs run only on the primary, sysadmin logins copied at creation, not a security boundary, sp_configure read-only from contained connections, server audits per contained AG, REUSE_SYSTEM_DATABASES and AUTOSEEDING_SYSTEM_DATABASES (2025), automatic seeding of system databases, unsupported replication and SSIS/maintenance plans, log shipping target, CDC, TDE, resource governor CU18 note, sys.availability_groups.is_contained), dbatools Copy-DbaLogin. Removed as unconfirmed: the dbatools Export-DbaLogin name.
Method: documentation only; no commands were run.
