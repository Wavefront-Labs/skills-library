---
id: computing-software.messaging-and-integration.debezium.mysql-schema-change-events-and-error-modes
name: mysql-schema-change-events-and-error-modes
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mysql, schema-change-topic, error-handling, include-schema-changes]
level: practitioner
status: docs-checked
description: "Use include.schema.changes, event.processing.failure.handling.mode and inconsistent.schema.handling.mode on MySQL."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mysql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The connector can emit DDL events to a consumer-facing schema change topic named exactly as the `topic.prefix` value. Control it with `include.schema.changes`. This is separate from the internal schema history topic, which consumers must not read. Messages carry a payload and optionally the schema.

Failure handling properties (default `fail`):

- `event.processing.failure.handling.mode`: how the connector reacts when processing an event fails, for example on a corrupted event. `fail` raises an exception that reports the event and its position and stops. `warn` logs the event and its position and skips it. `ignore` skips it with no log entry.
- `inconsistent.schema.handling.mode`: how it reacts to binlog events that refer to tables missing from its internal schema, meaning the internal model is out of step with the database. `fail` stops with the event and binlog offset; `warn` logs and skips it; `skip` skips it silently.

```json
"include.schema.changes": "true",
"event.processing.failure.handling.mode": "fail",
"inconsistent.schema.handling.mode": "fail"
```

Another related property: `binlog.buffer.size` (default `0`, buffering off) sets a look-ahead buffer. It matters when the binlog contains uncommitted data later finished by `ROLLBACK`, for example from savepoints or mixing temporary and regular tables in one transaction.

Gotcha: `warn`, `ignore` and `skip` drop events, and the silent ones hide it. Use them only after you understand which events are dropped.

Check: after a DDL change, consume the schema change topic and confirm the statement appears.

## Checked

2026-11-03. Page used: the Debezium mysql connector reference, https://debezium.io/documentation/reference/stable/connectors/mysql.html.
Confirmed against it: schema change topic named from topic.prefix, include.schema.changes, the two failure-handling properties and their modes, binlog.buffer.size and the savepoint case.
Removed or reworded: nothing.
Method: documentation only; no commands were run.
