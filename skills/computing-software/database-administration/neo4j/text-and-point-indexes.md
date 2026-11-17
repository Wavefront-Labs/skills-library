---
id: computing-software.database-administration.neo4j.text-and-point-indexes
name: text-and-point-indexes
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, text-index-contains, point-index-spatial, lookup-index, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Specialised indexes"
sources:
  - https://neo4j.com/docs/cypher-manual/current/indexes/performance-indexes/using-indexes/
  - https://neo4j.com/docs/cypher-manual/current/indexes/performance-indexes/create-indexes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Text, point and token lookup indexes

Goal: pick the right index type.
- A TEXT index only solves predicates on `STRING` values: `STARTS WITH`, `ENDS WITH`, `CONTAINS`. If a range and a text index exist on one property, the planner uses the text index only for `CONTAINS` and `ENDS WITH`.
- A POINT index only solves predicates on `POINT` values.
- Two token lookup indexes (nodes and relationships) are created by default; deleting them severely degrades performance.
Verify: PROFILE operator names reflect the index.

## Checked

2026-11-02. Confirmed in the using-indexes and create-indexes pages. Removed: the claim that RANGE indexes cannot serve CONTAINS and the bounding-box/distance wording for POINT indexes (not stated).
Method: documentation only; no commands were run.
