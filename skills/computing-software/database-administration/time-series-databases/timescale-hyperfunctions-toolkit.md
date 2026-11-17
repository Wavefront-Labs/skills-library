---
id: computing-software.database-administration.time-series-databases.timescale-hyperfunctions-toolkit
name: timescale-hyperfunctions-toolkit
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-functions, timescale-hyperfunctions-toolkit, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Use TimescaleDB Toolkit functions for percentiles, rates and downsampling."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyperfunctions and Toolkit

**Goal:** Use TimescaleDB Toolkit functions for percentiles, rates and downsampling.

## Steps
- Install the extension in the database: `CREATE EXTENSION timescaledb_toolkit;` (the self-hosted docs have per-platform package install pages).
- Approximate percentiles: `SELECT approx_percentile(0.95, percentile_agg(latency)) FROM requests;` (the percentile is in the range 0.0 to 1.0). Store the aggregate in a continuous aggregate and combine buckets with `rollup()`, e.g. `approx_percentile(0.95, rollup(pct_agg))`.
- Counter rates: `counter_agg(time, value)` creates a summary; accessors such as `rate(summary)` and `delta(summary)` read it.
- Downsample for charts: `lttb(time, value, 500)` returns a timevector of about 500 points; unpack with `unnest`.
- Time-weighted average: `average(time_weight('LOCF', time, value))`; the method is `LOCF` or `linear` (alias `trapezoidal`), case-insensitive. `LOCF` suits values recorded only on change.
- More aggregates in the same extension: `stats_agg`, `freq_agg`, `hyperloglog`.
- Upgrade order on self-hosted installs: the docs say to update `timescaledb_toolkit` to 1.6.0 before upgrading `timescaledb` if you use it.

**Gotcha:** Averaging irregularly sampled data with plain `avg` weights each row equally regardless of the time gaps; `time_weight` weights by time.

## Verify
- `\dx` shows `timescaledb_toolkit` installed.
- A percentile result is close to `percentile_cont` on a sample (it is an approximation).

## Checked

Checked 2026-11-03 against the timescale/docs repository: api/_hyperfunctions/uddsketch (approx_percentile, percentile_agg examples), lttb, time_weight, counter_agg/rate, self-hosted/tooling/install-toolkit, self-hosted/upgrades/about-upgrades. Removed: the 'available on Timescale cloud' hedge and the 'within a few percent' accuracy figure.

Method: documentation only; no commands were run.
