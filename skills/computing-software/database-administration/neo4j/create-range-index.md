---
id: computing-software.database-administration.neo4j.create-range-index
name: create-range-index
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, create-index, range-index, composite-index, text-index, point-index, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Default property indexes"
sources:
  - https://neo4j.com/docs/cypher-manual/current/indexes/search-indexes/
  - https://neo4j.com/docs/cypher-manual/current/indexes/syntax/
  - https://neo4j.com/docs/cypher-manual/current/indexes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Range indexes

Goal: index for lookups and ranges.
- `CREATE INDEX person_name IF NOT EXISTS FOR (p:Person) ON (p.name)`; `IF NOT EXISTS` makes it a no-op when an index of the same name or schema and type exists.
- Composite indexes: `CREATE INDEX composite_index FOR (n:PointOfInterest) ON (n.name, n.type)`. Equality and list-membership predicates must be on the first properties defined in the composite index.
- `SHOW INDEXES` lists indexes with their state (for example `ONLINE`).
Verify: `PROFILE` shows NodeIndexSeek instead of NodeByLabelScan.

## Checked

2026-11-02. Confirmed: `CREATE INDEX` and composite forms, `IF NOT EXISTS`, the leading-property rule, `SHOW INDEXES` states and NodeIndexSeek replacing NodeByLabelScan (create-indexes, using-indexes, list-indexes). Removed: 'range on the last property' wording and 'wait for ONLINE' advice (not stated).
Method: documentation only; no commands were run.
