---
id: computing-software.database-administration.cassandra.transient-replication
name: transient-replication
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, transient-replication, full-replica, cheap-quorums, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Replica types"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/transientreplication.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transient replication

Goal: understand the experimental replica type.
- Experimental and not recommended for production; first implemented in 4.0.
- Enable on every node with `transient_replication_enabled: true`; set the replication factor as `<total>/<transient>`, for example `'DC1': '3/1'` means 3 replicas in DC1, one of them transient.
- Works with `SimpleStrategy` and `NetworkTopologyStrategy`; transiently replicated keyspaces require tables with `read_repair` set to `NONE`.
- Not usable with monotonic reads, LWT, logged batches, counters, materialized views or secondary indexes.
- Hints are never written for transient replicas.
Verify: only trial in a test cluster.

## Checked

2026-11-02. Checked against the Transient Replication page (experimental warning, setting, syntax, strategies, read_repair NONE, restriction list, hints). Added from the page: read_repair NONE requirement and the exclusions the draft marked 'confirm' (now confirmed, plus monotonic reads and logged batches).

Method: documentation only; no commands were run.
