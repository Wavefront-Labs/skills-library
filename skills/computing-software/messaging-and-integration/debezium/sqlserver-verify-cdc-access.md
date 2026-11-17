---
id: computing-software.messaging-and-integration.debezium.sqlserver-verify-cdc-access
name: sqlserver-verify-cdc-access
category: computing-software
field: messaging-and-integration
product: debezium
tags: [sql-server, cdc, permissions, verification]
level: practitioner
status: docs-checked
description: "Verify the Debezium login can see the CDC capture instance with sys.sp_cdc_help_change_data_capture."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/sqlserver.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Before blaming the connector, confirm the database user can see the CDC configuration. Run, as the connector user:

```sql
USE MyDB;
GO
EXEC sys.sp_cdc_help_change_data_capture
GO
```

The procedure returns configuration for each CDC-enabled table in the database that contains change data the caller is authorised to access. Queries should not return empty results.

What the caller needs, per the docs:

- `SELECT` permission on all captured columns of the capture instance.
- Membership in any gating roles defined for the table (the `@role_name` given to `sys.sp_cdc_enable_table`).
- Members of `db_owner` can view all defined capture instances.

If the result is empty, verify the user can access both the capture instance and the CDC tables.

Related behaviour: the connector detects whether CDC is enabled or disabled for included source tables and adjusts its behaviour accordingly.

Gotcha: setting `@role_name` to `NULL` removes the gating role entirely, so any user with table access can read the change data. Use that only deliberately.

Check: the result must contain a capture instance row for each table in `table.include.list`.

## Checked

2026-11-08. Confirmed against the Debezium page connectors/sqlserver (read in part: Verifying that the user has access to the CDC table, and the CDC detection note). Removed the advice to add the user to the gating role, which the page does not state.

Method: documentation only; no commands were run.
