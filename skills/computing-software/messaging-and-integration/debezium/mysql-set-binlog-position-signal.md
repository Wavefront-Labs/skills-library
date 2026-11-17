---
id: computing-software.messaging-and-integration.debezium.mysql-set-binlog-position-signal
name: mysql-set-binlog-position-signal
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mysql, signal, binlog-position, recovery]
level: sme
status: docs-checked
description: "Reposition the MySQL connector at runtime with a set-binlog-position signal using a binlog file and position or a GTID set."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mysql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `set-binlog-position` signal tells the connector where to start reading the binlog. A later position skips events; an earlier one replays and emits duplicates. Use it for disaster recovery, skipping corrupted data, avoiding a replay after a database refresh from backup, partial replication or testing.

Prerequisites: a configured signaling channel, a signal data collection on the source database, and `heartbeat.interval.ms` set so offset changes persist.

Payload without GTIDs (file name must match the pattern like `mysql-bin.000001`; position is a non-negative integer):

```json
{"binlog_filename": "mysql-bin.000003", "binlog_position": 1234}
```

With GTIDs (MySQL UUID-based; MariaDB uses `0-1-100` style):

```json
{"gtid_set": "3E11FA47-71CA-11E1-9E33-C80AA9429562:1-100"}
```

You cannot mix the two in one signal. Send it through the source channel:

```sql
INSERT INTO debezium_signal (id, type, data) VALUES (
 'set-position-001', 'set-binlog-position',
 '{"binlog_filename": "mysql-bin.000003", "binlog_position": 1234}');
```

Then restart the connector so streaming begins from the new position.

Gotcha: a later position means the connector does not capture or stream the skipped range; an earlier one replays and emits duplicates.

Check: after restart, confirm the first event's `source` block shows your target binlog file and position.

## Checked

2026-11-03. Page used: the Debezium mysql connector reference, https://debezium.io/documentation/reference/stable/connectors/mysql.html.
Confirmed against it: signal purpose and uses, prerequisites, both payload formats and naming patterns, MariaDB GTID format, the source-channel INSERT, restart step.
Removed or reworded: the incremental-snapshot advice and the source.file / source.pos field names.
Method: documentation only; no commands were run.
