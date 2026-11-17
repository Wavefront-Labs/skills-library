---
id: computing-software.messaging-and-integration.debezium.postgresql-failover-slots-pg17
name: postgresql-failover-slots-pg17
category: computing-software
field: messaging-and-integration
product: debezium
tags: [postgresql, failover-slot, high-availability, postgresql-17]
level: sme
status: docs-checked
description: "Enable slot.failover with synchronized_standby_slots so Debezium survives a PostgreSQL 17 primary failover."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
On a PostgreSQL 17 or later primary, Debezium can create failover-enabled replication slots, letting it continue from a promoted standby without losing events.

Steps from the guide:

1. In the connector config set `slot.failover` to `true` (default `false`; it has no effect on PostgreSQL 16 or earlier).
2. On the primary, name the standby's physical slot in `postgresql.conf`:

```
synchronized_standby_slots = 'standby1_slot'
```

3. Restart PostgreSQL to apply it.
4. Verify the slot synchronised:

```sql
SELECT slot_name, failover, synced
FROM pg_replication_slots
WHERE slot_name = 'debezium';
```

`failover` should be `true`. After a failover, the promoted standby holds the slot and Debezium keeps reading from it.

Prerequisites: administrative access to server parameters, a primary running PostgreSQL 17 or later, and the connector configuration prepared.

Topology notes: on PostgreSQL 15 or earlier, slots exist only on the primary and the connector stops if it fails. PostgreSQL 16 allows slots on replicas, but they are not synchronised automatically, so advance them manually.

Gotcha: the docs promise that Debezium keeps reading on the new primary when `slot.failover` is enabled and the standby's physical slot is listed in `synchronized_standby_slots`.

Check: query `pg_replication_slots` and confirm `failover` is `true`; the docs' query also selects `synced`.

## Checked

2026-11-03. Page used: the Debezium postgresql connector reference, https://debezium.io/documentation/reference/stable/connectors/postgresql.html.
Confirmed against it: slot.failover default and PostgreSQL 17 requirement, synchronized_standby_slots, restart, verification query, PostgreSQL 15 and 16 topology notes.
Removed or reworded: the missing-slot guarantee wording and the synced check.
Method: documentation only; no commands were run.
