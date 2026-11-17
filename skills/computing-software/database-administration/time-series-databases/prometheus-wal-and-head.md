---
id: computing-software.database-administration.time-series-databases.prometheus-wal-and-head
name: prometheus-wal-and-head
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-layout, prometheus-wal-and-head, prometheus]
level: practitioner
status: docs-checked
description: "Explain the Prometheus head block, 128 MB WAL segments, WAL compression and replay so restarts and backups behave predictably."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://prometheus.io/docs/prometheus/latest/feature_flags/
  - https://raw.githubusercontent.com/prometheus/prometheus/main/tsdb/docs/format/wal.md
  - https://raw.githubusercontent.com/prometheus/prometheus/main/tsdb/docs/format/head_chunks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WAL and head block

**Goal:** Explain the head block and WAL so restarts, memory and crash recovery behave predictably.

## Steps
- The current block for incoming samples is kept in memory and is not fully persisted. It is protected against crashes by a write-ahead log in `wal/`, replayed when Prometheus restarts.
- WAL files are numbered, sequential segments limited to 128 MB. Prometheus retains at least three WAL files, and high-traffic servers may keep more to hold at least two hours of raw data. WAL files hold uncompacted raw data, so they are much larger than regular block files.
- Head chunks that are memory-mapped live in `chunks_head/`, in the data directory.
- Compression: `--storage.tsdb.wal-compression` can roughly halve WAL size with little extra CPU. It was introduced in 2.11.0 and enabled by default in 2.20.0; once enabled, downgrading below 2.11.0 requires deleting the WAL.
- The feature flag `--enable-feature=memory-snapshot-on-shutdown` stores a snapshot of in-memory chunks and series information on shutdown, so only the part of the WAL not covered by the snapshot needs replaying; this reduces startup time.
- Backups: snapshots are recommended. Excluding `chunks_head/`, `wal/` and `wbl/` gives a coherent copy at the cost of the time range they cover.

**Gotcha:** The WAL and `chunks_head` count toward size-based retention and peak every two hours, so the disk must fit them.

## Verify
- Restart time is acceptable for the series count; if not, consider the memory-snapshot flag.
- The data directory shows `wal/` segments no larger than 128 MB.

## Checked
2026-11-03. Confirmed against the Prometheus storage page (head block, WAL segment size, retention of three files, compression history, backups), the feature flags page (memory-snapshot-on-shutdown) and the TSDB format docs (WAL segments 128MB by default, chunks_head). Resolved the "confirm" on WAL compression default. Removed: 120 samples per chunk, "after about 2 hours the head is cut" wording beyond the two-hour blocks, the 3-8 KB per series figure, the `prometheus_tsdb_*` metric names and the local-SSD advice (not on a page read).
Method: documentation only; no commands were run.
