---
id: computing-software.database-administration.valkey.latency-monitor
name: latency-monitor
category: computing-software
field: database-administration
product: valkey
tags: [latency-monitor, latency-monitor-threshold, latency-doctor, latency-history, latency-graph, events]
level: practitioner
status: docs-checked
description: "Valkey latency monitoring: latency-monitor-threshold, monitored events, 160-entry time series and the LATENCY LATEST, HISTORY, GRAPH, DOCTOR, RESET commands."
sources:
  - https://valkey.io/topics/latency-monitor/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Latency monitoring samples latency-sensitive code paths (hooks), records spikes in per-event time series, and offers raw reporting plus a human-readable analysis.

Enable it by setting a threshold in milliseconds; only events at or above it are logged as spikes. It is off by default (threshold 0), though its cost is near zero:
```
CONFIG SET latency-monitor-threshold 100
```
Pick the threshold from your own requirement (for a 100 ms maximum, use 100).

Time series: one per event, 160 elements, each a pair of Unix timestamp and milliseconds taken. Spikes in the same second merge by keeping the maximum, so at least 160 seconds of history exist even under a low threshold. The all-time maximum is also recorded.

Events: `command` (regular commands), `fast-command` (O(1) and O(log N)), `fork` (the fork system call), `rdb-unlink-temp-file`, `aof-fsync-always` (fsync under `appendfsync always`), `aof-write`, `aof-write-pending-fsync`, `aof-write-active-child`, `aof-write-alone`, `aof-fstat`, `aof-rename`, `aof-rewrite-diff-write`, `active-defrag-cycle`, `expire-cycle`, `eviction-cycle`, `eviction-del`.

Commands:
- `LATENCY LATEST`: latest sample for every event.
- `LATENCY HISTORY event`: the time series for one event.
- `LATENCY GRAPH event`: ASCII graph.
- `LATENCY DOCTOR`: readable analysis with hints.
- `LATENCY RESET [event ...]`: clear series.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/latency-monitor/ (page text read in full): Four conceptual parts, threshold in milliseconds and CONFIG SET example, off by default, 160-element series, same-second maximum merge, 160 seconds minimum history, all-time maximum, every listed event, the five LATENCY subcommands.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.
