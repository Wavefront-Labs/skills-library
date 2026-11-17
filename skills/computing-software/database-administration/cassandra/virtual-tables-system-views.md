---
id: computing-software.database-administration.cassandra.virtual-tables-system-views
name: virtual-tables-system-views
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, system-views, virtual-keyspace, settings-table, replication-strategy, virtual-tables, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Querying node state via CQL"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/virtualtables.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual tables for diagnostics

Goal: inspect a node using CQL.
- Virtual keyspaces are `system_views` (the tables), `system_metrics` (metrics) and `system_virtual_schema` (internal; do not query it).
- `system_views` includes `settings`, `clients`, `thread_pools`, `sstable_tasks`, `caches`, `disk_usage` and `local_read_latency`; e.g. `SELECT * FROM system_views.clients;`.
- Consistency level is ignored for virtual tables; `ALLOW FILTERING` and aggregates work on them.
- They cannot be created, altered, dropped or truncated, and cannot be included in logged batches.
Verify: the `settings` table matches cassandra.yaml.

## Checked

2026-11-02. Checked against the Virtual Tables page (keyspaces, table list with descriptions, limitations, disk_usage and local_read_latency examples). Removed: the `queries` table and the explicit 'node-local' claim (not stated), and the '4.0+' version label.

Method: documentation only; no commands were run.
