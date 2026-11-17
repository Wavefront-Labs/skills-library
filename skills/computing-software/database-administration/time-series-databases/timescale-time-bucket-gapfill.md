---
id: computing-software.database-administration.time-series-databases.timescale-time-bucket-gapfill
name: timescale-time-bucket-gapfill
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-functions, timescale-time-bucket-gapfill, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Return regular time series with no missing buckets."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# time_bucket and gapfill

**Goal:** Return regular time series with no missing buckets.

## Steps
```sql
SELECT time_bucket_gapfill('1 hour', time) AS bucket, device_id,
       locf(avg(temp)) AS temp, interpolate(avg(temp)) AS temp_lin
FROM conditions
WHERE time >= '2026-11-01' AND time < '2026-11-02' AND device_id = 7
GROUP BY bucket, device_id ORDER BY bucket;
```
- `time_bucket` aligns buckets to midnight UTC. Its default `origin` is midnight on 3 January 2000 for buckets without month/year parts (1 January 2000 for month and year buckets). Pass `timezone` (for `TIMESTAMPTZ`) to start buckets at local midnight, or an `origin` to shift alignment (for example weeks starting on Sunday).
- `time_bucket_gapfill` takes optional `timezone`, `start` and `finish`. The docs say to bound the range with `WHERE`, because `start` and `finish` are legacy and `WHERE` lets the planner exclude chunks.
- `locf()` carries the last value forward (`prev` and `treat_null_as_missing` are optional); `interpolate()` fills linearly. Without a fill function gaps are `NULL`.
- `time_bucket_gapfill` must be a top-level expression of the query or subquery: do not nest it in `round(...)` or cast it; cast in an outer query.

**Gotcha:** Wrapping `time_bucket_gapfill` in another function or cast breaks it; do the cast in an outer query.

## Verify
- Row count equals range divided by bucket width.
- Filled values lie within neighbouring real values.

## Checked

Checked 2026-11-03 against the timescale/docs repository: api/time_bucket, api/_hyperfunctions/time_bucket_gapfill (time_bucket_gapfill, locf, interpolate, intro). Removed: 'aligns to epoch by default' (replaced by the documented origin), the claim that both WHERE bounds are required with an error otherwise, and 'both functions must wrap an aggregate'.

Method: documentation only; no commands were run.
