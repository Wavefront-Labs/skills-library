---
id: computing-software.database-administration.postgresql.physical-replication-slots-and-cascading-replicas
name: physical-replication-slots-and-cascading-replicas
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, streaming-replication, hot-standby, physical-replication-slots, cascading-replication, primary-slot-name, max-slot-wal-keep-size, wal-retention, disk-full]
level: advanced
status: verified
description: "Use physical replication slots so standbys never miss WAL, cap their retention so a dead standby cannot fill the primary's disk, and chain cascading replicas."
sources:
  - https://www.postgresql.org/docs/current/warm-standby.html#STREAMING-REPLICATION-SLOTS
  - https://www.postgresql.org/docs/current/warm-standby.html#CASCADING-REPLICATION
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Physical slots and cascading replication

**Goal:** standbys that can be offline for a while and catch up, without risking
the primary running out of disk.

## Slots
```sql
SELECT pg_create_physical_replication_slot('standby1');   -- on the upstream
```
Standby config: `primary_slot_name = 'standby1'`. The upstream keeps every WAL
segment the slot has not confirmed. A new slot has NULL `restart_lsn`/`wal_status` until a standby first connects;
`pg_create_physical_replication_slot('standby1', true)` reserves WAL immediately (`reserved`).

**Always cap it** (PG13+):
```conf
max_slot_wal_keep_size = 200GB     # slot is invalidated beyond this; default -1 = unlimited
```
An abandoned slot with no cap is the number one cause of "pg_wal filled the disk
and the primary stopped".

## Monitor
```sql
SELECT slot_name, active, wal_status, safe_wal_size,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retained
FROM pg_replication_slots;
```
`wal_status`: `reserved` (fine), `extended` (beyond max_wal_size), `unreserved`
(about to be lost), `lost` (standby must be rebuilt). Alert on `active = f` for
more than minutes and on retained size. Drop unused slots:
`SELECT pg_drop_replication_slot('standby1');`

## Cascading
A standby can serve WAL to further standbys: set `primary_conninfo` on the
downstream to the intermediate standby. Intermediate needs `max_wal_senders`
and `hot_standby = on` (with it off, downstream connections get `the database system is not accepting connections` / `Hot standby mode is disabled`), plus optionally its own slot for the downstream. Use it to save
cross-region bandwidth (one stream per region) or to offload the primary.

## Gotchas
- Physical slots are not copied to standbys; after failover recreate them on the new primary (the promoted node had none). PG17 failover slots cover logical slots only.
- Without slots, set `wal_keep_size` large enough or use `restore_command` from
  an archive so a lagging standby can catch up.
- Cascading adds lag per hop; the docs say cascading replication is asynchronous and synchronous settings have no effect on it.

## Verify
- Every slot is `active` and `wal_status = reserved`.
- `SHOW max_slot_wal_keep_size;` is not -1 on primaries.
- On an intermediate standby, `pg_stat_replication` lists its downstreams.

## Checked
- PostgreSQL 18.6: `pg_basebackup -C -S standby1` and `SELECT pg_create_physical_replication_slot('standby1')` created slots; the monitor query returned `standby1 | t | reserved` while connected; a slot created without `immediately_reserve` showed NULL `wal_status` and `retained`, one created with `true` showed `reserved` and a non-null `restart_lsn`; `pg_drop_replication_slot` removed them. A cascaded standby (second standby streaming from the first, with its own slot `standby2`) appeared in the intermediate's `pg_stat_replication`; with `hot_standby = off` on the intermediate, `pg_basebackup` against it failed with `FATAL: the database system is not accepting connections` / `DETAIL: Hot standby mode is disabled` and `pg_isready` printed `rejecting connections`. After promoting the upstream, its `pg_replication_slots` was empty.
- Docs: view-pg-replication-slots (`reserved`, `extended`, `unreserved`, `lost`, `safe_wal_size` NULL when the cap is -1), runtime-config-replication (`max_slot_wal_keep_size` default -1, unlimited), release 13 (introduced `max_slot_wal_keep_size`), warm-standby (cascading is asynchronous; slots can fill pg_wal).
- Patroni remark removed (not verified).
