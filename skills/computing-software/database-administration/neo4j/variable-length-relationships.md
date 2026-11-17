---
id: computing-software.database-administration.neo4j.variable-length-relationships
name: variable-length-relationships
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, var-length, relationship-bounds, path-explosion, variable-length-paths, shortest-path, quantified-path-patterns, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "[*1..3] semantics"
sources:
  - https://neo4j.com/docs/cypher-manual/current/patterns/variable-length-paths/
  - https://neo4j.com/docs/cypher-manual/current/patterns/unique-relationship-paths/
  - https://neo4j.com/docs/cypher-manual/current/patterns/reference/variable-length-paths/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variable-length relationships

Goal: traverse bounded depth.
- Legacy syntax `(a)-[:KNOWS*1..3]->(b)`; quantified path patterns express the same as `((:Person)-[:KNOWS]->(:Person)){1,3}`.
- By default the same relationship is never traversed twice in one `MATCH` result, though nodes may be.
Verify: `PROFILE` row counts stay manageable.

## Checked

2026-11-02. Confirmed: `*1..3` and `*..5` forms, `{1,3}` quantified path patterns, default relationship uniqueness (variable-length-paths, unique-relationship-paths, shortest-paths reference). Removed: combinatorial explosion, upper-bound and early-label-filter advice and the version hedge.
Method: documentation only; no commands were run.
