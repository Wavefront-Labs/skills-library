---
id: computing-software.data-engineering.etl-pipeline-design.postgres-replication-slots-and-wal
name: postgres-replication-slots-and-wal
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, cdc, change-data-capture, replication-slots, postgres-wal, logical-decoding, pgoutput, debezium, wal-bloat, publications]
level: practitioner
status: docs-checked
description: "Run Postgres CDC safely: logical replication setup, publications and slots, monitoring retained WAL, preventing disk-full from stalled consumers, heartbeats, failover and cleanup."
sources:
  - https://www.postgresql.org/docs/current/logicaldecoding-explanation.html
  - https://www.postgresql.org/docs/current/view-pg-replication-slots.html
  - https://www.postgresql.org/docs/current/runtime-config-replication.html
  - https://www.postgresql.org/docs/current/functions-admin.html
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Postgres replication slots and WAL bloat

**Goal:** stream changes out of Postgres (Debezium, Fivetran, Airbyte, DMS, Lakeflow) without the CDC consumer ever filling the primary's disk.

## 1. Setup
```sql
-- postgresql.conf (restart required): wal_level = logical; max_replication_slots, max_wal_senders sized for consumers
CREATE ROLE cdc_user WITH LOGIN REPLICATION PASSWORD '<secret>';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO cdc_user;
CREATE PUBLICATION cdc_pub FOR TABLE public.orders, public.customers;   -- explicit list beats FOR ALL TABLES
ALTER TABLE public.orders REPLICA IDENTITY FULL;   -- only if you need full before-images; default uses PK
```
- Managed services expose logical decoding through their own parameter settings; take the exact names from the provider's documentation.
- Tables without a primary key emit updates/deletes without identifying the row unless REPLICA IDENTITY is set — fix before enabling CDC.
- The consumer creates a **logical replication slot** (`pgoutput` plugin) — e.g. Debezium `slot.name`, `publication.name`.

## 2. Why slots are dangerous
A slot makes Postgres **retain all WAL** from the slot's `restart_lsn` until the consumer confirms it. Consumer down for a day on a busy database = a day of WAL on the primary's disk → disk full → database outage.

## 3. Monitor retained WAL
```sql
SELECT slot_name, active, wal_status,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn))        AS retained_wal,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn)) AS consumer_lag
FROM pg_replication_slots;
```
Alert on `active = false` for > N minutes and on retained WAL > a fraction of free disk. `wal_status` values: `reserved` (normal), `extended` (`max_wal_size` exceeded but WAL still retained), `unreserved` (the slot no longer retains the required WAL and some will be removed at a checkpoint), `lost` (the slot is no longer usable).

## 4. Guardrails
- **`max_slot_wal_keep_size`** (default -1, unlimited): cap WAL a slot can retain, e.g. `max_slot_wal_keep_size = '50GB'`. Beyond it the slot is invalidated (`wal_status = lost`) — the CDC consumer must re-snapshot, but the database survives. Choose: snapshot cost vs outage.
- **Heartbeats** for low-traffic databases: if captured tables rarely change but other databases on the instance write WAL, the slot can't advance. Debezium `heartbeat.interval.ms` + `heartbeat.action.query` (e.g. update a heartbeat table included in the publication) keeps it moving.
- Drop slots of retired consumers immediately: `SELECT pg_drop_replication_slot('old_slot');` — an abandoned slot is the usual cause of disk-full incidents.
- The slot's `catalog_xmin` is the oldest catalog transaction the slot needs retained, which holds back vacuum of system catalogs; monitor `pg_stat_activity` for old `xact_start`.

## 5. Failover and upgrades
- Failover slots (`failover = true` at slot creation, plus `sync_replication_slots` enabled on the standby) let a standby keep the slot; Debezium documents enabling them for its connector. Managed services have their own behaviour: check, and plan a re-snapshot path otherwise.
- Major version upgrades: follow the connector's upgrade procedure (Debezium documents stopping the connector, upgrading with an approved procedure such as pg_upgrade, then recreating the slot) and plan a re-snapshot or a resume from a known LSN.

## 6. Schema changes
`pgoutput` sends relation metadata; adding columns is fine, but new tables must be added to the publication (`ALTER PUBLICATION cdc_pub ADD TABLE ...`) and the consumer's table include list.

## Verify
- [ ] Alerts exist for inactive slots and retained WAL size.
- [ ] `max_slot_wal_keep_size` set deliberately (or the risk documented).
- [ ] No slots exist without an active, owned consumer.
- [ ] Failover behaviour tested in staging.

## Checked

Confirmed in the PostgreSQL pg_replication_slots page: `wal_status` values and meanings, `catalog_xmin`, the `active`, `restart_lsn` and `confirmed_flush_lsn` columns; runtime-config-replication: `max_slot_wal_keep_size` default -1; logical decoding page: failover slots with `sync_replication_slots`; Debezium PostgreSQL page: `heartbeat.interval.ms`, `heartbeat.action.query`, failover slots, upgrade procedure; functions-admin page: `pg_current_wal_lsn`, `pg_wal_lsn_diff`, `pg_size_pretty`, `pg_drop_replication_slot`. Removed earlier: managed-service parameter names, version numbers for `max_slot_wal_keep_size` and failover slots, the claim that pg_upgrade drops slots. The alert thresholds are advice, not documented values.

Method: docs-only read, 2026-11-09 (functions-admin and view-pg-replication-slots re-read via text extraction; others checked 2026-10-28); no commands were run.
