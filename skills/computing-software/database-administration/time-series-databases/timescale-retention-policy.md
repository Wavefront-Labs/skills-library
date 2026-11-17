---
id: computing-software.database-administration.time-series-databases.timescale-retention-policy
name: timescale-retention-policy
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-retention, timescale-retention-policy, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Automatically drop old hypertable chunks."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retention policy

**Goal:** Automatically drop old hypertable chunks.

## Steps
- `SELECT add_retention_policy('conditions', drop_after => INTERVAL '90 days');` (a plain interval as the second argument also works).
- It drops chunks that are fully older than `drop_after` when the policy runs, so rows can survive in a straddling chunk. `drop_created_before` selects by chunk creation time (not supported for continuous aggregates yet).
- Integer time columns need an integer age and `set_integer_now_func`. Only one retention policy per hypertable.
- `schedule_interval` is optional; if omitted the interval is measured from the finish of the last run to the next start.
- Remove: `SELECT remove_retention_policy('conditions');`. The policy also works on continuous aggregates.
- To keep aggregates after raw data is dropped, give the raw table a retention period longer than the refresh window of the aggregate's policy.

**Gotcha:** If a continuous aggregate refreshes over a range whose raw data has been dropped, the refresh sees the deletion and removes those aggregate rows too. Example from the docs: a refresh window of 7 days to 1 day with a 24-hour retention empties the aggregate; use a retention longer than the window, e.g. 30 days.

## Verify
- `show_chunks('conditions', older_than => INTERVAL '90 days')` returns nothing after the job.
- The rollup still returns old buckets.

## Checked

Checked 2026-11-03 against the timescale/docs repository: api/data-retention/add_retention_policy and remove_retention_policy, use-timescale/data-retention/data-retention-with-continuous-aggregates. Removed: 'default daily' schedule (not stated for this policy), and the `ignore_invalidation_older_than` remark (only mentioned as an automatically disabled legacy setting on major upgrade).

Method: documentation only; no commands were run.
