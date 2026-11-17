---
id: computing-software.database-administration.vitess.vreplication-troubleshooting-faq
name: vreplication-troubleshooting-faq
category: computing-software
field: database-administration
product: vitess
tags: [vreplication, troubleshooting, io-eof, gtid, binlog-format, vt-filtered, filepos]
level: practitioner
status: docs-checked
description: "Troubleshoot VReplication errors: the vt_filtered MySQL grants, causes of io.EOF, required my.cnf binlog settings, and when --db-flavor=FilePos is acceptable."
sources:
  - https://vitess.io/docs/25.0/reference/vreplication/faq/
  - https://vitess.io/docs/25.0/reference/features/connection-pools/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The VReplication FAQ covers four recurring questions.

Permissions: the `vt_filtered` user (the default for `--db-filtered-user`, used by VReplication on the source vstreamer and target vplayer sides) needs, on `*.*`: SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, FILE, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT and TRIGGER.

`io.EOF` errors are usually a MySQL layer problem; read the source and target vttablet logs to confirm. Possible causes:
- GTID is not enabled: VReplication requires GTID mode on, and `permissible` is not supported.
- Permissions for the vreplication MySQL users, especially `vt_filtered`, are wrong.
- Row-based replication is not enabled (`binlog_format=row`); statement-based is unsupported.
- The MySQL server is down or unreachable.

Settings in `my.cnf`: `log_bin=1`, `binlog_format=ROW`, `binlog_row_image=full`.

If GTIDs cannot be enabled, a workflow may run with `--db-flavor=FilePos` (the pre-5.6 file and position method) as a last resort only, because it is not fault tolerant: any error or failover means discarding the workflow and starting anew.

## Checked

2026-11-08. Read in full on the VReplication FAQ page: grants, io.EOF causes, my.cnf lines and FilePos guidance. The Connection Pools page confirms vt_filtered is the default --db-filtered-user, used by vstreamer and vplayer. Removed the /debug/status and VTAdmin pointer, which neither page states.

Method: documentation only; no commands were run.
