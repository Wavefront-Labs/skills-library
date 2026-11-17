---
id: computing-software.database-administration.neo4j.out-of-memory-diagnosis
name: out-of-memory-diagnosis
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, heap-dump, gc-log, query-memory-limit, neo4j-troubleshooting, out-of-memory, bolt-connection-refused, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "OOM"
sources: ["https://neo4j.com/docs/operations-manual/current/performance/memory-configuration/", "https://neo4j.com/docs/operations-manual/current/tools/neo4j-admin/neo4j-admin-report/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Out-of-memory diagnosis

Goal: find memory culprits.
- Transaction memory is capped by `db.memory.transaction.max` (a limit on memory a transaction can use) and `db.memory.transaction.total.max` (all transactions in one database; zero means unlimited); lower the limit if OutOfMemory messages appear under high transaction load.
- `CALL {...} IN TRANSACTIONS OF n ROWS` deletes in batches to avoid a huge garbage collection or an OutOfMemory exception.
- `neo4j-admin server report` can include a heap dump (`heap` option) for analysis.
- Size the heap with `server.memory.heap.initial_size` and `server.memory.heap.max_size`.
Verify: the offending query is rewritten or batched and heap use stays flat.

## Checked

2026-11-02. Confirmed in the memory configuration, configuration settings, subqueries-in-transactions and neo4j-admin report pages. Removed: `debug.log` and GC-logging advice and the list of offending query shapes (not read).
Method: documentation only; no commands were run.
