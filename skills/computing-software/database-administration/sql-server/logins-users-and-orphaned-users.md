---
id: computing-software.database-administration.sql-server.logins-users-and-orphaned-users
name: logins-users-and-orphaned-users
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, sql-server-security, sql-logins, orphaned-users, contained-database-users, sid-mismatch, alter-user-with-login, windows-authentication]
level: practitioner
status: docs-checked
description: "Understand SQL Server logins vs database users, fix orphaned users after a restore to another server, and use contained users so databases move with their logins."
sources:
  - https://learn.microsoft.com/en-us/sql/sql-server/failover-clusters/troubleshoot-orphaned-users-sql-server
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/contained-database-users-making-your-database-portable
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logins, users and orphaned users

**Goal:** after restoring or failing a database over to another instance, every
application can still log in.

## The model
- **Login**: server-level principal (SQL auth with password, or Windows/Entra
  identity), stored in `master`, identified by a SID.
- **Database user**: database-level principal, mapped to a login **by SID**.
A database moved to another server where the login does not exist leaves its users orphaned: the user's SID does not match any login. See the Troubleshoot orphaned users page.

## Find orphans
```sql
-- connect to the user database and compare the SIDs in sys.database_principals
-- with the logins on the server; the Troubleshoot orphaned users page has the query
USE appdb;
SELECT name, type_desc, sid FROM sys.database_principals;
```
## Fix
```sql
ALTER USER app_user WITH LOGIN = app_user;    -- remaps the user to the login (replaces the deprecated sp_change_users_login)
```

## Contained database users
```sql
EXEC sp_configure 'contained database authentication', 1; RECONFIGURE;
ALTER DATABASE appdb SET CONTAINMENT = PARTIAL;
USE appdb; CREATE USER app_user WITH PASSWORD = '<secret>';
```
A contained user authenticates inside the database, which makes the database portable between instances. Set the containment option when there are no active connections to the database.

## Verify
No orphaned users remain on every instance; a test login from each app host succeeds after a failover.

## Checked

2026-10-28. Confirmed against Microsoft Learn (Troubleshoot orphaned users, contained database users): orphaned users arise when a database moves to a server without the login, SIDs in sys.database_principals are compared to logins, ALTER USER ... WITH LOGIN replaces the deprecated sp_change_users_login, sp_configure 'contained database authentication', SET CONTAINMENT = PARTIAL, no active connections when setting containment. Removed unconfirmed: new-random-SID and error message text, the authentication_type_desc filter, CREATE LOGIN ... SID and password-hash copy, sp_help_revlogin and dbatools, Windows login SID note, Azure SQL norm, shadowing and dbo ownership gotchas.

Method: documentation only; no commands were run.
