---
id: computing-software.messaging-and-integration.debezium.postgresql-wal-disk-growth-and-heartbeats
name: postgresql-wal-disk-growth-and-heartbeats
category: computing-software
field: messaging-and-integration
product: debezium
tags: [postgresql, wal, heartbeat, disk-space]
level: advanced
status: docs-checked
description: "Stop replication slots from retaining WAL by using heartbeat.interval.ms and heartbeat.action.query on low-traffic databases."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Debezium slot holds WAL until the connector confirms an LSN. Compare two columns in `pg_replication_slots`: `confirmed_flush_lsn` (data older than this is reclaimable) and `restart_lsn` (oldest WAL the connector may need). If `confirmed_flush_lsn` keeps advancing while `restart_lsn` lags, PostgreSQL reclaims space in batches and no action is needed.

Real growth has these causes from the docs:

- Many updates in the database but few touching captured tables, so no offset commits happen.
- A multi-database instance where Debezium watches a low-traffic database while a busy one fills the shared WAL; the slot is per-database, so Debezium is not invoked.
- AWS RDS writing to its own system tables roughly every five minutes in idle environments.

Fix by enabling heartbeats:

```json
"heartbeat.interval.ms": "10000",
"heartbeat.action.query": "INSERT INTO debezium_heartbeat (ts) VALUES (now())"
```

`heartbeat.interval.ms` defaults to 0 (off). The action query writes a row in the captured database so a change event is produced and the LSN is acknowledged. The heartbeat table must be in the publication named by `publication.name`; if the publication is not `FOR ALL TABLES`, run `ALTER PUBLICATION <name> ADD TABLE <heartbeat_table>;`.

Gotcha: `lsn.flush.mode=manual` makes the connector stop flushing the LSN entirely; WAL will accumulate unless something else flushes it.

Check: watch `pg_replication_slots` over a few minutes and confirm `restart_lsn` advances.

## Checked

2026-11-03. Page used: the Debezium postgresql connector reference, https://debezium.io/documentation/reference/stable/connectors/postgresql.html.
Confirmed against it: confirmed_flush_lsn and restart_lsn, the three causes, heartbeat.interval.ms default, heartbeat.action.query, adding the heartbeat table to the publication, lsn.flush.mode manual.
Removed or reworded: nothing.
Method: documentation only; no commands were run.
