---
id: computing-software.database-administration.time-series-databases.prometheus-snapshots-backup
name: prometheus-snapshots-backup
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-backup, prometheus-snapshots-backup, prometheus]
level: practitioner
status: docs-checked
description: "Take consistent point-in-time copies of Prometheus data with the admin API snapshot endpoint."
sources:
  - https://prometheus.io/docs/prometheus/latest/querying/api/
  - https://prometheus.io/docs/prometheus/latest/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshots

**Goal:** Take consistent point-in-time copies of Prometheus data.

## Steps
- Enable the admin API: `--web.enable-admin-api` (default off).
- Snapshot: `curl -XPOST http://localhost:9090/api/v1/admin/tsdb/snapshot`. It writes into `snapshots/<datetime>-<rand>` under the TSDB data directory and returns that directory name. `skip_head=true` skips data present only in the head block.
- The storage docs recommend snapshots for backups: copying files without a snapshot risks losing the samples recorded since the last block was created (typically every two hours, covering the last three hours of samples). Excluding the `chunks_head/`, `wal/` and `wbl/` directories also gives a coherent backup, at the cost of the time range they cover.
- Copy the snapshot off the host with your usual file or object-store tooling.
- Restore: the storage docs describe recovering by restoring block directories from backups into the data directory; do this with Prometheus stopped.
- For ongoing protection, the storage docs point to remote read/write integrations.

**Gotcha:** The admin API also exposes series deletion; keep it behind network controls.

## Verify
- The restored instance returns data for the snapshot's time range.
- `promtool tsdb list <data dir>` lists the snapshot's blocks.

## Checked
2026-11-03. Confirmed against the HTTP API page (admin API flag, snapshot endpoint, `skip_head`, snapshot path) and the storage page (snapshots recommended, backup without snapshots, excluded directories, remote integrations). Removed: the hard-link/small-space claim, the rsync wording, and a step-by-step restore (the pages read describe only restoring block directories from backups).
Method: documentation only; no commands were run.
