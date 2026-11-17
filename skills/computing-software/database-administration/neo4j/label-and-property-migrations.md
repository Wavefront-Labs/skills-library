---
id: computing-software.database-administration.neo4j.label-and-property-migrations
name: label-and-property-migrations
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, add-label, rename-property, batch-migrate, graph-migrations, relabel-nodes, refactor-model, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Changing a live model"
sources:
  - https://neo4j.com/docs/cypher-manual/current/subqueries/subqueries-in-transactions/
  - https://neo4j.com/docs/cypher-manual/current/clauses/set/
  - https://neo4j.com/docs/cypher-manual/current/clauses/remove/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relabelling and property migrations

Goal: migrate in batches.
- `CALL { MATCH (n:Old) SET n:New REMOVE n:Old } IN TRANSACTIONS` commits in batches (default 1000 input rows).
- `SET n:Label` adds a label and `REMOVE n:Label` removes one.
Verify: counts by label match before and after.

## Checked

2026-11-02. Confirmed: batch behaviour of `CALL {} IN TRANSACTIONS` and label `SET`/`REMOVE` (subqueries-in-transactions, set, remove). Removed: the zero-downtime sequence and the Liquibase tooling suggestion.
Method: documentation only; no commands were run.
