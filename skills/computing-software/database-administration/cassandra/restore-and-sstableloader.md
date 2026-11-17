---
id: computing-software.database-administration.cassandra.restore-and-sstableloader
name: restore-and-sstableloader
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, sstableloader, nodetool-refresh, point-in-time-restore, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Restore procedures"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/tools/nodetool/refresh.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/tools/sstable/sstableloader.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/operating/backups.html", "https://cassandra.apache.org/doc/latest/cassandra/architecture/storage-engine.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restoring and sstableloader

Goal: restore tables.
- `nodetool refresh <ks> <t>` loads newly placed SSTables without a restart.
- `sstableloader -d <hosts> <path>/<ks>/<table>` bulk-loads SSTables; `-d`/`--nodes` (initial hosts) is required.
- Commit log segment archiving is configured in `commitlog_archiving.properties`.
Verify: row counts match source.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: `refresh` purpose, `sstableloader` `--nodes` requirement and directory form, `commitlog_archiving.properties` mention (tool pages, storage engine). Removed: the topology-based choice between the two tools and the point-in-time restore claim.

Method: documentation only; no commands were run.
