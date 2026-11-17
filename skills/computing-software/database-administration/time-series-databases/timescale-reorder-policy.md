---
id: computing-software.database-administration.time-series-databases.timescale-reorder-policy
name: timescale-reorder-policy
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-reorder, timescale-reorder-policy, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Physically order uncompressed chunks by an index to speed range scans."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reorder policy

**Goal:** Physically order uncompressed chunks by an index to speed range scans.

## Steps
- `SELECT add_reorder_policy('conditions', 'conditions_device_id_time_idx');` where the index is on `(device_id, time)`. It runs every 24 hours by default; change the schedule with `alter_job`.
- The policy reorders all chunks except the two most recent, which still get writes. A chunk reordered by the policy is not reordered again by later runs.
- If you write much data into older, already reordered chunks, re-run `SELECT reorder_chunk('_timescaledb_internal._hyper_1_10_chunk', '_timescaledb_internal.conditions_device_id_time_idx');`; if many older chunks changed, drop and recreate the policy.
- `reorder_chunk` works like `CLUSTER` but with lower lock levels (the chunk and hypertable stay readable for most of the process) and uses a bit more disk space.
- Only one reorder policy per hypertable. Remove with `SELECT remove_reorder_policy('conditions');`.
- Useful when data arrives in loose time order but is queried per device. Compressed data gets ordering from compression `segmentby` and `orderby` instead.

**Gotcha:** The reorder policy does not keep re-sorting old chunks that later receive writes; plan to re-run `reorder_chunk` for them.

## Verify
- `timescaledb_information.jobs` shows the reorder policy job.
- Per-device scans read fewer pages (check with `EXPLAIN (ANALYZE, BUFFERS)`).

## Checked

Checked 2026-11-03 against the timescale/docs repository: api/hypertable/add_reorder_policy, reorder_chunk, remove_reorder_policy. Removed: 'the chunk before the newest' (the docs say all except the two most recent), the claim that the rewrite takes a full extra copy of the chunk, and the claim that reordering a compressed table 'wastes work'. Fixed: the wrong chunk count.

Method: documentation only; no commands were run.
