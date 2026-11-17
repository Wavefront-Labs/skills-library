---
id: computing-software.database-administration.time-series-databases.timescale-drop-chunks-manual
name: timescale-drop-chunks-manual
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-retention, timescale-drop-chunks-manual, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Drop or inspect chunks manually for one-off cleanup."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manual drop_chunks

**Goal:** Drop or inspect chunks manually for one-off cleanup.

## Steps
- Preview: `SELECT show_chunks('conditions', older_than => INTERVAL '1 year');`.
- Drop: `SELECT drop_chunks('conditions', older_than => INTERVAL '1 year');`; `newer_than` drops chunks newer than a point, and combining both drops the intersection (an error if the ranges do not overlap).
- `created_before` / `created_after` select by chunk creation time instead; they cannot be combined with `older_than` / `newer_than`.
- An `INTERVAL` is computed as `now() - interval` and only works for `TIMESTAMP`, `TIMESTAMPTZ` and `DATE` columns; for integer time columns pass an integer in the column's unit. To remove data in the future (for example wrong clocks), pass a timestamp, not an interval: `drop_chunks('conditions', newer_than => now() + interval '3 months')`.
- The first argument can be a hypertable or a continuous aggregate; drop from each separately.
- Take a backup before large drops.

**Gotcha:** Chunks are dropped only when their whole range is before (or after) the cutoff, so rows older than the cutoff can remain in a straddling chunk.

## Verify
- The preview list before and after matches expectation.
- Disk space is released (check `hypertable_size`).

## Checked

Checked 2026-11-03 against the timescale/docs repository: api/hypertable/drop_chunks and show_chunks. Removed: the ACCESS EXCLUSIVE lock statement and the 'off-peak' lock timing (not documented on these pages) and the claim that dropping raw chunks never touches aggregates (stated instead as dropping each relation separately).

Method: documentation only; no commands were run.
