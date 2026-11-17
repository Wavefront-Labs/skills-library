---
id: computing-software.database-administration.neo4j.explain-and-profile
name: explain-and-profile
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, explain, profile, db-hits, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Reading execution plans"
sources:
  - https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/execution-plans/
  - https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/query-tuning/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EXPLAIN and PROFILE

Goal: read query plans.
- `EXPLAIN` plans the query but does not run it; `PROFILE` runs it and shows real measurements such as DB hits.
- Plans show estimated rows and actual rows; operators such as AllNodesScan, CartesianProduct, EagerAggregation appear in the plan tables.
Verify: after tuning, db hits drop substantially.

## Checked

2026-11-02. Confirmed in the execution plans and query tuning pages. Removed: the generic warning-sign list beyond operator names that appear in the examples.
Method: documentation only; no commands were run.
