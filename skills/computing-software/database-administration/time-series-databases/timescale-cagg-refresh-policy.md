---
id: computing-software.database-administration.time-series-databases.timescale-cagg-refresh-policy
name: timescale-cagg-refresh-policy
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-caggs, timescale-cagg-refresh-policy, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Keep a continuous aggregate current without refreshing the whole range every time."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Refresh policies

**Goal:** Keep a continuous aggregate current without refreshing the whole range every time.

## Steps
```sql
SELECT add_continuous_aggregate_policy('conditions_hourly',
  start_offset => INTERVAL '3 hours', end_offset => INTERVAL '1 hour', schedule_interval => INTERVAL '30 minutes');
```
- `start_offset` and `end_offset` are relative to the time the policy runs (intervals for timestamp/date columns, integers for integer time columns); `start_offset` must be greater than `end_offset`.
- The docs recommend excluding buckets that see lots of writes through `end_offset`. They advise against `end_offset => NULL`; to include the newest data in queries, enable real-time aggregation instead.
- `start_offset => NULL` is equivalent to `MIN(timestamp)` of the hypertable, so the window reaches back to the oldest data.
- `schedule_interval` defaults to 24 hours. Optional arguments include `if_not_exists`, `initial_start`, `timezone`, `buckets_per_batch` (default 10), `max_batches_per_execution` (default 0, unlimited) and `refresh_newest_first` (default true).
- A manual refresh covers late data older than `start_offset`: `CALL refresh_continuous_aggregate('conditions_hourly', '2026-01-01', '2026-02-01');`. Only buckets that fit completely inside the window are refreshed.
- Changes to data older than the invalidation threshold are logged as the min and max timestamp per transaction, and the affected complete buckets are recalculated at the next refresh.

**Gotcha:** A policy only refreshes its own window, so changes older than `start_offset` are not picked up until you run a manual refresh.

## Verify
- `timescaledb_information.job_stats` shows `last_run_status` of Success and a recent `last_successful_finish`.
- Aggregate and raw sums agree for a closed bucket.

## Checked

Checked 2026-11-03 against the timescale/docs repository (docs.timescale.com now redirects to tigerdata.com/docs): api/continuous-aggregates/add_continuous_aggregate_policy, refresh_continuous_aggregate, use-timescale/continuous-aggregates/about-continuous-aggregates, api/informational-views/job_stats. Removed: the unconfirmed rule that the window must cover two buckets (the documented behaviour is that only fully contained buckets refresh).

Method: documentation only; no commands were run.
