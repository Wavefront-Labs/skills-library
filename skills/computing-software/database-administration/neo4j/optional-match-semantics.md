---
id: computing-software.database-administration.neo4j.optional-match-semantics
name: optional-match-semantics
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, optional-match-nulls, left-join-cypher, null-patterns, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Left-join behaviour"
sources:
  - https://neo4j.com/docs/cypher-manual/current/clauses/optional-match/
  - https://neo4j.com/docs/cypher-manual/current/functions/aggregating/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OPTIONAL MATCH

Goal: keep rows with no match.
- `MATCH (p:Person) OPTIONAL MATCH (p)-[:OWNS]->(c:Car) RETURN p.name, c.model` uses `null` for the missing part of the pattern.
- A `WHERE` after `OPTIONAL MATCH` is part of the pattern description: its predicates are considered while looking for matches, not after.
- `count(input)` ignores `null` values; `count(*)` includes rows returning `null`.
Verify: rows for people without cars still appear.

## Checked

2026-11-02. Confirmed: `null` for missing parts, `WHERE` as part of the pattern, `count()` versus `count(*)` with nulls (optional-match, aggregating).
Method: documentation only; no commands were run.
