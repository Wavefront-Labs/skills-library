---
id: computing-software.database-administration.postgresql.pgaudit-audit-logging
name: pgaudit-audit-logging
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pgaudit, audit-logging, compliance, session-audit, object-audit, security]
level: practitioner
status: docs-checked
description: "Install and tune pgAudit for session and object audit logging in PostgreSQL, keep log volume under control, and ship audit records off the host."
sources:
  - https://github.com/pgaudit/pgaudit
  - https://www.postgresql.org/docs/current/runtime-config-logging.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Session and object audit logging with pgAudit

## Install
```bash
# install the pgaudit package for your PostgreSQL major version, or build with PGXS (see the README)
```
```ini
# postgresql.conf (restart)
shared_preload_libraries = 'pgaudit'     # append to existing list
```
```sql
CREATE EXTENSION pgaudit;                -- per database where you use object audit
```
pgAudit major versions are tied to PostgreSQL majors (pgaudit 17.x for PG17); upgrade it together with the server.

## Session audit (by statement class)
```sql
ALTER SYSTEM SET pgaudit.log = 'ddl, role';     -- classes: read, write, function, role, ddl, misc, misc_set, all
ALTER SYSTEM SET pgaudit.log_catalog = off;     -- skip noise from psql \d and tools
ALTER SYSTEM SET pgaudit.log_parameter = off;   -- on = bind values in log (sensitive!)
ALTER SYSTEM SET pgaudit.log_relation = on;     -- one line per relation touched
SELECT pg_reload_conf();
ALTER ROLE etl_batch SET pgaudit.log = 'none';  -- exempt a noisy, trusted role
ALTER ROLE dba SET pgaudit.log = 'all';         -- audit everything humans with power do
```
Log line: `AUDIT: SESSION,1,1,DDL,CREATE TABLE,TABLE,public.t,CREATE TABLE t(id int),<not logged>`

## Object audit (by table, via a role's privileges)
```sql
CREATE ROLE auditor NOLOGIN;
ALTER SYSTEM SET pgaudit.role = 'auditor'; SELECT pg_reload_conf();
GRANT SELECT, UPDATE ON payroll TO auditor;     -- any SELECT/UPDATE on payroll by anyone is audited
GRANT SELECT (ssn) ON employees TO auditor;     -- only queries touching ssn
```
Object audit is the way to audit reads of sensitive tables without logging every read.

## Volume and shipping
- `pgaudit.log = 'all'` or `'read'` on a busy OLTP system can produce very large log volume and slow the server. Start with `ddl, role` + object audit on sensitive tables.
- Use `log_destination = 'csvlog'` or `'jsonlog'` and a log shipper (Fluent Bit, Vector) to a store DBAs cannot edit; local logs are not tamper-proof.
- `log_line_prefix` should include `%m %u %d %r %a` so audit lines carry user, db, client.

## Verify
```sql
SHOW pgaudit.log;
CREATE TABLE audit_probe(); DROP TABLE audit_probe;    -- check the log for AUDIT: SESSION lines
```

## Gotchas
- Superusers can `SET pgaudit.log = 'none'` in their session. Audit the setting change itself (`misc_set`) and restrict superuser.
- Statements inside functions are logged with `function` class only if enabled; dynamic SQL in DO blocks is audited as executed statements.

## Checked

2026-10-28. Confirmed against the pgAudit README: pgAudit v17.X supports PostgreSQL 17 (a branch per major version), settings at global, database and role level (ALTER ROLE ... SET), pgaudit.log_catalog, log_parameter, log_relation and pgaudit.role, the MISC_SET class, AUDIT: SESSION log format, PGXS build. Removed: distribution package names and the 10-100x volume figure.

Method: documentation only; no commands were run.
