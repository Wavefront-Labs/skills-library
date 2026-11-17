---
id: computing-software.messaging-and-integration.debezium.outbox-event-router-table-and-config
name: outbox-event-router-table-and-config
category: computing-software
field: messaging-and-integration
product: debezium
tags: [outbox, smt, event-router, transactional-outbox]
level: practitioner
status: docs-checked
description: "Set up the Debezium outbox event router SMT with the default outbox table columns, topic routing and update handling."
sources:
  - https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The outbox pattern writes events to an outbox table in the same transaction as your data; Debezium reads that table and the `EventRouter` SMT turns rows into clean messages.

```
transforms=outbox
transforms.outbox.type=io.debezium.transforms.outbox.EventRouter
```

Default outbox table columns:

- `id` (uuid): unique event id, emitted as a message header; set another column with `table.field.event.id`.
- `aggregatetype`: becomes part of the topic name.
- `aggregateid`: the message key; keeps ordering per Kafka partition (`table.field.event.key`).
- `type`: event type.
- `payload`: the message value (`table.field.event.payload`), default JSON.

Routing: `route.by.field` (default `aggregatetype`) and `route.topic.replacement` (default `outbox.event.${routedByValue}`). A row with `aggregatetype` `customers` goes to `outbox.event.customers`. `route.topic.regex` defaults to `(?<routedByValue>.*)`. `route.tombstone.on.empty.payload` defaults to `false`.

The outbox table behaves as a queue. `table.op.invalid.behavior` (default `warn`) handles UPDATEs: `warn` and `error` log and continue to the next record, `fatal` stops the connector. DELETE operations are filtered out automatically.

Apply the SMT only to outbox events, because connectors also emit heartbeat, tombstone and metadata messages with a different structure. Use an SMT predicate, or the `route.topic.regex` option.

`table.field.event.timestamp` replaces the default Debezium timestamp, and `table.field.event.schema.version` sets the schema version.

Gotcha: the outbox table is treated as a queue; UPDATEs are not allowed (see `table.op.invalid.behavior`), while the SMT filters out DELETE operations.

## Checked

2026-11-08. Confirmed against the Debezium page transformations/outbox-event-router, read in full: default table columns, route.by.field, route.topic.replacement and regex defaults, table.op.invalid.behavior, timestamp and schema version options and selective application. Removed the scheduled-job advice, which the page does not give.

Method: documentation only; no commands were run.
