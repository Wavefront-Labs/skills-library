---
id: computing-software.messaging-and-integration.debezium.postgresql-slot-drop-and-retry-properties
name: postgresql-slot-drop-and-retry-properties
category: computing-software
field: messaging-and-integration
product: debezium
tags: [postgresql, slot-drop-on-stop, retries, status-updates]
level: practitioner
status: docs-checked
description: "Know the defaults for slot.drop.on.stop, slot.max.retries, status.update.interval.ms and xmin tracking."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Properties that govern the replication connection:

- `slot.drop.on.stop` (default `false`): when `true`, the slot is dropped on a graceful stop. By default the slot persists so a restart resumes where it left off. Use `true` only in tests and development; dropping the slot lets PostgreSQL discard WAL, so the next start snapshots again or relies on offsets in the Kafka Connect offsets topic.
- `slot.max.retries` (default `6`): maximum consecutive attempts to connect to the slot.
- `slot.retry.delay.ms`: wait between those attempts.
- `status.update.interval.ms` (default `10000`): how often replication status is sent to the server, and how often the connection is checked for death after a server shutdown.
- `xmin.fetch.interval.ms` (default `0`): how often the slot XMIN is read. XMIN is the lower bound where a new slot could start. `0` disables tracking.
- `lsn.flush.mode` (default `connector`): `connector` flushes after processing; `manual` leaves flushing to your own mechanism and can exhaust disk if you forget; it replaces the deprecated `flush.lsn.source`.

```json
"slot.drop.on.stop": "false",
"slot.max.retries": "6",
"status.update.interval.ms": "10000"
```

Gotcha: with `slot.drop.on.stop=false` the slot remains after the connector stops, so a retired connector leaves its slot on the server.

Check: query the `pg_replication_slots` view while the connector runs and confirm the slot is active.

## Checked

2026-11-03. Page used: the Debezium postgresql connector reference, https://debezium.io/documentation/reference/stable/connectors/postgresql.html.
Confirmed against it: slot.drop.on.stop, slot.max.retries, slot.retry.delay.ms, status.update.interval.ms, xmin.fetch.interval.ms, lsn.flush.mode.
Removed or reworded: the pg_drop_replication_slot command and the active = t form.
Method: documentation only; no commands were run.
