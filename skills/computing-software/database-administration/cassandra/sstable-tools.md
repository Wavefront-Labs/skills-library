---
id: computing-software.database-administration.cassandra.sstable-tools
name: sstable-tools
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, sstablemetadata, sstablescrub, sstableverify, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Offline tools"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/tools/sstable/index.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/tools/sstable/sstabledump.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/tools/sstable/sstablemetadata.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/tools/sstable/sstableverify.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/tools/sstable/sstablescrub.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSTable utilities

Goal: inspect SSTables.
- `sstabledump <options> <sstable file path>` dumps an SSTable to standard output as JSON (`-l` writes one JSON object per row); `sstablemetadata` shows minimum and maximum timestamp, estimated droppable tombstones and repaired-at.
- `sstableverify <options> <keyspace> <table>` checks for errors or corruption; `sstablescrub` rewrites a broken SSTable skipping corrupted rows, so follow it with a repair.
- Cassandra must be stopped before running these tools; the scripts do not check.
Verify: the dump shows the expected partitions.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: usage lines, outputs, scrub behaviour and the stop-first note (SSTable tools pages). Removed: the claim that sstabledump shows tombstones explicitly.

Method: documentation only; no commands were run.
