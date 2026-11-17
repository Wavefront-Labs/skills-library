---
id: computing-software.messaging-and-integration.debezium.postgresql-multiple-connectors-unique-slots
name: postgresql-multiple-connectors-unique-slots
category: computing-software
field: messaging-and-integration
product: debezium
tags: [postgresql, slot-name, multiple-connectors, publication]
level: practitioner
status: docs-checked
description: "Give every Debezium PostgreSQL connector its own slot.name and publication.name to avoid silent data loss."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A replication slot has one LSN pointer and emits each change only once. If two connectors share a slot, PostgreSQL delivers each event to only one of them. The other never sees it, and PostgreSQL gives no warning, so the loss is silent.

Set distinct values per connector instance:

```json
"slot.name": "orders_slot",
"publication.name": "orders_publication"
```

Rules from the docs when several connectors capture from the same PostgreSQL server:

- Unique `slot.name` per connector, always.
- Unique `publication.name` per connector is preferred. Connectors can share a publication only if they intentionally watch the identical table set, and they still need separate slots.
- Create manual slots with `pg_create_logical_replication_slot('slot_name', 'plugin_name')` when you want control.

See postgresql-wal-disk-growth-and-heartbeats for WAL retention.

Check: `SELECT slot_name, active FROM pg_replication_slots;` should show one active slot per running connector.

## Checked

2026-11-03. Page used: the Debezium postgresql connector reference, https://debezium.io/documentation/reference/stable/connectors/postgresql.html.
Confirmed against it: one LSN per slot, silent data loss when sharing, unique slot and publication names, shared publications only for identical table sets, manual slot creation.
Removed or reworded: raising max_replication_slots and max_wal_senders, WAL multiplication, per-connector heartbeats, the copied-JSON gotcha.
Method: documentation only; no commands were run.
