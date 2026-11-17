---
id: computing-software.database-administration.postgresql.logical-decoding-for-cdc
name: logical-decoding-for-cdc
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-logical-replication, logical-decoding, wal2json, pgoutput, debezium, change-data-capture, logical-replication-slot, test-decoding, max-slot-wal-keep-size]
level: practitioner
status: verified
description: "Stream PostgreSQL changes to Kafka or other consumers with logical decoding slots (pgoutput, wal2json, Debezium) without letting slots fill the disk."
sources:
  - https://www.postgresql.org/docs/current/logicaldecoding.html
  - https://github.com/eulerto/wal2json
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logical decoding for CDC

**Goal:** feed row-level changes to a downstream system reliably, with slot retention under control.

## Prerequisites
```ini
wal_level = logical          # restart
max_replication_slots = 10
max_wal_senders = 10
max_slot_wal_keep_size = '50GB'   # 13+: cap WAL a lagging slot may pin; slot is invalidated past it
```
Role: `CREATE ROLE cdc WITH REPLICATION LOGIN PASSWORD '...';` plus SELECT on the tables (for snapshots) and an `pg_hba.conf` line for it.

## Try it by hand
```sql
SELECT pg_create_logical_replication_slot('try', 'test_decoding');
INSERT INTO t VALUES (1);
SELECT * FROM pg_logical_slot_peek_changes('try', NULL, NULL);   -- peek: does not consume
SELECT * FROM pg_logical_slot_get_changes('try', NULL, NULL);    -- get: consumes / advances
SELECT pg_drop_replication_slot('try');                           -- ALWAYS clean up
```
wal2json gives JSON: `pg_recvlogical -d app --slot cdc --create-slot -P wal2json` then `pg_recvlogical -d app --slot cdc --start -o format-version=2 -f -`.

## Output plugins
| Plugin | Notes |
|---|---|
| `pgoutput` | Built in, used by native subscriptions and Debezium (`plugin.name=pgoutput`); needs a publication |
| `wal2json` | Extension package; JSON; popular for custom consumers |
| `test_decoding` | Debug only |

## Debezium essentials
- Create the publication yourself (`CREATE PUBLICATION dbz FOR TABLE ...`) and set `publication.autocreate.mode=disabled` so the connector does not need owner rights.
- Tables need a primary key or `REPLICA IDENTITY FULL` to get `before` images on UPDATE/DELETE.
- Low-traffic databases: enable `heartbeat.interval.ms` with a heartbeat table so the slot's `confirmed_flush_lsn` advances while other databases generate WAL.

## Operating slots
```sql
SELECT slot_name, plugin, active, wal_status, pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn)) lag
FROM pg_replication_slots WHERE slot_type = 'logical';
```
Alert when lag grows or `active = false`. A dead consumer with an unbounded slot fills `pg_wal` and takes the primary down.

## Gotchas
- Slots are not failed over to standbys before 17 (17 adds `failover = true` slots + `sync_replication_slots`); after failover the consumer must resnapshot.
- DDL is not decoded; consumers see new columns only when rows change.
- Large transactions are decoded at commit; set `logical_decoding_work_mem` and use streaming (`streaming = on` for pgoutput) to avoid spill files.

## Verify
Insert/update/delete a test row and confirm all three events arrive downstream in order with the right keys; the slot lag returns to near zero.

## Checked
- PostgreSQL 17.6: `test_decoding` slot with `peek` (twice the same 9 rows) versus `get` (consumes, then 0); decoded INSERT/UPDATE/DELETE lines; an UPDATE on a published table without a key fails until `REPLICA IDENTITY FULL`, after which the update shows `old-key:` and `new-tuple:`; the slot-listing queries run; `pg_recvlogical --create-slot -P test_decoding` then `--start -f` streamed `BEGIN`/INSERT/`COMMIT`; `wal2json` is not part of this build; `max_slot_wal_keep_size`, `logical_decoding_work_mem` and the replication-slot settings exist with the shown contexts; creating a slot inside a transaction that already wrote fails (`cannot create logical replication slot in transaction that has performed writes`). The 17 release notes add the slot failover property. Debezium's connector page documents `plugin.name`, `publication.autocreate.mode` with `disabled`, `heartbeat.interval.ms` and the replica-identity requirement; Debezium itself was not run.
