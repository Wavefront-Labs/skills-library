---
id: computing-software.database-administration.neo4j.node-key-and-type-constraints
name: node-key-and-type-constraints
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, node-key, property-type-constraint, composite-constraint, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Composite keys"
sources:
  - https://neo4j.com/docs/cypher-manual/current/schema/constraints/create-constraints/
  - https://neo4j.com/docs/cypher-manual/current/schema/constraints/list-constraints/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node key and property type constraints

Goal: define composite identity.
- `CREATE CONSTRAINT director_key FOR (d:Director) REQUIRE (d.first, d.last) IS NODE KEY`: the properties must exist and the combination must be unique. Labelled Enterprise Edition.
- `REQUIRE movie.title IS :: STRING` is a property type constraint, also labelled Enterprise Edition.
- `SHOW CONSTRAINTS` lists constraints.
Verify: `SHOW CONSTRAINTS` lists them.

## Checked

2026-11-02. Confirmed: key and type constraint syntax, semantics and Enterprise labels, `SHOW CONSTRAINTS` (create-constraints, list-constraints). Removed: the '5.9+' version claim and 'creation fails on violations'.
Method: documentation only; no commands were run.
