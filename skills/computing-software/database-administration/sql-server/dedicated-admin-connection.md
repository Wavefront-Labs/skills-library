---
id: computing-software.database-administration.sql-server.dedicated-admin-connection
name: dedicated-admin-connection
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, sql-server-configuration, dedicated-admin-connection, dac, remote-admin-connections, incident-response]
level: practitioner
status: docs-checked
description: "Enable and use the SQL Server Dedicated Admin Connection (DAC) to get in when the instance is unresponsive, and what you can and cannot do over it."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/diagnostic-connection-for-database-administrators
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/remote-admin-connections-server-configuration-option
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dedicated Admin Connection (DAC)

The DAC is a reserved scheduler and memory for **one** sysadmin connection, so you can
diagnose an instance that is out of worker threads, blocked, or pegged at 100% CPU.

## Enable remote DAC (do it now, before the incident)
By default the DAC listens only on the local machine (loopback).
```sql
EXEC sp_configure 'remote admin connections', 1;
RECONFIGURE;
```
On clustered systems the DAC is off for remote use by default and Microsoft recommends enabling
remote admin connections there. Azure SQL Database supports DAC too (name the target user
database; DAC connections to its `master` are not supported).

## Connect
```bash
sqlcmd -S ADMIN:sqlprod01 -E -d master
sqlcmd -S ADMIN:sqlprod01\INST2 -U sa -P '...'
sqlcmd -S sqlprod01 -E -A          # -A is the DAC switch
```
SSMS: use **File > New > Database Engine Query** with server name `admin:sqlprod01`.
Disable IntelliSense first (Tools > Options > Languages > Transact-SQL > IntelliSense), because it
tries to open a second connection per query window and only one DAC is allowed.

DAC port: TCP 1434 if available, otherwise assigned dynamically at startup; the error log
records the port. If remote admin connections is on, connect with an explicit port
(`sqlcmd -S tcp:<server>,<port>`). For local-only DAC use `sqlcmd -S 127.0.0.1,1434`.
Open the port in the firewall.

## What to do over it
Quick diagnostic queries only:
```sql
SELECT session_id, blocking_session_id, wait_type, wait_time, cpu_time, status,
       DB_NAME(database_id) db, t.text
FROM sys.dm_exec_requests r CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
ORDER BY cpu_time DESC;
SELECT COUNT(*) AS workers FROM sys.dm_os_workers;
KILL 87;
```
Then fix (kill the root blocker, reduce MAXDOP, etc.).

## Limits
- Only one DAC per instance; a second attempt is denied with error 17810. Find and close the
  existing one if a colleague is on.
- No parallel queries; `BACKUP` and `RESTORE` fail (error 3637); only limited resources are guaranteed,
  so avoid heavy DMVs (e.g. `sys.dm_tran_version_store`) and complex joins. Run blocking-prone
  queries under READ UNCOMMITTED with a short `LOCK_TIMEOUT`.
- Connect to `master` (`-d master`); if the login's default database is offline you get error 4060.
- SQL Server Express does not listen on the DAC port unless started with trace flag 7806.
- Must be sysadmin.
- If the instance is completely hung at the OS level, DAC may not help either.

## Verify
In a test, connect with `sqlcmd -S ADMIN:<server>` from a remote host and run
`SELECT wg.name FROM sys.dm_exec_sessions s JOIN sys.dm_resource_governor_workload_groups wg ON s.group_id = wg.group_id WHERE s.session_id = @@SPID;`
The DAC session is in workload group `DACGroup`.

## Checked
Date 2026-10-23. Documentation release: Diagnostic connection for database administrators (SQL Server 2017-2025, Azure SQL).
Confirmed: sysadmin only, local-only by default, `-A` and `admin:` forms, port 1434 or dynamic, one DAC per instance (error 17810), error 3637 for BACKUP/RESTORE, Azure SQL Database rules, DACGroup check, Express trace flag 7806. Removed the unconfirmed exact error-log and max-connection message texts and the Object Explorer claim.
Method: documentation only; no commands were run.
