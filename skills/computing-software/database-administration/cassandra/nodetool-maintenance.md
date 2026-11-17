---
id: computing-software.database-administration.cassandra.nodetool-maintenance
name: nodetool-maintenance
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, nodetool-flush, nodetool-drain, nodetool-cleanup, nodetool-scrub, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Operational commands"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/tools/nodetool/nodetool.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/tools/nodetool/drain.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/tools/nodetool/cleanup.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/tools/nodetool/upgradesstables.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nodetool maintenance commands

Goal: run safe maintenance.
- `drain` stops accepting writes and flushes all tables, so run it before shutdown; `flush` flushes tables; `cleanup` removes keys no longer belonging to the node; `scrub` rebuilds SSTables; `upgradesstables` rewrites SSTables not on the current version; `garbagecollect` removes deleted data.
- Compaction throughput can be capped with `nodetool setcompactionthroughput` (MiB/s, 0 disables throttling).
Verify: the node restarts and `nodetool status` shows it up.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: descriptions of each command and `setcompactionthroughput` (nodetool reference). Removed: the claim about commit log replay time.

Method: documentation only; no commands were run.
