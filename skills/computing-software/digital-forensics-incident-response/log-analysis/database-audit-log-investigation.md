---
id: computing-software.digital-forensics-incident-response.log-analysis.database-audit-log-investigation
name: database-audit-log-investigation
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [database-audit-logs, sql-server-audit, pgaudit, mysql-audit, dfir]
level: practitioner
status: draft
description: "Investigate database audit logs for data theft and tampering: SQL Server Audit, pgaudit, MySQL/MariaDB audit plugins, Oracle unified audit, and what default logs miss."
sources: ["https://learn.microsoft.com/en-us/sql/relational-databases/security/auditing/sql-server-audit-database-engine", "https://github.com/pgaudit/pgaudit", "https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/introduction-to-auditing.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Database audit log investigation

Default database logging rarely records queries. Find out early what auditing existed; if none, rely on connection logs, slow query logs, network evidence and application logs.

## Sources by engine
| Engine | Audit source | Read with |
|---|---|---|
| SQL Server | SQL Server Audit (`.sqlaudit` files, Windows Security/Application log); default trace (schema changes, logins); error log (failed logins) | `SELECT * FROM sys.fn_get_audit_file('<dir>\*.sqlaudit', DEFAULT, DEFAULT)` |
| PostgreSQL | `log_connections`, `log_statement`, pgaudit (`pgaudit.log = 'read,write,ddl,role'`) | csvlog / jsonlog in `log_directory` |
| MySQL / MariaDB | Enterprise Audit, Percona/MariaDB audit plugin (`server_audit`), general log (heavy), binlog (writes) | `mysqlbinlog --base64-output=decode-rows -vv` |
| Oracle | Unified Auditing (`UNIFIED_AUDIT_TRAIL`), listener log | `SELECT event_timestamp, dbusername, action_name, object_name, sql_text FROM unified_audit_trail` |
| Cloud (RDS, Azure SQL, Cloud SQL) | Engine audit exported to CloudWatch / Log Analytics / Cloud Logging | Provider console / queries |

## What to look for
- Bulk reads of sensitive tables (`SELECT * FROM customers`) by unusual principals or from new client hosts / applications (`application_name`, `client_net_address`).
- `BACKUP DATABASE ... TO DISK/URL`, `bcp`, `COPY ... TO PROGRAM`, `SELECT ... INTO OUTFILE`: export paths.
- Privilege changes: `CREATE LOGIN`, `ALTER ROLE ... ADD MEMBER sysadmin`, `GRANT`.
- Code execution: `xp_cmdshell` enabled via `sp_configure`, `COPY FROM PROGRAM`, UDF loads.
- Audit tampering: `ALTER SERVER AUDIT ... STATE = OFF`, pgaudit settings changed, `SET sql_log_bin=0`.

## Gotchas
- Binlogs / transaction logs show writes and deletes even without auditing; reads leave no trace there.
- Application service accounts make every user's query look the same; correlate with app logs for the real user.

## Verify
Any claimed data access names the principal, client host, objects and row counts (or states the audit gap).
