---
id: computing-software.database-administration.time-series-databases.timescale-compression-policy
name: timescale-compression-policy
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-compression, timescale-compression-policy, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Compress chunks automatically once they are old enough to stop receiving writes."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compression policy

**Goal:** Compress chunks automatically once they are old enough to stop receiving writes.

## Steps
- Enable compression first (`ALTER TABLE ... SET (timescaledb.compress, ...)`); policies can only be created on hypertables or continuous aggregates that already have it.
- `SELECT add_compression_policy('conditions', INTERVAL '7 days');` uses `compress_after`; alternatively `compress_created_before => INTERVAL '3 months'` selects chunks by creation time (mutually exclusive with `compress_after`, not yet supported for continuous aggregates). Integer time columns need an integer age and `set_integer_now_func`.
- Since 2.18.0 this is superseded by `CALL add_columnstore_policy('conditions', after => INTERVAL '7 days');` (needs `after` or `created_before`, not both); the compression APIs remain supported.
- Inserts, updates and deletes on compressed chunks are supported, but choose an age beyond your normal backfill window so late data lands in uncompressed chunks.
- Manual: `SELECT compress_chunk(c) FROM show_chunks('conditions', older_than => INTERVAL '7 days') c;`.
- Decompress: `SELECT decompress_chunk('_timescaledb_internal._hyper_2_2_chunk');`.
- Jobs: `SELECT * FROM timescaledb_information.jobs WHERE proc_name = 'policy_compression';`.
- Remove: `SELECT remove_compression_policy('conditions');`.

**Gotcha:** The policy age must exceed how late your data arrives, otherwise late writes keep touching compressed chunks.

## Verify
- `chunk_compression_stats('conditions')` shows older chunks as compressed.
- Job runs report success in `timescaledb_information.job_stats`.

## Checked

Checked 2026-11-03 against the timescale/docs repository: api/compression/add_compression_policy, compress_chunk, decompress_chunk, remove_compression_policy, api/hypercore/add_columnstore_policy, api/hypertable/show_chunks, use-timescale/hypercore/modify-data-in-hypercore. Removed: the price note and the 'newer: add_columnstore_policy, confirm' hedge (now stated with its documented CALL form).

Method: documentation only; no commands were run.
