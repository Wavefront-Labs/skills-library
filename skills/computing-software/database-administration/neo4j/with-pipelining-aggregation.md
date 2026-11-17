---
id: computing-software.database-administration.neo4j.with-pipelining-aggregation
name: with-pipelining-aggregation
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, with-pipeline, collect, grouping-keys, with-clause, aggregation, order-by-limit, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Query chaining"
sources:
  - https://neo4j.com/docs/cypher-manual/current/clauses/with/
  - https://neo4j.com/docs/cypher-manual/current/functions/aggregating/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WITH and aggregation

Goal: build multi-stage queries.
- A variable not referenced in a `WITH` is dropped from scope; `WITH *` keeps all variables.
- Aggregating functions group by the non-aggregating expressions (the grouping keys): `MATCH ... RETURN a.city, count(*) AS n`.
- `collect(input)` returns a list; `collect(null)` returns an empty list.
- `WITH` can be followed by `WHERE` to filter, for example `WITH s, sum(x) AS totalSales WHERE totalSales >= 1000`.
Verify: group counts total to the row count.

## Checked

2026-11-02. Confirmed: `WITH` scope and `WITH *`, `WITH ... WHERE`, grouping keys, `collect()` (clauses/with, functions/aggregating). Removed: `collect(DISTINCT x)` (the page documents `DISTINCT` only for `count`).
Method: documentation only; no commands were run.
