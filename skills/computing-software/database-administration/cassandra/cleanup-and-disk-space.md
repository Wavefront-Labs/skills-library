---
id: computing-software.database-administration.cassandra.cleanup-and-disk-space
name: cleanup-and-disk-space
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, disk-space-emergency, garbagecollect-tombstones, snapshot-cleanup, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Out-of-space recovery"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/tools/nodetool/nodetool.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/tools/nodetool/clearsnapshot.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/tools/nodetool/garbagecollect.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/tools/nodetool/cleanup.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reclaiming disk space

Goal: recover from full disks.
- Clear old snapshots with `nodetool clearsnapshot` (`--all`, `-t <snapshot_name>` or `--older-than-timestamp`).
- `nodetool garbagecollect` removes deleted data from one or more tables; `nodetool cleanup` removes keys no longer belonging to a node (for example after adding nodes).
- Never delete live SSTables by hand.
Verify: free disk space recovers and compactions resume.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: `clearsnapshot` options, `garbagecollect` and `cleanup` purposes (nodetool reference pages). Removed: the 20% free-space figure and the unsourced advice to stop compactions and add nodes.

Method: documentation only; no commands were run.
