---
id: computing-software.database-administration.mysql.audit-logging
name: audit-logging
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-audit-log, audit-log-plugin, percona-audit-log, audit-log-filter, compliance, security]
level: practitioner
status: draft
description: "Audit MySQL activity with MySQL Enterprise Audit filters or the Percona/MariaDB audit plugins: install, filter by user and event class, rotate and ship logs."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/audit-log.html
  - https://dev.mysql.com/doc/refman/8.4/en/audit-log-filtering.html
  - https://docs.percona.com/percona-server/8.4/audit-log-filter-overview.html
  - https://mariadb.com/kb/en/mariadb-audit-plugin/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Audit logging

Community MySQL has no audit plugin. Options: MySQL Enterprise Audit (commercial), Percona Server's audit log filter component (free, uses the same JSON filter functions as Enterprise in Percona 8.4), MariaDB's `server_audit` plugin (also loadable in some MySQL versions).

## MySQL Enterprise Audit / Percona audit_log_filter
Install (Enterprise: run the shipped script):
```bash
mysql -u root -p < <MYSQL_SHARE_DIR>/audit_log_filter_linux_install.sql
```
Define filters in JSON and assign them to accounts:
```sql
-- log connections and DDL/DCL for everyone
SELECT audit_log_filter_set_filter('conn_ddl', '{"filter": {"class": [
  {"name": "connection"},
  {"name": "general", "event": {"name": "status", "log": {"field": {"name": "general_command.str", "value": "Query"}}}}
]}}');
SELECT audit_log_filter_set_user('%', 'conn_ddl');           -- default for all accounts
-- log everything for DBAs
SELECT audit_log_filter_set_filter('log_all', '{"filter": {"log": true}}');
SELECT audit_log_filter_set_user('dba_alice@%', 'log_all');
SELECT * FROM mysql.audit_log_filter; SELECT * FROM mysql.audit_log_user;
```
Settings: `audit_log_format = JSON`, `audit_log_rotate_on_size = 1G`, `audit_log_max_size`/`audit_log_prune_seconds` for retention, `audit_log_encryption = AES` and `audit_log_compression = GZIP` available. Read with `audit_log_read()` or directly from the files.

## MariaDB server_audit
```ini
plugin_load_add = server_audit
server_audit_logging = ON
server_audit_events = CONNECT,QUERY_DDL,QUERY_DCL
server_audit_excl_users = monitoring
server_audit_file_rotate_size = 1000000000
server_audit_file_rotations = 10
```

## Policy that works
- Always: connections (incl. failures), DDL, DCL (GRANT/CREATE USER), changes to audit settings.
- For sensitive tables: table-access events filtered to those tables, not every SELECT.
- Ship logs off-host promptly (Filebeat/Fluent Bit) to storage the DBAs cannot alter.

## Verify
Log in with a wrong password and run a `CREATE TABLE`; confirm both appear in the audit file with user, host and timestamp.

## Gotchas
- Logging every query on a busy OLTP server costs real throughput and disk; measure.
- `SUPER`/`AUDIT_ADMIN` holders can change filters; audit filter changes and restrict those privileges.
- The general query log is not an audit log (no filtering, huge, easily disabled).
