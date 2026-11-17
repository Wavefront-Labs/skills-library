---
id: computing-software.database-administration.time-series-databases.timescale-create-hypertable
name: timescale-create-hypertable
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-hypertables, timescale-create-hypertable, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Turn a time-stamped PostgreSQL table into a hypertable partitioned by time."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating a hypertable

**Goal:** Turn a time-stamped PostgreSQL table into a hypertable partitioned by time.

## Steps
```sql
CREATE TABLE conditions (time timestamptz NOT NULL, device_id int, temp double precision);
SELECT create_hypertable('conditions', by_range('time', INTERVAL '1 day'));
```
- The `by_range` form is the generalized API from TimescaleDB 2.13. The older form is `create_hypertable('conditions', 'time', chunk_time_interval => INTERVAL '1 day')`. Newer releases also let you declare it in `CREATE TABLE ... WITH (tsdb.hypertable)`.
- The time column must be `NOT NULL`; `create_hypertable` adds the constraint if it is missing. You cannot convert a table that uses declarative partitioning or inheritance.
- A non-empty table needs `migrate_data => TRUE`, which can lock the table for a long time and can deadlock with foreign keys to other tables; without it a non-empty table errors.
- `create_default_indexes` is `TRUE` by default (indexes on the time/partitioning columns). Add `(device_id, time DESC)` for per-device queries.
- Check: `SELECT * FROM timescaledb_information.hypertables;`.

**Gotcha:** Unique indexes and primary keys on a hypertable must include the partitioning column(s), so `PRIMARY KEY (id)` alone is rejected.

## Verify
- `timescaledb_information.hypertables` lists the table.
- Inserts create chunks visible in `show_chunks('conditions')`.

## Checked

Checked 2026-11-03 against the timescale/docs repository: api/hypertable/create_hypertable, use-timescale/hypertables/hypertables-and-unique-indexes, use-timescale/schema-management/about-indexing. Removed: the claim that the time column can be integer or date without the full type list, and the 'by_range is the current API (confirm)' hedge.

Method: documentation only; no commands were run.
