---
id: computing-software.messaging-and-integration.debezium.oracle-database-preparation-archivelog-supplemental
name: oracle-database-preparation-archivelog-supplemental
category: computing-software
field: messaging-and-integration
product: debezium
tags: [oracle, archivelog, supplemental-logging, setup]
level: advanced
status: docs-checked
description: "Prepare Oracle with archive log mode and supplemental logging for Debezium LogMiner, including the Amazon RDS commands."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/oracle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Debezium for Oracle needs the database in archive log mode with supplemental logging.

Archive log mode (self-managed), as SYSDBA:

```sql
alter system set db_recovery_file_dest_size = 10G;
alter system set db_recovery_file_dest = '/path/to/recovery_area' scope=spfile;
shutdown immediate
startup mount
alter database archivelog;
alter database open;
archive log list
```

The output should read "Database log mode: Archive Mode".

Amazon RDS does not allow these commands or SYSDBA login. Check backups are enabled with `SELECT LOG_MODE FROM V$DATABASE;` (must be `ARCHIVELOG`; reboot if not), then:

```sql
exec rdsadmin.rdsadmin_util.set_configuration('archivelog retention hours',24);
exec rdsadmin.rdsadmin_util.alter_supplemental_logging('ADD');
```

Minimal supplemental logging at database level:

```sql
ALTER DATABASE ADD SUPPLEMENTAL LOG DATA;
```

To capture the before state, also add table-level logging:

```sql
ALTER TABLE inventory.customers ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS;
```

All-column logging increases redo volume, so apply it selectively rather than database-wide.

Capacity: redo logs must be able to store the data dictionary, which grows with the number of tables and columns. Ask your DBA whether log capacity needs increasing.

Check: run `SELECT LOG_MODE FROM V$DATABASE;` and expect `ARCHIVELOG` before deploying the connector.

## Checked

2026-11-08: read the Preparing the database and Redo log sizing sections of the Debezium Oracle connector reference (raw AsciiDoc source of the cited page, connectors/oracle.adoc). Confirmed the archive log mode commands, the RDS commands and retention value, the table-level and database-level supplemental logging statements, the redo volume warning and the data dictionary capacity note. Removed: the SUPPLEMENTAL_LOG_DATA_MIN check, which the page does not mention.

Method: documentation only; no commands were run.
