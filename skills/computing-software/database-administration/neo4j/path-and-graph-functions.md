---
id: computing-software.database-administration.neo4j.path-and-graph-functions
name: path-and-graph-functions
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, nodes-function, relationships-function, elementid, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Graph functions"
sources:
  - https://neo4j.com/docs/cypher-manual/current/functions/scalar/
  - https://neo4j.com/docs/cypher-manual/current/functions/list/
  - https://neo4j.com/docs/cypher-manual/current/functions/graph/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Path and graph functions

Goal: inspect graph elements.
- Functions documented: `nodes(p)`, `relationships(p)`, `length(p)`, `labels(n)`, `type(r)`, `properties(n)`, `elementId(n)`.
- `id()` is deprecated; use `elementId()`. Neo4j reuses internal ids when nodes and relationships are deleted, so the docs recommend application-generated ids.
- `elementId()` gives no guarantee about the mapping between ids and elements outside a single transaction.
Verify: no code stores internal ids as keys.

## Checked

2026-11-02. Confirmed: the listed functions, `id()` deprecation and id reuse, `elementId()` guarantees (scalar, list, graph function pages). Removed: 'deprecated in 5.x' and the claim about restores/imports.
Method: documentation only; no commands were run.
