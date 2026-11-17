---
id: computing-software.messaging-and-integration.debezium.mongodb-connection-heartbeat-and-naming-properties
name: mongodb-connection-heartbeat-and-naming-properties
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mongodb, heartbeat, schema-name-adjustment, cursor]
level: practitioner
status: docs-checked
description: "Set heartbeat.interval.ms, cursor.max.await.time.ms and schema.name.adjustment.mode on the MongoDB connector."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mongodb.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Operational properties and documented defaults:

- `heartbeat.interval.ms` (default `0`, off): interval in milliseconds for messages sent to a heartbeat topic. They show the connector is still receiving events, and are particularly useful when only records in non-captured collections change for a long time. Without them, offsets do not advance and the oplog position can age out.
- `cursor.max.await.time.ms` (default `0`): the longest the change stream cursor waits for the server to produce a result before causing an execution timeout exception. `0` uses the server or driver default.
- `schema.name.adjustment.mode` (default `none`): `none` does no adjustment; `avro` replaces characters that Avro type names cannot use with underscores; `avro_unicode` replaces underscores and invalid characters with `_uxxxx` unicode escapes. The underscore acts as an escape sequence, like a backslash in Java.
- `snapshot.mode` (default `initial`): `always`, `initial`, `initial_only`, `no_data`, `when_needed`, `configuration_based` or `custom`, as for other connectors.

```json
"heartbeat.interval.ms": "30000",
"schema.name.adjustment.mode": "avro"
```

Use `avro` or `avro_unicode` when collection names contain characters that are not valid in Avro type names.

Check: list the heartbeat topic and confirm messages arrive at the configured interval.

## Checked

2026-11-03. Page used: the Debezium mongodb connector reference, https://debezium.io/documentation/reference/stable/connectors/mongodb.html.
Confirmed against it: heartbeat.interval.ms default and purpose, cursor.max.await.time.ms, schema.name.adjustment.mode values and the underscore escape note, snapshot.mode default.
Removed or reworded: the name-collision gotcha and the hyphen example.
Method: documentation only; no commands were run.
