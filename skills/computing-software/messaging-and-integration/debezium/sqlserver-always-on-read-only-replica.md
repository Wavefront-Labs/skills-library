---
id: computing-software.messaging-and-integration.debezium.sqlserver-always-on-read-only-replica
name: sqlserver-always-on-read-only-replica
category: computing-software
field: messaging-and-integration
product: debezium
tags: [sql-server, always-on, read-only-replica, application-intent]
level: sme
status: docs-checked
description: "Capture SQL Server changes from an Always On readable secondary with driver.applicationIntent=ReadOnly."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/sqlserver.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The connector can read from an Always On read-only replica. Prerequisites:

- CDC is configured and enabled on the primary node. SQL Server does not support CDC directly on replicas.
- The connector option `driver.applicationIntent` is set to `ReadOnly`, as SQL Server requires.

```json
"driver.applicationIntent": "ReadOnly"
```

When Debezium detects this option, it automatically:

- Sets `snapshot.isolation.mode` to `snapshot`, the only transaction isolation mode supported on read-only replicas.
- Commits the read-only transaction on each iteration of the streaming query loop, so it sees the latest CDC data.

For reference, `snapshot.isolation.mode` defaults to `repeatable_read` elsewhere, and supports `read_uncommitted`, `read_committed`, `repeatable_read`, `snapshot` and `exclusive` (exclusive uses repeatable read but takes an exclusive lock on all captured tables).

Gotcha: `snapshot` is the only isolation mode supported on read-only replicas, so do not override it there.

Check: with CDC enabled on the primary and `driver.applicationIntent` set, confirm the connector streams changes through the replica.

## Checked

2026-11-08. Confirmed against the Debezium page connectors/sqlserver (read in part: the SQL Server Always On section and the snapshot.isolation.mode property). Removed an unsupported startup-log check and the claim that the per-iteration commit is deliberate beyond what the page says.

Method: documentation only; no commands were run.
