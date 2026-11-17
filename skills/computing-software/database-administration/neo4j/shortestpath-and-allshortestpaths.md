---
id: computing-software.database-administration.neo4j.shortestpath-and-allshortestpaths
name: shortestpath-and-allshortestpaths
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, shortestpath, allshortestpaths, path-predicates, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Shortest path queries"
sources:
  - https://neo4j.com/docs/cypher-manual/current/patterns/shortest-paths/
  - https://neo4j.com/docs/cypher-manual/current/patterns/reference/shortest-paths/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# shortestPath and allShortestPaths

Goal: find shortest connections.
- `MATCH p = shortestPath((a:Person {id:$a})-[:KNOWS*..10]-(b:Person {id:$b})) RETURN p`; `allShortestPaths()` returns all of them.
- A `WHERE` on the `MATCH` is a pre-filter: paths satisfying it are found first, then the shortest chosen.
- A predicate checkable during the search (for example `all(rel IN r WHERE rel.flag IS NULL)`) allows a fast bidirectional breadth-first search. A predicate that inspects the whole path after matching (such as its length) forces a slower exhaustive search.
- The manual points to GDS for weighted shortest paths.
Verify: path length matches an independent check.

## Checked

2026-11-02. Confirmed: function syntax, `WHERE` pre-filter, fast versus exhaustive search, GDS for weighted paths (shortest-paths and its reference). Fixed: the draft said per-relationship `ALL(...)` predicates force exhaustive search; the page says those are the fast case. Removed: APOC for weighted paths and 'hop-based'.
Method: documentation only; no commands were run.
