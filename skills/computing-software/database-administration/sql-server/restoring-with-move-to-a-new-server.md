---
id: computing-software.database-administration.sql-server.restoring-with-move-to-a-new-server
name: restoring-with-move-to-a-new-server
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, sql-server-backup, restore-with-move, restore-filelistonly, database-migration, orphaned-users]
level: practitioner
status: docs-checked
description: "Restore a SQL Server database to a different server, name or path: FILELISTONLY, WITH MOVE, then fix owner, orphaned users and server-level metadata."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/restore-a-database-to-a-new-location-sql-server
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-statements-filelistonly-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/databases/manage-metadata-when-making-a-database-available-on-another-server
  - https://learn.microsoft.com/en-us/sql/sql-server/failover-clusters/troubleshoot-orphaned-users-sql-server
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Restoring to a new location or server (WITH MOVE)

## 1. Inspect the backup
```sql
RESTORE HEADERONLY   FROM DISK = N'<BACKUP_PATH>';   -- position of each backup set in the media set
RESTORE FILELISTONLY FROM DISK = N'<BACKUP_PATH>' WITH FILE = 1;   -- LogicalName, PhysicalName, Type
```
`FILELISTONLY` returns the logical and physical names of the files in a backup set; `HEADERONLY` tells you the
position of a backup set in the media set (the `FILE =` value).

## 2. Restore with new file paths (and optionally a new name)
```sql
RESTORE DATABASE Sales_Test
FROM DISK = N'<BACKUP_PATH>'
WITH MOVE N'Sales_data' TO N'<DATA_DIR>\Sales_Test.mdf',
     MOVE N'Sales_log'  TO N'<LOG_DIR>\Sales_Test_log.ldf',
     NORECOVERY;
RESTORE LOG Sales_Test FROM DISK = N'<LOG_BACKUP_PATH>' WITH NORECOVERY;
RESTORE DATABASE Sales_Test WITH RECOVERY;
```
- By default files are restored to their original locations. Use `MOVE` for each database file you relocate, and to
  avoid collisions with existing files. The logical names come from `FILELISTONLY`.
- The restoring administrator must be the only person using the database being restored.
- With the full or bulk-logged recovery model, back up the active transaction log of an existing database before
  restoring over it.
- If the database does not exist you need `CREATE DATABASE`; if it exists, `RESTORE` permission defaults to sysadmin,
  dbcreator and the database owner (dbo). `db_owner` members do not get it.
- A backup made on another server has no msdb history on the destination, so in SSMS choose Device, not Database.
- Restoring a SQL Server 2005 or later database upgrades it automatically.
- Do not restore databases from untrusted sources; run `DBCC CHECKDB` on a non-production server and review the code
  first.

## 3. After the restore (metadata that does not travel)
```sql
-- owner: the login that ran the restore becomes the owner
ALTER AUTHORIZATION ON DATABASE::Sales_Test TO [sa];
-- orphaned users: database users whose SID has no matching login on this server
SELECT dp.name FROM sys.database_principals dp
LEFT JOIN sys.server_principals sp ON dp.sid = sp.sid
WHERE sp.sid IS NULL AND dp.authentication_type_desc = 'INSTANCE';
ALTER USER <user_name> WITH LOGIN = <login_name>;   -- remap
```
`sp_change_users_login` is deprecated; use `ALTER USER ... WITH LOGIN`.

Also re-create outside the database, in master and msdb on the destination: logins, server-level triggers, linked
servers, credentials (used by Agent proxy accounts), server-level event notifications and explicit Service Broker
routes. A certificate or asymmetric key that carries server-level permissions must be re-created in master and mapped
to a login. An encrypted database cannot be restored without the certificate or asymmetric key that protects it.

## Gotchas
- A database restored from production into test may carry PII.
- When a database is attached from another server, `is_broker_enabled` and `is_honor_broker_priority_on` are set to
  OFF; turn them back on with `ALTER DATABASE`.
- Cross-database ownership chaining is disabled by attach and detach operations.

## Verify
`SELECT name, state_desc, SUSER_SNAME(owner_sid) FROM sys.databases WHERE name = 'Sales_Test';` shows ONLINE and the
expected owner; the application logs in successfully with its login.

## Checked
Date: 2026-11-09. Confirmed against the Learn pages "Restore a database to a new location", "RESTORE FILELISTONLY",
"Manage metadata when making a database available on another server" and "Troubleshoot orphaned users": MOVE
behaviour, permissions, encrypted-database requirement, owner behaviour, orphaned-user query and ALTER USER fix,
deprecation of `sp_change_users_login`, master/msdb metadata, certificate-mapped logins, broker defaults, ownership
chaining. Removed (not stated on those pages): `REPLACE` and `VERIFYONLY` remarks, service-account access advice,
compatibility-level and recovery-model commands, `STATS`.
Method: documentation only; no commands were run.
