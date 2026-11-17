---
id: computing-software.database-administration.time-series-databases.timescale-unique-constraints
name: timescale-unique-constraints
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-indexing, timescale-unique-constraints, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Enforce uniqueness and upsert on a hypertable."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unique constraints and upserts

**Goal:** Enforce uniqueness and upsert on a hypertable.

## Steps
- A unique index or primary key must include all partitioning columns, in any order, and may include others: `CREATE UNIQUE INDEX ON hypertable_example (device_id, time);`. You cannot create one without the time column. The docs say this restriction guarantees global uniqueness.
- With a space dimension on `device_id`, the index needs both `time` and `device_id`.
- Upsert with standard PostgreSQL syntax: `INSERT INTO conditions (time, device_id, temp) VALUES (...) ON CONFLICT (device_id, time) DO UPDATE SET temp = EXCLUDED.temp;`.
- Foreign keys: from a hypertable to a regular table are supported, and from a regular table referencing a hypertable are supported. Foreign keys from a hypertable to another hypertable are not supported.
- Unique constraints also work when inserting into compressed chunks; a small amount of data is decompressed to check for violations.
- If a table already has a unique index when converted, you can only partition by columns in that index.

**Gotcha:** A constraint without the time column is rejected, so a surrogate `id` primary key alone will not work; pair it with time.

## Verify
- Inserting a duplicate key raises a conflict or updates as designed.
- `\d+ conditions` shows the composite key.

## Checked

Checked 2026-11-03 against the timescale/docs repository: use-timescale/hypertables/hypertables-and-unique-indexes, use-timescale/schema-management/about-constraints, use-timescale/hypercore/modify-data-in-hypercore. Removed: 'uniqueness is checked only within the chunk's range'. Fixed: foreign keys referencing a hypertable from a regular table are supported (the draft said unsupported).

Method: documentation only; no commands were run.
