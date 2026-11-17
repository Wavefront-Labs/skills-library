---
id: computing-software.database-administration.time-series-databases.timescale-index-strategy
name: timescale-index-strategy
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-indexing, timescale-index-strategy, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Index hypertables for your real query shapes without crushing ingest."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Index strategy

**Goal:** Index hypertables for your real query shapes without crushing ingest.

## Steps
- Creating a hypertable creates an index on the time column; keep it.
- Think in layers: equality columns first, then the range column. For per-device queries use `CREATE INDEX ON devices (device_id, time DESC);`; a composite index on `(store_id, device_id, time DESC)` also serves queries on a prefix of its columns.
- Indexes without the time column are possible but the docs note they make ingest very slow.
- `UNIQUE` and `PRIMARY KEY` indexes must include the partitioning column.
- Partial indexes work as in PostgreSQL, e.g. `CREATE INDEX ON conditions (time DESC) WHERE temp > 100;`; the docs show `WHERE humidity IS NOT NULL`.
- Indexes are created per chunk. `CREATE INDEX ... WITH (timescaledb.transaction_per_chunk)` uses one transaction per chunk so inserts continue during most of the build; it replaces `CREATE INDEX CONCURRENTLY`, which is not supported on hypertables, and is not supported for `CREATE UNIQUE INDEX`. If it fails partway the root index is marked invalid (`pg_index.indisvalid IS FALSE`); drop and recreate it.
- `brin` indexes can be built the same way (`USING brin(...) WITH (timescaledb.transaction_per_chunk)`).
- Drop unused indexes after checking `pg_stat_user_indexes.idx_scan`.
- Compressed chunks use their own columnar structures (segmentby and orderby), not the rowstore indexes.

**Gotcha:** Each extra index adds write cost and chunk size, so index only columns your queries filter on.

## Verify
- `EXPLAIN` uses the intended index for key queries.
- Index sizes are acceptable in `chunks_detailed_size('conditions')` (`index_bytes`).

## Checked

Checked 2026-11-03 against the timescale/docs repository: use-timescale/schema-management/about-indexing and indexing, api/hypertable/create_index, use-timescale/hypercore/secondary-indexes, api/hypertable/chunks_detailed_size. Removed: the 'BRIN is rarely needed' opinion, the 'five indexes halve ingest' figure and the no-regular-index claim wording for compressed chunks.

Method: documentation only; no commands were run.
