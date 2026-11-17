---
id: computing-software.messaging-and-integration.debezium.sqlserver-online-schema-update
name: sqlserver-online-schema-update
category: computing-software
field: messaging-and-integration
product: debezium
tags: [sql-server, schema-change, capture-instance, online]
level: advanced
status: docs-checked
description: "Update SQL Server capture instances without downtime and understand the processing gap trade-off."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/sqlserver.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Online schema updates need no application or connector downtime, and are simpler than the offline route. The cost is a potential gap: after you alter the source table but before the new capture instance exists, changes still land in the old change table with the old structure. Added columns will be missing from those events. If your application cannot tolerate that, use the offline procedure.

Steps:

1. Apply all schema changes to the source table.
2. Create a new capture table with `sys.sp_cdc_enable_table` and a unique `@capture_instance`.
3. After Debezium streams from the new table, drop the old one with `sys.sp_cdc_disable_table` and `@capture_instance` naming the old instance.

The connector emits a notification after it finishes reading the old capture instance (see the notifications docs).

Example from the docs, adding a column then creating version two:

```sql
ALTER TABLE customers ADD phone_number VARCHAR(32);
EXEC sys.sp_cdc_enable_table @source_schema = 'dbo', @source_name = 'customers',
  @role_name = NULL, @supports_net_changes = 0, @capture_instance = 'dbo_customers_v2';
```

Constraints:

- You must be a SQL Server operator with elevated privileges.
- Complete the whole update before applying another to the same table.
- Do not change schema while an incremental snapshot is running; it is unsupported.

Gotcha: rows inserted between the ALTER and the new instance are the ones that lack the new field. Minimise that window by running both statements back to back.

Check: insert a row using the new column and confirm the event carries it.

## Checked

2026-11-08. Confirmed against the Debezium page connectors/sqlserver (read in part: Online schema updates and its worked example, the incremental snapshot schema change note): steps, processing gap, notification after reading the old instance and the example statements. Nothing removed.

Method: documentation only; no commands were run.
