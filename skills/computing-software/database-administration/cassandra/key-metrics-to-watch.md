---
id: computing-software.database-administration.cassandra.key-metrics-to-watch
name: key-metrics-to-watch
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, pending-compactions, thread-pool-stats, read-latency, jmx-metrics, cassandra-metrics, dropped-messages, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "What to alert on"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/metrics.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/tools/nodetool/nodetool.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/operating/topo_changes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key metrics and thresholds

Goal: define alerts.
- `nodetool tpstats` prints thread-pool usage; the thread-pool metrics include `PendingTasks` (queued tasks).
- Dropped messages have their own DroppedMessage metrics per message type.
- Per-table figures from `nodetool tablestats` and `tablehistograms`; coordinator latency from `proxyhistograms`; GC from `gcstats`; compactions from `compactionstats`.
- Alert on dropped messages, pending tasks, hint activity and nodes reported down (DN) by `nodetool status`.
Verify: dashboards show per-node p99 and dropped counts.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: thread-pool `PendingTasks`, DroppedMessage metrics, nodetool command descriptions, DN meaning down. Removed: named stages (MutationStage and others), the blocked-task claim, gc.log and the Prometheus exporter.

Method: documentation only; no commands were run.
