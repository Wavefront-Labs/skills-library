---
id: computing-software.database-administration.time-series-databases.timescale-continuous-aggregate-create
name: timescale-continuous-aggregate-create
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-caggs, timescale-continuous-aggregate-create, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Create a materialised rollup on a hypertable that refreshes incrementally."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating a continuous aggregate

**Goal:** Create a materialised rollup on a hypertable that refreshes incrementally.

## Steps
```sql
CREATE MATERIALIZED VIEW conditions_hourly WITH (timescaledb.continuous) AS
SELECT time_bucket('1 hour', time) AS bucket, device_id, avg(temp) AS avg_temp, max(temp) AS max_temp
FROM conditions GROUP BY bucket, device_id WITH NO DATA;
```
- The query selects from a hypertable or another continuous aggregate and groups by `time_bucket(<constant width>, <time column>)`.
- The default is `WITH DATA`, which refreshes once from all current data at creation. `WITH NO DATA` skips that (and allows creation inside a transaction block); refresh later with `CALL refresh_continuous_aggregate('conditions_hourly', '2026-01-01', now());` or a refresh policy.
- Joins are supported: inner joins since 2.10, and `LEFT`/`LATERAL` joins and joins with many tables since 2.16; see the joins table for the release you run.
- Store sum and count rather than avg if you need to re-aggregate to coarser buckets, or build a hierarchical aggregate on the view.
- `timescaledb.create_group_indexes` defaults to true, so indexes on the `GROUP BY` columns plus the bucket are created for you.
- `timescaledb.materialized_only` defaults to true; see the real-time aggregation skill to change it.

**Gotcha:** The default `WITH DATA` builds the whole history in one go at creation; use `WITH NO DATA` and a policy or batched manual refreshes on large tables.

## Verify
- `timescaledb_information.continuous_aggregates` lists the view.
- A sample bucket matches a hand-run aggregate on the raw table.

## Checked

Checked 2026-11-03 against the timescale/docs repository: api/continuous-aggregates/create_materialized_view and refresh_continuous_aggregate, use-timescale/continuous-aggregates/about-continuous-aggregates (joins table) and create-a-continuous-aggregate. Removed: the 'now() is not allowed' claim (not found in these pages) and the advice to add an index on (device_id, bucket DESC) because group indexes are created by default.

Method: documentation only; no commands were run.
