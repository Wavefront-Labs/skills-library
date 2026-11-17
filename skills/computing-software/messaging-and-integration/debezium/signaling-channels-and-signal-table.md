---
id: computing-software.messaging-and-integration.debezium.signaling-channels-and-signal-table
name: signaling-channels-and-signal-table
category: computing-software
field: messaging-and-integration
product: debezium
tags: [signaling, signal-table, channels, configuration]
level: practitioner
status: docs-checked
description: "Enable Debezium signaling: create the id/type/data signal table, set signal.data.collection and pick source, kafka, jmx or file channels."
sources:
  - https://debezium.io/documentation/reference/stable/configuration/signalling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Signals let you change connector behaviour or trigger actions such as ad hoc snapshots at runtime. Channels are chosen with `signal.enabled.channels`; the `source` channel is on by default because incremental snapshots need it.

Source channel setup:

1. Create a signal table on the source database with exactly the columns `id`, `type`, `data` in that order:

```sql
CREATE TABLE debezium_signal (id VARCHAR(42) PRIMARY KEY, type VARCHAR(32) NOT NULL, data VARCHAR(2048) NULL);
```

2. Make `id` wide enough for your signal ids, or the signal cannot be processed. Grant the connector user `INSERT` on the table.
3. For databases with native CDC such as SQL Server or Db2, enable CDC on the signal table.
4. Set `signal.data.collection` to the case-sensitive fully qualified name, for example `inventory.debezium_signals`.

The table must be unique per connector. You need not add it to `table.include.list`, but if you use `column.include.list` you must include `id`, `type` and `data`.

Qualified name formats: PostgreSQL `schema.table`; MySQL and MariaDB `database.table`; SQL Server and Oracle `database.schema.table`; MongoDB `database.collection`.

Other channels:

- `kafka`: set `signal.kafka.topic`. The message key must equal `topic.prefix`; the value is JSON with `type` and `data`.
- `jmx`: add `jmx` and enable the MBean server; use MBean `debezium.<connector-type>.management.signals.<server>` with parameters id, type, data.
- `file`: default file `file-signals.txt` on the classpath root; change with `signal.file`.

Gotcha: except for the source channel, signaling channels have no retry policy; verify results, for example via notifications.

## Checked

2026-11-08. Confirmed against the Debezium page configuration/signalling, read in full: channels and the default source channel, signal table columns and order, id width warning, INSERT privilege, CDC on the signal table, case-sensitive qualified name formats, Kafka key rule, JMX MBean, file channel default and the no-retry note. Nothing removed.

Method: documentation only; no commands were run.
