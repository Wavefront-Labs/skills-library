---
id: computing-software.database-administration.neo4j.call-subquery-patterns
name: call-subquery-patterns
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, call-subquery, union, importing-with, exists-subquery, in-transactions, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Scoped subqueries"
sources:
  - https://neo4j.com/docs/cypher-manual/current/subqueries/call-subquery/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CALL subqueries

Goal: run subqueries per row.
- `CALL (n) { MATCH (n)-->(m) RETURN count(m) AS c }`: variables from the outer scope are imported with the variable scope clause `CALL (<variable>)`.
- `UNION` / `UNION ALL` combine result sets with identical columns.
Verify: per-row results correct on a small set.

## Checked

2026-11-02. Confirmed in the CALL subquery page (variable scope clause). Removed: the older `WITH n` import remark and the top-N-per-group claim.
Method: documentation only; no commands were run.
