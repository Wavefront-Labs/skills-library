---
id: computing-software.messaging-and-integration.debezium.sqlserver-no-maximum-lsn-and-agent-status
name: sqlserver-no-maximum-lsn-and-agent-status
category: computing-software
field: messaging-and-integration
product: debezium
tags: [sql-server, agent, lsn, troubleshooting]
level: advanced
status: docs-checked
description: "Diagnose the No maximum LSN recorded error and check SQL Server Agent status without granting VIEW SERVER STATE."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/sqlserver.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The connector cannot stream when the database has no recorded maximum LSN. Documented causes:

- The SQL Server Agent is not running. This is the only true error.
- No changes yet exist in the change table.
- Low activity, and the CDC cleanup job has cleared the CDC tables.

The last two are normal. The connector queries the Agent status to tell them apart and, if the Agent is stopped, logs an ERROR: "No maximum LSN recorded in the database; SQL Server Agent is not running".

To check manually:

```sql
SELECT CASE WHEN dss.[status]=4 THEN 1 ELSE 0 END AS isRunning
FROM [#db].sys.dm_server_services dss
WHERE dss.[servicename] LIKE N'SQL Server Agent (%';
```

That query needs `VIEW SERVER STATE`, an instance-wide permission that exposes every database on the instance. To avoid granting it, set the connector property `database.sqlserver.agent.status.query` to a custom query that calls your own function:

```json
"database.sqlserver.agent.status.query": "SELECT [#db].func_is_sql_server_agent_running()"
```

`[#db]` is a placeholder for the database name. The function must return `true` or `1` if the Agent runs and `false` or `0` otherwise. Define it so it runs with elevated rights internally, so the connector login stays low-privilege.

How streaming works: for each capture table the connector reads changes between the last stored maximum LSN and the current one, sorted by commit LSN then change LSN, and passes both LSNs to Kafka Connect as offsets.

Check: start the Agent service and confirm the error stops appearing.

## Checked

2026-11-08. Confirmed against the Debezium page connectors/sqlserver (read in part: No maximum LSN recorded in the database, Reading the change data tables): the three causes, the ERROR text, the status query, the VIEW SERVER STATE note, database.sqlserver.agent.status.query and LSN ordering. Nothing removed.

Method: documentation only; no commands were run.
