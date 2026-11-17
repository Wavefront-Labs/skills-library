---
id: computing-software.database-administration.neo4j.merge-idempotent-upsert
name: merge-idempotent-upsert
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, merge, on-create, on-match, create, set-delete, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "MERGE semantics"
sources:
  - https://neo4j.com/docs/cypher-manual/current/clauses/merge/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MERGE for upserts

Goal: avoid duplicates and race pitfalls.
- `MERGE (p:Person {email:$e}) ON CREATE SET p.created=timestamp() ON MATCH SET p.seen=timestamp()`.
- To merge a relationship between existing nodes, bind the nodes first with `MATCH`/`MERGE`, then `MERGE` the relationship.
- Back `MERGE` keys with a property uniqueness or key constraint: under concurrent loads `MERGE` alone guarantees the pattern exists, not that it is unique.
Verify: running twice leaves one node.

## Checked

2026-11-02. Confirmed: `ON CREATE`/`ON MATCH`, merging a relationship between bound nodes, constraints protecting against concurrent duplicates (merge). Removed: the claim that merging whole patterns always creates duplicate nodes.
Method: documentation only; no commands were run.
