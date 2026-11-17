---
id: computing-software.database-administration.neo4j.set-remove-delete
name: set-remove-delete
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, detach-delete, set-map-update, remove-label, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Mutation clauses"
sources:
  - https://neo4j.com/docs/cypher-manual/current/clauses/set/
  - https://neo4j.com/docs/cypher-manual/current/clauses/delete/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SET, REMOVE and DELETE

Goal: change and remove data.
- `SET n += {a:1}` adds or updates properties; `SET n = {a:1}` replaces all existing properties.
- `DETACH DELETE n` also deletes relationships.
- `SET n:Label` / `REMOVE n:Label` for labels.
- Batch big deletes with `CALL (n) { ... } IN TRANSACTIONS`.
Verify: counts before and after match expectations.

## Checked

2026-11-02. Confirmed in the SET page (replace all properties with `=`) and DELETE page (`DETACH DELETE`, CALL subquery with scope). Removed: the plain-DELETE failure remark (not confirmed).
Method: documentation only; no commands were run.
