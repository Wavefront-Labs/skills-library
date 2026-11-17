---
id: computing-software.database-administration.time-series-databases.prometheus-compaction
name: prometheus-compaction
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-layout, prometheus-compaction, prometheus]
level: practitioner
status: docs-checked
description: "Know how Prometheus compacts 2-hour blocks, its disk-headroom cost, overlapping blocks and the Thanos sidecar setting."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://raw.githubusercontent.com/thanos-io/thanos/main/docs/components/sidecar.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compaction

**Goal:** Know how block compaction works and when it falls behind.

## Steps
- Ingested samples are first grouped into two-hour blocks. These are compacted in the background into longer blocks spanning up to 10 percent of the retention time or 31 days, whichever is smaller.
- Source blocks and the new compacted block coexist on disk, so on-disk size can briefly exceed `storage.tsdb.retention.size`; the excess is released at the next retention cleanup. Set the retention size to at most 80-85 percent of the disk so the 15-20 percent buffer covers in-progress compactions.
- Overlapping blocks (for example from backfill): the flag `--storage.tsdb.allow-overlapping-blocks` is needed only for Prometheus v2.38 and below; newer versions do not need it.
- With the Thanos sidecar, local compaction must be disabled by setting `--storage.tsdb.min-block-duration=2h` and `--storage.tsdb.max-block-duration=2h` to equal values (the sidecar uploads only uncompacted blocks unless you use `--shipper.upload-compacted`).
- To watch compaction health, use the compaction metrics exposed on the server's own `/metrics` endpoint (look up exact names there).

**Gotcha:** Equal min and max block duration is for Thanos sidecar setups only; on a standalone server it disables compaction, so blocks stay at 2 hours.

## Verify
- Block count settles rather than growing without bound (`promtool tsdb list data/`).
- Disk usage peaks stay inside the free-space buffer.

## Checked
2026-11-03. Confirmed against the Prometheus storage page (2-hour blocks, 10 percent or 31 days, coexisting blocks, 80-85 percent guidance, overlapping-blocks flag for v2.38 and below) and the Thanos sidecar docs (equal block durations, uncompacted-only upload, `--shipper.upload-compacted`). Resolved the "confirm" on the overlapping-blocks default. Removed: the 2h/6h/18h/54h levels, the 20 percent free-disk figure (replaced by the documented 15-20 percent buffer), three `prometheus_tsdb_compaction*` metric names (not on a page read), and the Mimir claim.
Method: documentation only; no commands were run.
