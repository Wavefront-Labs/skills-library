---
id: computing-software.database-administration.time-series-databases.timescale-space-partitioning
name: timescale-space-partitioning
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-hypertables, timescale-space-partitioning, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Decide whether to add a second hash dimension to a hypertable."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Space partitioning and dimensions

**Goal:** Decide whether to add a second hash dimension to a hypertable.

## Steps
- Add: `SELECT add_dimension('conditions', by_hash('location', 4));` (generalized API from 2.13; there is a deprecated older interface). In the current reference `add_dimension` can only be run on an empty hypertable.
- A dimension can be a range (`by_range`) or hash (`by_hash`) partition; hash partitions are meant to parallelize across multiple disks.
- The docs' best practice is not to use additional dimensions, especially on Tiger Cloud, which handles storage scaling transparently.
- Better tools on one node: composite indexes `(device_id, time DESC)` and compression `segmentby`.
- Unique and primary key indexes must then include every partitioning column, including the space column.
- Check: `timescaledb_information.dimensions`.

**Gotcha:** Adding a dimension on a hypertable that already has data fails; and unique indexes must include the added column too.

## Verify
- `timescaledb_information.dimensions` shows the expected dimensions.
- The chunk count over a 30-day window stays manageable.

## Checked

Checked 2026-11-03 against the timescale/docs repository: api/hypertable/add_dimension, create_hypertable, use-timescale/hypertables/hypertables-and-unique-indexes. Removed: 'designed for multi-node', 'partitions near the number of disks' and the chunk-multiplication planner remarks, which the pages do not state.

Method: documentation only; no commands were run.
