---
id: computing-software.database-administration.sql-server.sql-server-audit
name: sql-server-audit
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, azure-sql, sql-server-security, sql-server-audit, server-audit-specification, database-audit-specification, fn-get-audit-file, compliance, on-failure-shutdown]
level: practitioner
status: docs-checked
description: "Configure SQL Server Audit with server and database audit specifications, read the .sqlaudit files, and choose safe failure behaviour."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/auditing/sql-server-audit-database-engine
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/auditing/sql-server-audit-action-groups-and-actions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Server Audit

**Goal:** a tamper-evident record of logins, permission changes and access to
sensitive tables, built on Extended Events, without hurting the workload.

## Pieces
1. **Server audit** (in `master`): the target - file, Windows Security log or
   Application log - plus queue delay and failure behaviour.
2. **Server audit specification**: server-level action groups.
3. **Database audit specification** (per database): database action groups and
   object-level actions. All editions support server-level audits; database-level audits are in all editions from SQL Server 2016 SP1.
   One server audit specification and one database audit specification per database can belong to an audit. Audits are created disabled.
   `tempdb` and temporary tables are not audited.

## Example
```sql
USE master;
CREATE SERVER AUDIT Audit_Main
  TO FILE (FILEPATH = '<AUDIT_DIR>\', MAXSIZE = 256 MB, MAX_ROLLOVER_FILES = 50)
  WITH (QUEUE_DELAY = 1000, ON_FAILURE = CONTINUE);
ALTER SERVER AUDIT Audit_Main WITH (STATE = ON);

CREATE SERVER AUDIT SPECIFICATION Audit_Server_Spec FOR SERVER AUDIT Audit_Main
  ADD (FAILED_LOGIN_GROUP), ADD (SUCCESSFUL_LOGIN_GROUP),
  ADD (SERVER_ROLE_MEMBER_CHANGE_GROUP), ADD (SERVER_PERMISSION_CHANGE_GROUP),
  ADD (AUDIT_CHANGE_GROUP), ADD (DATABASE_PERMISSION_CHANGE_GROUP)
  WITH (STATE = ON);

USE appdb;
CREATE DATABASE AUDIT SPECIFICATION Audit_Appdb FOR SERVER AUDIT Audit_Main
  ADD (SELECT ON OBJECT::dbo.payroll BY public),
  ADD (UPDATE ON OBJECT::dbo.payroll BY public),
  ADD (SCHEMA_OBJECT_CHANGE_GROUP)
  WITH (STATE = ON);
```
`BY public` audits every user. Database-level actions (SELECT, UPDATE, INSERT, DELETE, EXECUTE, RECEIVE, REFERENCES) do not apply to columns.
`CREATE SERVER AUDIT` also accepts a `WHERE` predicate (comparisons and AND/OR/NOT on audit fields, up to 3,000 characters) to filter events,
for example `WHERE object_name = 'SensitiveData'`; `QUEUE_DELAY` is in milliseconds (minimum 1000, 0 = synchronous) and
`MAXSIZE` has a 2 MB minimum. Other targets: `APPLICATION_LOG`, `SECURITY_LOG`. Permissions: `ALTER ANY SERVER AUDIT` or `CONTROL SERVER`.

## Read it
```sql
SELECT event_time, action_id, succeeded, server_principal_name, database_name,
       object_name, statement
FROM sys.fn_get_audit_file('<AUDIT_DIR>\Audit_Main*.sqlaudit', DEFAULT, DEFAULT)
WHERE event_time > DATEADD(day, -1, SYSUTCDATETIME());   -- event_time is UTC (datetime2)
```
`fn_get_audit_file` needs a path plus file name pattern (one `*` wildcard allowed), works only for file targets (not application/security log), and needs
`CONTROL SERVER` (2019 and earlier) or `VIEW SERVER SECURITY AUDIT` (2022+). Ship files to a SIEM or a central table regularly.
Microsoft's caution: sysadmins can tamper with any audit component and db_owner with database specifications. Setting the server audit state ON/OFF
is intrinsically audited; create/alter/drop of audit specifications is not, so add `AUDIT_CHANGE_GROUP`. To audit administrators, audit the `dbo` user.
Restrict ACLs on the audit folder and consider reporting from a separate instance.

## Failure behaviour
- `CONTINUE`: keep serving if the target fails (events lost).
- `SHUTDOWN`: the instance stops if it cannot write to the audit target (default is CONTINUE); the login running `CREATE SERVER AUDIT`
  needs the SHUTDOWN permission. If an audit fails at startup the server does not start (use `-f`); starting with `-m` downgrades SHUTDOWN audits to CONTINUE for that session.
- `FAIL_OPERATION`: audited actions fail, others continue.

## Gotchas
- Successful-login auditing on a busy app pool generates huge volume; audit failed
  logins and privileged changes broadly, data access narrowly.
- Security log target needs the service account in the "Generate security audits" policy and the "Audit object access" policy enabled for success and failure;
  the Application log is readable and writable by any authenticated user, so it is less secure.
- Azure SQL Database has its own auditing; Azure SQL Managed Instance supports SQL Server Audit with differences (URL or EXTERNAL_MONITOR targets).
- Transaction-level auditing (`TRANSACTION_GROUP`) collects nothing unless Common Criteria Compliance is enabled (2016 SP2 CU3, 2017 CU4+).
- `FAILED_LOGIN_GROUP` does not apply to Azure SQL Database.

## Verify
- [ ] `sys.dm_server_audit_status` shows the audit started and the file path writable.
- [ ] A test failed login and a permission change appear in `fn_get_audit_file`.
- [ ] Files are collected off-server and retention matches policy.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 pages for SQL Server Audit, Audit action groups and actions, CREATE SERVER AUDIT and sys.fn_get_audit_file (2017-2025).
Confirmed: components and edition availability, action-group and action names used in the example, ON_FAILURE semantics and startup/-m behaviour, WHERE predicate, QUEUE_DELAY and MAXSIZE limits, Security log requirements, `fn_get_audit_file` columns, UTC time, targets and permissions, tamper caution. Removed unconfirmed claims: "2022 adds a WHERE predicate" (the predicate is documented without a 2022 gate), "AUDIT_CHANGE_GROUP always recorded", `az sql server audit-policy`, and the combined multi-action form.
The overview page lists `sys.dm_server_audit_status` as the view for current audit state.
Method: documentation only; no commands were run.
