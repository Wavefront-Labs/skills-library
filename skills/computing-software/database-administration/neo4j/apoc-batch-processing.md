---
id: computing-software.database-administration.neo4j.apoc-batch-processing
name: apoc-batch-processing
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, apoc-periodic, periodic-commit-apoc, batch-size, apoc, apoc-periodic-iterate, apoc-load-json, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Batching with APOC"
sources: ["https://neo4j.com/docs/apoc/current/overview/apoc.periodic/apoc.periodic.iterate/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# apoc.periodic procedures

Goal: batch large updates.
- `CALL apoc.periodic.iterate("MATCH (n:X) RETURN n","SET n.y=1",{batchSize:10000,parallel:false})`; the config defaults are `batchSize` 10000 and `parallel` false.
- As of Neo4j 2026.04 and Cypher 25, `apoc.periodic.iterate` is deprecated; use `CALL {...} IN CONCURRENT TRANSACTIONS` for parallel work.
- With `parallel: true` conflicting statements may deadlock.
Verify: the result row shows `failedBatches` of 0.

## Checked

2026-11-02. Confirmed in the apoc.periodic.iterate page (syntax, config defaults, deprecation note, parallel deadlock warning, result columns). Removed: the claim that native `CALL {} IN TRANSACTIONS` is preferred only 'when available'.
Method: documentation only; no commands were run.
