---
id: computing-software.database-administration.time-series-databases.prometheus-retention-time-size
name: prometheus-retention-time-size
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-retention, prometheus-retention-time-size, prometheus]
level: practitioner
status: docs-checked
description: "Configure Prometheus retention by age and size (config file or deprecated flags) and know when blocks are actually deleted."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://prometheus.io/docs/prometheus/latest/configuration/configuration/
  - https://prometheus.io/docs/prometheus/latest/command-line/prometheus/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retention time and size

**Goal:** Configure Prometheus retention by age and size and know when blocks actually go.

## Steps
- Time retention defaults to 15d when neither time nor size is set. Size retention (`size`) is disabled by default (0). Units for size: B, KB, MB, GB, TB, PB, EB, based on powers of 2 (1KB is 1024B).
- Current versions configure retention in the config file under `storage.tsdb.retention` (`time`, `size`, and an experimental `percentage`); these take precedence over the flags `--storage.tsdb.retention.time` and `--storage.tsdb.retention.size`, which are deprecated. Older versions use the flags.
- If both time and size are set, whichever triggers first is used.
- The oldest data is removed first. Only persistent blocks are deleted, but WAL and m-mapped chunks count toward the total size, so the disk must fit the peak of `wal` plus `chunks_head`.
- Blocks must be fully expired before removal, and cleanup runs in the background and may take up to two hours.
- Set the size to at most 80-85 percent of the allocated disk, to leave room for compactions that keep source and compacted blocks at once.
- For long retention beyond one node, the storage docs point to remote storage integrations; local storage is not clustered or replicated.

**Gotcha:** With only a time limit, a cardinality spike can fill the disk before old blocks expire; set a size limit as a safety net.

## Verify
- The oldest data in queries moves forward over time.
- Disk usage stabilises below the disk size with the buffer intact.

## Checked
2026-11-03. Confirmed against the storage page (defaults, units, both limits, WAL counted, two-hour cleanup, 80-85 percent) and the configuration reference and command-line pages (`storage.tsdb.retention` fields, flags deprecated). Corrected: the flags are now deprecated in favour of the config file. Removed: the `500GB` and `30d` example values, "changes take effect after restart" (config says retention changes apply at runtime on the next block reload), the 10 percent headroom figure (replaced by 80-85 percent), the UI path and the two metric names (not on a page read).
Method: documentation only; no commands were run.
