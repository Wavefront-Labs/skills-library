---
id: computing-software.database-administration.neo4j.query-tuning-playbook
name: query-tuning-playbook
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, query-planner-hints, using-index, cardinality-estimates, query-tuning, eager-operator, cartesian-product, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Practical steps"
sources:
  - https://neo4j.com/docs/cypher-manual/current/indexes/performance-indexes/index-hints/
  - https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/
  - https://neo4j.com/docs/operations-manual/current/performance/statistics-execution-plans/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query tuning playbook

Goal: speed up queries.
- Use `PROFILE` and check which operators solve each predicate.
- Hints: `USING INDEX p:Pioneer(born)`, `USING JOIN ON a`; see the index hints page before using them.
- `CALL db.prepareForReplanning()` recalculates all database statistics, triggers an index resample, clears query caches, and queries are then planned with the latest statistics.
Verify: db hits and elapsed time fall.

## Checked

2026-11-02. Confirmed: hint syntax and `db.prepareForReplanning()` behaviour (index-hints, operators-detail, statistics-execution-plans). Removed: 'avoid Cartesian products', 'push filters early' and 'anchor on selective labels' (general advice not stated on the pages).
Method: documentation only; no commands were run.
