---
id: computing-software.messaging-and-integration.debezium.mysql-failure-recovery-and-purged-binlog
name: mysql-failure-recovery-and-purged-binlog
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mysql, failure, at-least-once, binlog-purge]
level: advanced
status: docs-checked
description: "Know how the MySQL connector behaves on outages, crashes and purged binlogs, and how to deduplicate."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mysql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Debezium gives exactly-once delivery in normal operation but at-least-once during fault recovery, so consumers must tolerate duplicates.

Documented behaviours:

- Invalid configuration, no connection, or a restart position that MySQL no longer retains: the connector fails at start, logs the details, and stops. Fix the cause and restart.
- MySQL unavailable: the connector fails and stops. Against a highly available cluster you can restart immediately; it connects to another server, finds the last transaction and reads that server's binlog from there.
- Kafka Connect crash: tasks resume from the last recorded offset, possibly regenerating events already processed before the crash.
- Kafka unavailable: the connector pauses and resumes where it left off.
- Binlog purged while the connector is stopped: on restart MySQL no longer has the start position, so the connector performs another initial snapshot. If snapshots are disabled it fails with an error.

To detect duplicates, use fields in each event `source` block: origin, the server event time, binlog file name and position.

Prevention: `binlog_expire_logs_seconds` sets automatic binlog removal (default `2592000`, 30 days); keep it longer than any outage you expect.

## Checked

2026-11-08: read the Behavior when things go wrong section and the binlog_expire_logs_seconds row of the shared MariaDB and MySQL partial (shared-mariadb-mysql.adoc) that the cited MySQL connector page includes. Confirmed the delivery guarantees, each fault behaviour, the duplicate-detection fields and the retention default. Removed: the GTID field mention (its snippet was not read), the connector lag advice, the snapshot-flood gotcha and the test Check line.

Method: documentation only; no commands were run.
