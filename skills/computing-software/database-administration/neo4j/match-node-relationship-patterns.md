---
id: computing-software.database-administration.neo4j.match-node-relationship-patterns
name: match-node-relationship-patterns
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, match-pattern, relationship-direction, node-labels, match, optional-match, graph-pattern, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Basic pattern syntax"
sources:
  - https://neo4j.com/docs/cypher-manual/current/clauses/match/
  - https://neo4j.com/docs/cypher-manual/current/patterns/unique-relationship-paths/
  - https://neo4j.com/docs/cypher-manual/current/indexes/performance-indexes/using-indexes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MATCH patterns for nodes and relationships

Goal: write correct patterns.
- `MATCH (p:Person {name:$name})-[:ACTED_IN]->(m:Movie) RETURN m.title`.
- `--` matches a relationship in any direction with no filter on type or properties.
- Within one `MATCH` result a relationship is never matched twice.
Verify: `PROFILE` shows NodeIndexSeek rather than NodeByLabelScan when an index exists.

## Checked

2026-11-02. Confirmed: pattern syntax, `--` meaning, relationship uniqueness, NodeIndexSeek replacing NodeByLabelScan (match, unique-relationship-paths, using-indexes). Removed: the AllNodesScan claim, 'omit type is slower' and the repeated-variable identity claim.
Method: documentation only; no commands were run.
