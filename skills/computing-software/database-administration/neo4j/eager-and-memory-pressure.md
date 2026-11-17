---
id: computing-software.database-administration.neo4j.eager-and-memory-pressure
name: eager-and-memory-pressure
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, eager-operator-avoidance, transaction-memory-limit, heap-exhaustion, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Avoiding Eager"
sources:
  - https://neo4j.com/docs/operations-manual/current/configuration/configuration-settings/
  - https://neo4j.com/docs/cypher-manual/current/subqueries/subqueries-in-transactions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Eager operators and memory

Goal: bound memory use.
- Batch writes with `CALL { ... } IN TRANSACTIONS`.
- `db.memory.transaction.max` limits the memory of a single transaction; `db.memory.transaction.total.max` limits the total.
Verify: PROFILE shows no Eager and memory stable.

## Checked

2026-11-02. Confirmed in the configuration settings reference. Removed: the description of Eager operators and the read/write split advice (not read).
Method: documentation only; no commands were run.
