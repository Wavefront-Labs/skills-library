---
id: computing-software.messaging-and-integration.debezium.mysql-gtid-and-supported-topologies
name: mysql-gtid-and-supported-topologies
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mysql, gtid, topology, high-availability]
level: practitioner
status: docs-checked
description: "Choose a supported MySQL topology and enable gtid_mode and enforce_gtid_consistency for replica failover."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mysql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Supported topologies:

- Standalone: binlog must be enabled.
- Primary and replica: the connector follows one server only, since binlog positions differ on each. A replica works if its binlog is enabled. If the followed server fails, restore it before the connector can continue.
- High availability clusters: most use GTIDs, so replicas track all changes from any primary.
- Multi-primary (NDB-style cluster replication): requires GTIDs. The connector can fail over to another multi-primary replica provided it has caught up to every transaction the first one saw.
- Hosted (RDS, Aurora): no global read lock, so snapshots use table-level locks.

Enable GTIDs (MySQL 5.6.5 and later) in the server configuration:

```
gtid_mode=ON
enforce_gtid_consistency=ON
```

Confirm with `show global variables like '%GTID%';`, both should read `ON`. GTIDs are not required by the connector, but they simplify replication and let you confirm primaries and replicas are consistent.

For multi-primary failover with a subset of sources, use `gtid.source.includes`, a comma-separated list of regular expressions matching source UUIDs; only matching GTID ranges are used to locate the position. `gtid.source.excludes` does the opposite.

Gotcha: without GTIDs, a connector pointed at a different server cannot find its position, because binlog file names and offsets are not shared.

Check: run `show global variables like '%GTID%';` on the server the connector will follow and confirm `gtid_mode` and `enforce_gtid_consistency` are `ON`.

## Checked

2026-11-03. Page used: the Debezium mysql connector reference, https://debezium.io/documentation/reference/stable/connectors/mysql.html.
Confirmed against it: supported topologies, GTIDs from MySQL 5.6.5, gtid_mode and enforce_gtid_consistency, gtid.source.includes and excludes.
Removed or reworded: the SELECT @@gtid_mode check.
Method: documentation only; no commands were run.
