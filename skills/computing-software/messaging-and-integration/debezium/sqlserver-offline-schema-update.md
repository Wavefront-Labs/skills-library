---
id: computing-software.messaging-and-integration.debezium.sqlserver-offline-schema-update
name: sqlserver-offline-schema-update
category: computing-software
field: messaging-and-integration
product: debezium
tags: [sql-server, schema-change, capture-instance, offline]
level: advanced
status: docs-checked
description: "Refresh SQL Server capture tables after a schema change with the safe offline procedure using a new capture instance."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/sqlserver.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Source table changes are not reflected in an existing change table, so after a schema change the connector cannot emit correct events until you create a new capture instance. Debezium cannot do this for you; coordinate with a SQL Server operator with elevated privileges.

Offline procedure, the safest option:

1. Suspend the application writing to the database.
2. Wait for the connector to stream all pending change records.
3. Stop the connector.
4. Apply all schema changes to the source table.
5. Create a new capture table with `sys.sp_cdc_enable_table` using a unique `@capture_instance`.
6. Resume the application.
7. Start the connector.
8. After it streams from the new instance, drop the old one with `sys.sp_cdc_disable_table` and `@capture_instance` set to the old name.

```sql
EXEC sys.sp_cdc_enable_table @source_schema='dbo', @source_name='customers',
  @role_name=NULL, @supports_net_changes=0, @capture_instance='dbo_customers_v2';
```

Rules from the docs:

- Finish the whole process before a second schema update on the same table; put all DDL in a single batch.
- SQL Server rejects renaming a column or changing a type on a CDC table.
- Changing NULL to NOT NULL, or back, is not reflected until you create a new capture instance; events keep the old optional flag.
- After `sp_rename`, events keep the old table name until the connector restarts.

Offline updates may not fit high-availability systems; see sqlserver-online-schema-update.

Check: after the drop, confirm only one capture instance remains per table.

## Checked

2026-11-08. Confirmed against the Debezium page connectors/sqlserver (read in part: Database schema evolution and Offline schema updates): the eight-step procedure, unique capture instance, sys.sp_cdc_disable_table, single-batch DDL advice, unsupported column rename and type change, NULL/NOT NULL caveat and sp_rename behaviour. Nothing removed.

Method: documentation only; no commands were run.
