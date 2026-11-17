---
id: computing-software.database-administration.postgresql.failover-slots-sync-to-standbys
name: failover-slots-sync-to-standbys
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, failover-slots, sync-replication-slots, logical-replication, standby-slot-names, synchronized-standby-slots, pg17]
level: practitioner
status: docs-checked
description: "Keep PostgreSQL logical replication slots usable after failover with PG17 failover slots: failover=true, sync_replication_slots and synchronized_standby_slots."
sources:
  - https://www.postgresql.org/docs/current/logicaldecoding-explanation.html#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION
  - https://www.postgresql.org/docs/current/runtime-config-replication.html#GUC-SYNC-REPLICATION-SLOTS
  - https://www.postgresql.org/docs/current/logical-replication-failover.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Failover slots synchronized to standbys

Logical slots normally exist only on the primary, so after a failover CDC consumers and subscribers have no slot on the new primary. Logical slots created with `failover` enabled can be synchronized to a physical standby so that subscribers can resume from the new primary.

## Setup
Primary:
```ini
synchronized_standby_slots = 'pg2_slot'   # physical slot(s) of standbys that must confirm WAL before logical consumers get it
```
Standby (pg2):
```ini
sync_replication_slots = on
hot_standby_feedback = on
primary_slot_name = 'pg2_slot'
primary_conninfo = 'host=pg1 user=replicator dbname=postgres'   # dbname required for slot sync
```
Create logical slots with failover enabled:
```sql
SELECT pg_create_logical_replication_slot('cdc', 'pgoutput', failover => true);   -- direct slot
CREATE SUBSCRIPTION sub ... WITH (failover = true);                              -- subscriber-created slot
ALTER SUBSCRIPTION sub SET (failover = true);                                     -- existing (cannot run inside a transaction block)
```

## Check sync state
```sql
-- standby
SELECT slot_name, synced, temporary, inactive_since, invalidation_reason FROM pg_replication_slots;
```
The docs treat a slot as ready for failover when `synced AND NOT temporary AND invalidation_reason IS NULL`. Slots are copied asynchronously, so confirm this before failing over. `pg_sync_replication_slots()` can synchronize manually on the standby, but the docs say it is primarily for testing and debugging, has no cyclic retries and is more prone to failure; `sync_replication_slots = on` is the recommended method.

## Failover procedure
1. Promote pg2.
2. Repoint consumers: subscribers `ALTER SUBSCRIPTION sub CONNECTION 'host=pg2 ...'`.
3. Consumers resume from their confirmed LSN on the synchronized slot.

## Why synchronized_standby_slots matters
Logical WAL senders send decoded changes only after the listed physical slots confirm receiving the WAL, so the consumer cannot get ahead of the standby. The docs say logical replication will not proceed if a listed slot does not exist or is invalidated, and that the primary will not completely shut down until the listed standbys have confirmed the latest flushed WAL; expect some added latency.

## Gotchas
- The standby needs a physical slot to the primary (`primary_slot_name`), `hot_standby_feedback = on` and a valid `dbname` in `primary_conninfo`.
- The slot is persisted on the standby only if the primary's slot still retains WAL and catalog rows that are available on the standby; otherwise it logs that it could not synchronize the slot to avoid data loss.
- `pg_createsubscriber` drops the standby's failover slots (they cannot be synchronized after conversion).

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): Replication Slot Synchronization (logical decoding chapter) and Logical Replication Failover (requirements: failover slot or subscription `failover` option, `sync_replication_slots` on the standby, physical slot via `primary_slot_name`, `hot_standby_feedback`, `dbname` in `primary_conninfo`, `synchronized_standby_slots` recommended, manual `pg_sync_replication_slots` caveats, slot persistence condition, the documented failover-ready query), the `synchronized_standby_slots` and `sync_replication_slots` parameters (the latter off by default) and ALTER SUBSCRIPTION (`SET (failover = ...)` not inside a transaction block). Removed the version gate, the cascading-standby, `max_slot_wal_keep_size` and HA-tool remarks and the Debezium reference, which the documentation does not give.
Method: documentation only; no commands were run.
