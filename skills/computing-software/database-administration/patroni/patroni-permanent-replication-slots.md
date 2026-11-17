---
id: computing-software.database-administration.patroni.patroni-permanent-replication-slots
name: patroni-permanent-replication-slots
category: computing-software
field: database-administration
product: patroni
tags: [patroni, replication-slots, logical-slots, permanent-slots, slots]
level: advanced
status: docs-checked
description: "Define permanent physical and logical slots via the slots hashmap and understand synchronisation rules."
sources:
  - https://patroni.readthedocs.io/en/latest/dynamic_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep slots across failover.

`slots` is a hashmap in dynamic configuration; slots listed survive switchover/failover and are created by Patroni if missing. It requires `postgresql.use_slots: true`.

```
slots:
  permanent_logical_slot_name:
    type: logical
    database: my_db
    plugin: test_decoding
  permanent_physical_slot_name:
    type: physical
```

Keys: `type` (physical or logical; logical needs `database` and `plugin`; physical may set `cluster_type` as primary or standby, restricting where it exists, otherwise it is not created or an existing one is dropped).

Behaviour:
- PostgreSQL 11+: permanent physical slots are created on all nodes and advanced every `loop_wait` seconds. Older versions: only on the current primary.
- Logical slots are copied from the primary to standbys with a restart, then advanced every `loop_wait`; copying uses a libpq connection with rewind or superuser credentials. Logical slot failover works only on PostgreSQL 11+.
- Defining permanent logical slots makes Patroni enable `hot_standby_feedback`.
- A replica's position may lag the former primary, so applications may receive some messages twice; track `confirmed_flush_lsn`.
- Slots are synchronised only from primary/standby_leader to replicas, so applications must use them on the leader; using them on replicas makes `pg_wal` grow indefinitely on other nodes. Exception: physical slots named like Patroni members are synchronised among all nodes.
- The `nostream` tag disables copying logical slots on that node and its cascading replicas.

## Checked

2026-11-08: slots keys, PostgreSQL 11 behaviour, logical slot copying, hot_standby_feedback, synchronisation warning and the nostream tag confirmed in the dynamic configuration page. Pages were read in full except where noted.

Method: documentation only; no commands were run.
