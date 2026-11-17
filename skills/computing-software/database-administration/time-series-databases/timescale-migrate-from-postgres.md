---
id: computing-software.database-administration.time-series-databases.timescale-migrate-from-postgres
name: timescale-migrate-from-postgres
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-migration, timescale-migrate-from-postgres, timescaledb, postgresql]
level: practitioner
status: draft
description: "Move an existing PostgreSQL time-series table into a hypertable with minimal downtime."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migrating from PostgreSQL

**Goal:** Move an existing PostgreSQL time-series table into a hypertable with minimal downtime.

## Steps
- Create the new hypertable with the same schema; `create_hypertable(..., by_range('time', INTERVAL '1 day'))`.
- Bulk load by time slices: `INSERT INTO new SELECT * FROM old WHERE time >= $a AND time < $b;` in a loop, or `COPY` out and `timescaledb-parallel-copy` in.
- Keep writes flowing by dual-writing via trigger or application, then cut over.
- For in-place conversion on small tables use `migrate_data => true`.
- Recreate indexes after the load when possible, then `ANALYZE`.
- Rewrite primary keys to include the time column.

**Gotcha:** A single huge INSERT ... SELECT creates one long transaction and enormous WAL; slice by day or hour.

## Verify
- Row counts per day match between old and new.
- Application queries return the same results from the hypertable.
