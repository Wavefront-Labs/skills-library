---
id: computing-software.database-administration.neo4j.lists-maps-comprehensions
name: lists-maps-comprehensions
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, list-comprehension, pattern-comprehension, unwind, cypher-types, case-expression, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Collection handling"
sources:
  - https://neo4j.com/docs/cypher-manual/current/expressions/list-expressions/
  - https://neo4j.com/docs/cypher-manual/current/expressions/map-expressions/
  - https://neo4j.com/docs/cypher-manual/current/clauses/unwind/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lists, maps and comprehensions

Goal: transform collections.
- List comprehension: `[x IN range(0,10) WHERE x % 2 = 0]` and `[x IN range(0,5) | x * 10]`.
- Pattern comprehension: `[(employee:Person)-[:WORKS_FOR]->(alice) | employee.name]`.
- `UNWIND` expands a list into rows; the new name is required.
- Map projection: `p {.name, .age}` selects properties; `collect(m{.title, .released})` builds lists of maps.
Verify: results match a hand-written example.

## Checked

2026-11-02. Confirmed: list and pattern comprehension forms, `UNWIND`, map projection (list-expressions, map-expressions, unwind). Removed: 'the standard batch-write idiom' wording.
Method: documentation only; no commands were run.
