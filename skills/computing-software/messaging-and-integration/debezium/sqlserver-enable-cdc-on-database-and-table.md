---
id: computing-software.messaging-and-integration.debezium.sqlserver-enable-cdc-on-database-and-table
name: sqlserver-enable-cdc-on-database-and-table
category: computing-software
field: messaging-and-integration
product: debezium
tags: [sql-server, cdc, sp-cdc-enable-table, setup]
level: practitioner
status: docs-checked
description: "Enable SQL Server CDC with sys.sp_cdc_enable_db and sys.sp_cdc_enable_table before starting the Debezium connector."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/sqlserver.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Debezium reads SQL Server change data capture (CDC) tables, so CDC must be on for the database and for every captured table. The SQL Server Agent must be running.

Database (requires sysadmin membership and being db_owner; you cannot enable CDC on the `master` database):

```sql
USE MyDB
GO
EXEC sys.sp_cdc_enable_db
GO
```

This creates the `cdc` schema, a CDC user, metadata tables and other system objects.

Table (requires db_owner on the database):

```sql
USE MyDB
GO
EXEC sys.sp_cdc_enable_table
@source_schema = N'dbo',
@source_name = N'MyTable',
@role_name = N'MyRole',
@filegroup_name = N'MyDB_CT',
@supports_net_changes = 0
GO
```

Parameters: `@source_name` is the table to capture; `@role_name` is a role whose members get `SELECT` on the captured columns (members of sysadmin or db_owner also have access, and `NULL` means no role gating); `@filegroup_name` must already exist, and the docs say it is best not to place change tables in the same filegroup as source tables.

Enable CDC for every table you want captured, and only user tables are supported. Indexed (materialised) views are not, because a capture instance needs a base table.

Gotcha: a stopped SQL Server Agent means no change data is produced even though CDC is enabled.

Check: run `EXEC sys.sp_cdc_help_change_data_capture` and confirm a row for each captured table.

## Checked

2026-11-08. Confirmed against the Debezium page connectors/sqlserver (read in part: Enabling CDC on the database and on a table): sysadmin and db_owner prerequisites, master database exclusion, cdc schema creation, sys.sp_cdc_enable_db and sys.sp_cdc_enable_table parameters, filegroup advice, role behaviour and sys.sp_cdc_help_change_data_capture. Nothing removed.

Method: documentation only; no commands were run.
