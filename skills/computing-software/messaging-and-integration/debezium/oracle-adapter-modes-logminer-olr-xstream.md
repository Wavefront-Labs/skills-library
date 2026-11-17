---
id: computing-software.messaging-and-integration.debezium.oracle-adapter-modes-logminer-olr-xstream
name: oracle-adapter-modes-logminer-olr-xstream
category: computing-software
field: messaging-and-integration
product: debezium
tags: [oracle, logminer, adapter, openlogreplicator]
level: practitioner
status: docs-checked
description: "Choose database.connection.adapter for the Debezium Oracle connector: logminer, logminer_unbuffered, olr or xstream."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/oracle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set `database.connection.adapter` to choose how changes are read:

- `logminer` (default): native Oracle LogMiner API with connector-level buffering. This is uncommitted changes mode. The connector receives both committed and in-flight changes, and buffers until commit or rollback because Oracle interleaves transactions. It minimises load on the database, but you must give the connector enough memory for the largest transactions and highest concurrency.
- `logminer_unbuffered`: LogMiner with database-level buffering (committed changes mode). The connector receives only committed events and forwards them with no internal buffer, needing far less connector memory. The burden moves to the database; large transactions can exceed PGA memory and cause `PGA_AGGREGATE_LIMIT` errors. Recommended only if every transaction fits in PGA.
- `olr`: OpenLogReplicator, an open-source reader of redo and archive logs with minimal database impact.
- `xstream`: Oracle XStream, a commercial component of Oracle GoldenGate.

```json
"database.connection.adapter": "logminer"
```

Buffer-related properties for `logminer`: `log.mining.transaction.retention.ms` (default `0`) keeps transactions until commit or rollback when `0`; a positive value discards transactions older than that between log switches. Avoid long-running transactions because DML is buffered until the end.

Gotcha: `logminer_unbuffered` looks cheaper from the connector side but can overload the database; test with your biggest batch job.

## Checked

2026-11-08: read the LogMiner, OpenLogReplicator and XStream adapter descriptions and the database.connection.adapter and log.mining.transaction.retention.ms property rows in the Debezium Oracle connector reference (raw AsciiDoc source of the cited page, connectors/oracle.adoc). Confirmed all four adapter values, the default, the buffering modes, PGA_AGGREGATE_LIMIT and the retention behaviour. Removed: the unsupported startup-log Check line.

Method: documentation only; no commands were run.
