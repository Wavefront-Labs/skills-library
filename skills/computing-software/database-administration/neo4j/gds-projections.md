---
id: computing-software.database-administration.neo4j.gds-projections
name: gds-projections
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, gds-graph-project, native-projection, cypher-projection, gds, graph-projection, pagerank, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "In-memory graphs"
sources: ["https://neo4j.com/docs/graph-data-science/current/management-ops/graph-creation/graph-project/", "https://neo4j.com/docs/graph-data-science/current/management-ops/graph-drop/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GDS graph projections

Goal: project graphs for analytics.
- `CALL gds.graph.project(graphName, nodeProjection, relationshipProjection, configuration)` loads a named in-memory graph into the graph catalog.
- Drop it when done with `CALL gds.graph.drop(graphName)` to free memory.
- The catalog lives only while the instance runs; projections are lost on restart.
Verify: the project call yields `nodeCount` and `relationshipCount` as expected.

## Checked

2026-11-02. Confirmed in the graph project, graph drop and graph catalog pages. Removed: `gds.graph.project.estimate`, `gds.graph.list` and 'run on secondaries' (not read).
Method: documentation only; no commands were run.
