---
id: computing-software.cybersecurity-defensive.system-hardening.database-audit-logging
name: database-audit-logging
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [database-hardening, database-audit-logging, pgaudit, sql-server-audit, mariadb-audit, privileged-activity-monitoring]
level: advanced
status: docs-checked
description: "Configure database audit logging for logins, privilege changes, DDL and sensitive data access with pgAudit, SQL Server Audit and the MariaDB audit plugin; ship logs to the SIEM."
sources: ["https://github.com/pgaudit/pgaudit", "https://learn.microsoft.com/en-us/sql/relational-databases/security/auditing/sql-server-audit-database-engine", "https://learn.microsoft.com/en-us/sql/t-sql/statements/create-server-audit-transact-sql", "https://docs.cloud.google.com/sql/docs/postgres/pg-audit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database audit logging

**Goal:** you can answer who logged in, who changed privileges or schema, and who read sensitive tables, with logs the DBA cannot silently erase.

## What to audit
- Successful and failed logins.
- Role/permission changes (GRANT, REVOKE, CREATE/ALTER/DROP USER/ROLE).
- DDL on production schemas.
- DML/SELECT on sensitive tables (cardholder, PII) - scoped, not everything.
- Audit configuration changes themselves.

## PostgreSQL (pgAudit)
pgAudit must be in `shared_preload_libraries` (otherwise no audit logging occurs), and `CREATE EXTENSION pgaudit`
must run before `pgaudit.log` is set (the extension installs event triggers for DDL object details).
```
shared_preload_libraries = 'pgaudit'
pgaudit.log = 'role, ddl'
log_connections = 'receipt,authentication,authorization'
log_disconnections = on
```
In current PostgreSQL `log_connections` takes a comma-separated list (options include `receipt`, `authentication`,
`authorization`, `setup_durations`; default empty, which disables connection logging; failed authentication is
always logged). Check the docs for your server version. `log_disconnections` defaults to off.
- `pgaudit.log` classes: `READ`, `WRITE`, `FUNCTION`, `ROLE` (GRANT, REVOKE, CREATE/ALTER/DROP ROLE), `DDL` (DDL
  not in ROLE), `MISC`, `MISC_SET`, `ALL`; subtract with `-`. Default `none`.
- `pgaudit.log_parameter` defaults to `off`; when on, statement parameters are written to the log.
- Object-level auditing for sensitive tables: create an `auditor` role, grant it the privileges to audit
  (e.g. `GRANT SELECT ON <table> TO auditor;`), set `pgaudit.role = 'auditor'`. Only SELECT, INSERT, UPDATE and DELETE
  are covered; TRUNCATE is not.

## SQL Server Audit
```sql
CREATE SERVER AUDIT Aud TO FILE (FILEPATH = '<AUDIT_DIR>', MAXSIZE = 256 MB) WITH (ON_FAILURE = CONTINUE);
ALTER SERVER AUDIT Aud WITH (STATE = ON);
CREATE SERVER AUDIT SPECIFICATION SrvSpec FOR SERVER AUDIT Aud
  ADD (FAILED_LOGIN_GROUP), ADD (SUCCESSFUL_LOGIN_GROUP), ADD (SERVER_ROLE_MEMBER_CHANGE_GROUP),
  ADD (AUDIT_CHANGE_GROUP), ADD (DATABASE_PERMISSION_CHANGE_GROUP) WITH (STATE = ON);
USE <DATABASE>;
CREATE DATABASE AUDIT SPECIFICATION DbSpec FOR SERVER AUDIT Aud
  ADD (SELECT, UPDATE ON dbo.<TABLE> BY public), ADD (SCHEMA_OBJECT_CHANGE_GROUP) WITH (STATE = ON);
```
- `TO` accepts `FILE`, `APPLICATION_LOG`, `SECURITY_LOG`, `URL`, `EXTERNAL_MONITOR`. Microsoft rates the Windows
  Security log as more secure than the Application log (any authenticated user can write to the latter).
- `ON_FAILURE` takes `CONTINUE`, `SHUTDOWN` or `FAIL_OPERATION`; choose `SHUTDOWN` only if losing audit must stop
  the instance. `MAXSIZE` defaults to `UNLIMITED` (file grows until the disk is full).
- `BY public` audits every user, since every user is in the public role.

## MySQL/MariaDB
MariaDB's `server_audit` plugin selects events with `server_audit_events` (`CONNECT`, `QUERY`, `TABLE`,
`QUERY_DDL`, `QUERY_DML`, `QUERY_DCL`, `QUERY_DML_NO_SELECT`, depending on plugin version). For MySQL itself use
the audit feature your edition provides; read its vendor page.

## Managed cloud
- Cloud SQL for PostgreSQL: set the flag `cloudsql.enable_pgaudit=on` (changing it restarts the instance), run
  `CREATE EXTENSION pgaudit;`, then set `pgaudit.log`. The default for `pgaudit.log` is none.
- RDS for PostgreSQL supports pgAudit; AWS recommends monitoring storage consumption because of the detail logged.
- Azure SQL: use the service's auditing feature to a log destination.

## Shipping and protection
Forward to SIEM in near real time; DBAs must not have delete rights on the SIEM copy. Alert on: audit stopped, new sysadmin/superuser, bulk SELECT on sensitive tables, logins from unusual hosts.

## Gotchas
- Auditing all statements on busy OLTP systems kills performance and storage; scope it.
- Parameter logging may write sensitive values (passwords, PANs) into logs.

## Verify
- [ ] A test GRANT appears in the SIEM within minutes with user and host.
- [ ] Disabling the audit triggers an alert.

## Checked
2026-10-31. Confirmed in the pgAudit README (preload requirement, `CREATE EXTENSION` ordering, log classes, defaults,
object audit via `pgaudit.role`, TRUNCATE exclusion), PostgreSQL logging docs (`log_connections`,
`log_disconnections`), SQL Server Audit pages (targets, `ON_FAILURE`, `MAXSIZE` default, action group names,
`BY public` example), the MariaDB audit plugin page (event names), the Cloud SQL pgAudit page and the RDS
pgAudit page. Removed: `rds.log_retention`, named MySQL commercial/Percona plugins, the Azure Log Analytics
specifics, and the unverified performance and tamper claims beyond the Microsoft Security-log note.
Method: documentation only; no commands were run.
