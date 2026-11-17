---
id: computing-software.database-administration.yugabytedb.ysql-audit-logging-pgaudit
name: ysql-audit-logging-pgaudit
category: computing-software
field: database-administration
product: yugabytedb
tags: [audit-logging, pgaudit, ysql-pg-conf-csv, compliance, pgaudit-log, log-parameter, session-audit]
level: advanced
status: docs-checked
description: "Enable YSQL audit logging with pgaudit through ysql_pg_conf_csv, create the extension, and choose which statement classes, relations and parameters to log."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/secure/audit-logging/audit-logging-ysql.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# YSQL audit logging with pgaudit

YSQL uses the PostgreSQL Audit extension v1.7 and writes audit entries to the YB-TServer logs.

Enable at cluster start with `--ysql_pg_conf_csv` (comma-separated; quote settings that contain commas or quotes):
```
--ysql_pg_conf_csv="log_line_prefix='%m [%p %l %c] %q[%C %R %Z %H] [%r %a %u %d] '","pgaudit.log='all, -misc'",pgaudit.log_parameter=on,pgaudit.log_relation=on,pgaudit.log_catalog=off,suppress_nonpg_logs=on
```
These apply to every user and session after restart; with RF 3 or more a rolling restart works. For one session use `SET pgaudit.log='DDL';`.

Then create the extension once from any node:
```
CREATE EXTENSION IF NOT EXISTS pgaudit;
```

Main options:
- `pgaudit.log`: statement classes READ, WRITE, FUNCTION, ROLE, DDL, MISC, or ALL (default none); prefix with `-` to exclude
- `pgaudit.log_catalog`: log statements on `pg_catalog` (on by default; turn off to cut noise from tools)
- `pgaudit.log_client` and `pgaudit.log_level`: echo to clients for debugging
- `pgaudit.log_parameter`: include bound parameters (off by default)
- `pgaudit.log_relation`: one entry per relation referenced in SELECT or DML

By default the statement text is logged for all selected classes. The documented example log_line_prefix includes the client address, user and database (`%r %a %u %d`) so entries are attributable.

## Checked

2026-11-09: pgaudit v1.7, the `ysql_pg_conf_csv` example, restart behaviour, per-session `SET`, extension creation, and the option descriptions and defaults confirmed against the YugabyteDB YSQL audit logging page (yugabyte-db docs audit-logging-ysql.md, read in full). Corrected the `pgaudit.log_catalog` description (default is on) and softened the log_line_prefix advice to what the page shows.

Method: docs-checked 2026-11-09 against yugabyte-db docs secure/audit-logging/audit-logging-ysql.md
