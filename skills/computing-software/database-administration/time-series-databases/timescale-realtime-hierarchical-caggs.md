---
id: computing-software.database-administration.time-series-databases.timescale-realtime-hierarchical-caggs
name: timescale-realtime-hierarchical-caggs
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-caggs, timescale-realtime-hierarchical-caggs, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Serve fresh data from a continuous aggregate and stack coarser aggregates on top."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Real-time and hierarchical aggregates

**Goal:** Serve fresh data from a continuous aggregate and stack coarser aggregates on top.

## Steps
- Real-time: `ALTER MATERIALIZED VIEW conditions_hourly SET (timescaledb.materialized_only = false);` joins materialized data with unmaterialized raw data from the source. In the current `create_materialized_view` reference `timescaledb.materialized_only` defaults to `TRUE`, so queries return only materialized data until you change it.
- Hierarchical (2.9 and later): build a daily view from the hourly one: `CREATE MATERIALIZED VIEW conditions_daily WITH (timescaledb.continuous) AS SELECT time_bucket('1 day', bucket) AS bucket, device_id, max(max_temp) AS max_temp FROM conditions_hourly GROUP BY 1,2;`. Use the time-bucketed column of the lower aggregate as the time column.
- Each aggregate in a stack only sees the layer below. Real-time joining recurses down the stack, but stops at any materialized-only aggregate, so layers above it do not get data newer than what it has materialized.
- Aggregates must be re-aggregable: sum of sums, max of max, not avg of avg; store sum and count if you need an average.
- Compress and apply retention to the continuous aggregate itself with `add_compression_policy` and `add_retention_policy` on the view; both accept a continuous aggregate.
- A hierarchical aggregate can sit on an aggregate that has a `JOIN`, but cannot itself have a `JOIN`.

**Gotcha:** Averaging hourly averages gives wrong daily averages; store sum and count and divide at read time.

## Verify
- A new insert shows up in the real-time view before the next refresh.
- Daily totals equal the sum of hourly totals.

## Checked

Checked 2026-11-03 against the timescale/docs repository: api/continuous-aggregates/create_materialized_view and alter_materialized_view, use-timescale/continuous-aggregates/hierarchical-continuous-aggregates and about-continuous-aggregates, api/compression/add_compression_policy, api/data-retention/add_retention_policy. Removed: the 'default false in older releases, true from 2.13' history (current reference shows default TRUE) and the price-like remark about busy tails.

Method: documentation only; no commands were run.
