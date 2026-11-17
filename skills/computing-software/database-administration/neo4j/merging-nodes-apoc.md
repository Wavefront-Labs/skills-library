---
id: computing-software.database-administration.neo4j.merging-nodes-apoc
name: merging-nodes-apoc
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, apoc-refactor-mergenodes, merge-properties, relationship-rewire, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Consolidating"
sources: ["https://neo4j.com/docs/apoc/current/overview/apoc.refactor/apoc.refactor.mergeNodes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Merging nodes

Goal: merge duplicates safely.
- `apoc.refactor.mergeNodes(nodes [, config])`; the documented example passes `{properties:"combine", mergeRels:true}`.
- Config options include `mergeRels`, `selfRef`, `produceSelfRef`, `preserveExistingSelfRels` and `avoidDuplicates`.
Verify: relationship counts are preserved after the merge.

## Checked

2026-11-02. Confirmed in the apoc.refactor.mergeNodes page (syntax, config keys, example). Removed: backup, batching and constraint advice (not on the page).
Method: documentation only; no commands were run.
