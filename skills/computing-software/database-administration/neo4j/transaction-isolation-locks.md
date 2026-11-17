---
id: computing-software.database-administration.neo4j.transaction-isolation-locks
name: transaction-isolation-locks
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, read-committed, write-locks, lock-ordering, acid-transactions, lock-contention, deadlock, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Concurrency model"
sources: ["https://neo4j.com/docs/operations-manual/current/database-internals/concurrent-data-access/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Isolation and locks

Goal: avoid contention.
- The default isolation level is read committed: a transaction that reads a node or relationship does not block another from writing it.
- Anomalies can occur under read committed; simulate stronger isolation by taking write locks explicitly (a write lock on a shared node serialises transactions on it).
- Cypher takes a write lock automatically when a `SET` depends on the property it reads (for example `SET n.prop = n.prop + 1`), preventing lost updates.
- `SHOW TRANSACTIONS` lists running transactions (it needs the matching privilege).
Verify: concurrent increments of one property give the expected final value.

## Checked

2026-11-02. Confirmed in the Concurrent data access page and the privileges page (`SHOW TRANSACTIONS`). Removed: the neighbour-locking, supernode serialising and deadlock-retry claims (not read).
Method: documentation only; no commands were run.
