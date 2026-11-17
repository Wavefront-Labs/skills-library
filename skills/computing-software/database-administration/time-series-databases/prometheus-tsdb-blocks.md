---
id: computing-software.database-administration.time-series-databases.prometheus-tsdb-blocks
name: prometheus-tsdb-blocks
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-layout, prometheus-tsdb-blocks, prometheus]
level: practitioner
status: docs-checked
description: "Understand the Prometheus on-disk block layout so you can inspect, size and recover a data directory."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://prometheus.io/docs/prometheus/latest/command-line/promtool/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TSDB blocks

**Goal:** Understand the on-disk block layout so you can inspect, size and repair a Prometheus data directory.

## Steps
- The data directory is set by `--storage.tsdb.path` (default `data/`). It holds one directory per block, plus `chunks_head/` and `wal/`.
- Ingested samples are grouped into two-hour blocks. Each block directory holds a `chunks` subdirectory (segment files, each up to 512 MB by default), a metadata file (`meta.json`), an `index` file mapping metric names and labels to series, and `tombstones`.
- Blocks are compacted in the background into longer blocks (see prometheus-compaction).
- Deleting series through the API writes tombstone records instead of removing the data from chunk segments immediately.
- Inspect: `promtool tsdb list -r data/` lists blocks; `promtool tsdb analyze data/` analyzes churn, label pair cardinality and compaction efficiency.
- Average storage is 1-2 bytes per sample.
- If storage is corrupted so Prometheus will not start: back up the directory and restore corrupted block directories from backups; as a last resort remove individual block directories or WAL files, losing the data for that time range.
- Use a local POSIX-compliant filesystem; NFS (including AWS EFS) is not supported.

**Gotcha:** Removing block or WAL files loses the data for their time range; stop the server before touching the data directory.

## Verify
- `promtool tsdb list` shows contiguous blocks with the expected time ranges.
- Prometheus starts cleanly after any restore.

## Checked
2026-11-03. Confirmed against the Prometheus storage page (layout, 2-hour blocks, 512 MB segments, tombstones, 1-2 bytes per sample, corruption advice, NFS) and the promtool page (`tsdb list -r`, `tsdb analyze`). Resolved the "confirm" on the bytes-per-sample figure. Removed: ULID naming, the `lock` file, the `meta.json` field list and compaction level, the `.tmp` directory check and the "corrupts the index state" wording (not on a page read).
Method: documentation only; no commands were run.
