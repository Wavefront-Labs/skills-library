---
id: computing-software.database-administration.cassandra.nodetool-repair-modes
name: nodetool-repair-modes
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, nodetool-repair, incremental-repair, primary-range, repair, anti-entropy, merkle-tree, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Full, incremental, subrange"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/repair.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running nodetool repair

Goal: finish repairs inside gc_grace_seconds.
- Incremental repair is the default; `nodetool repair --full` runs a full repair. Increasing the replication factor needs a full repair (`-full`).
- By default repair covers every range a node replicates, duplicating work if run on each node; `-pr` restricts it to the node's primary ranges, and a full cluster repair is `nodetool repair -pr` on each node in each datacenter.
- With the default gc_grace_seconds of 10 days, repair at least that often so deleted data does not reappear.
- `-prv` previews a repair without running it.
Verify: every range is repaired within the gc_grace_seconds window.

## Checked

2026-11-02. Checked against the Repair page (incremental default, --full, -pr, -prv, gc_grace_seconds 10 days, full repair after raising RF). Removed: 'since 4.0', `repair_admin list` (not in the docs repo) and 'full after topology changes'.

Method: documentation only; no commands were run.
