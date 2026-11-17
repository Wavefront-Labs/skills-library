---
id: computing-software.database-administration.neo4j.centrality-community-algorithms
name: centrality-community-algorithms
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, pagerank, louvain, node-similarity, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Running algorithms"
sources: ["https://neo4j.com/docs/graph-data-science/current/algorithms/page-rank/", "https://neo4j.com/docs/graph-data-science/current/common-usage/running-algos/", "https://neo4j.com/docs/graph-data-science/current/introduction/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Centrality, community and path algorithms

Goal: run core algorithms.
- Algorithms run in one of four modes: `stream` (result rows), `stats` (summary), `mutate` and `write`; for example `gds.pageRank.stream`, `gds.pageRank.stats`, `gds.pageRank.mutate`, `gds.pageRank.write`.
- For big graphs, add `ORDER BY` and `LIMIT` to stream results for top-N use.
- `gds.pageRank.write.estimate` estimates memory before a run.
- GDS runs as Community Edition by default; Enterprise features need a GDS Enterprise licence file.
Verify: results sanity-checked on a small known graph.

## Checked

2026-11-02. Confirmed in the PageRank, running-algorithms and introduction pages. Removed: the list of community, similarity and path algorithms (pages not read).
Method: documentation only; no commands were run.
