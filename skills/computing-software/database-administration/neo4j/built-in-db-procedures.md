---
id: computing-software.database-administration.neo4j.built-in-db-procedures
name: built-in-db-procedures
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, db-labels, db-schema-visualization, dbms-components, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Introspection"
sources:
  - https://neo4j.com/docs/operations-manual/current/procedures/built-in-procedures/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Built-in db.* procedures

Goal: inspect the model and server.
- `CALL db.labels()`, `db.relationshipTypes()`, `db.schema.visualization()`, `dbms.components()` (returns name, versions, edition), `SHOW PROCEDURES` and `SHOW FUNCTIONS`.
- `CALL db.stats.retrieve('GRAPH COUNTS')`; valid sections are GRAPH COUNTS, TOKENS, QUERIES and META.
Verify: results match expected labels.

## Checked

2026-11-02. Confirmed in the built-in procedures page (`dbms.components`, `db.stats.retrieve` sections) and the privileges page (`db.schema.visualization`). Removed: the tooling remark.
Method: documentation only; no commands were run.
