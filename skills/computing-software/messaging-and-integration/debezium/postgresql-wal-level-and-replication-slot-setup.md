---
id: computing-software.messaging-and-integration.debezium.postgresql-wal-level-and-replication-slot-setup
name: postgresql-wal-level-and-replication-slot-setup
category: computing-software
field: messaging-and-integration
product: debezium
tags: [postgresql, wal, replication-slot, setup]
level: practitioner
status: docs-checked
description: "Configure postgresql.conf for logical decoding and create or auto-create the replication slot Debezium needs."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Debezium reads PostgreSQL through logical decoding, which needs these settings in `postgresql.conf`:

```
wal_level=logical
max_wal_senders=1
max_replication_slots=1
```

`wal_level` selects logical decoding of the write-ahead log, `max_wal_senders` caps the processes that stream WAL, and `max_replication_slots` caps slots. Raise the last two when you run more than one connector.

By default the connector creates its slot at startup if it does not exist. Automatic creation needs the `REPLICATION` privilege, `CREATE` on the database when using `pgoutput` (publication creation), and `max_replication_slots` of at least 1. Long-running transactions do not block slot creation.

Create the slot yourself in production, or when the user lacks those privileges, during controlled upgrades, or when recreating slots after failover:

```sql
SELECT pg_create_logical_replication_slot('slot_name', 'pgoutput');
```

Use `pgoutput` or `decoderbufs` as the plug-in and make `slot_name` match the connector property `slot.name`. Each connector must have a distinct slot name.

Gotcha: a slot keeps every WAL segment the connector still needs, even during outages. Watch WAL disk usage. See postgresql-wal-disk-growth-and-heartbeats.

Check: run `SHOW wal_level;` and confirm it returns `logical` before starting the connector.

## Checked

2026-11-03. Page used: the Debezium postgresql connector reference, https://debezium.io/documentation/reference/stable/connectors/postgresql.html.
Confirmed against it: postgresql.conf settings, automatic slot creation privileges, long-running transactions, manual creation scenarios and command, plug-in choice.
Removed or reworded: the catalog-bloat claim.
Method: documentation only; no commands were run.
