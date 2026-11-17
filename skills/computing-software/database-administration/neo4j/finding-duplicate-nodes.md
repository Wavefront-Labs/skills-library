---
id: computing-software.database-administration.neo4j.finding-duplicate-nodes
name: finding-duplicate-nodes
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, find-duplicates, group-by-key, fuzzy-match, duplicate-nodes, merge-nodes, data-profiling, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Find duplicate Neo4j nodes by grouping on a key, APOC text similarity functions, GDS Node Similarity, then apoc.refactor.mergeNodes"
sources: ["https://neo4j.com/docs/cypher-manual/current/", "https://neo4j.com/docs/operations-manual/current/", "https://neo4j.com/docs/apoc/current/overview/apoc.text/", "https://neo4j.com/docs/apoc/current/overview/apoc.refactor/apoc.refactor.mergeNodes/", "https://github.com/neo4j/graph-data-science/blob/master/doc/modules/ROOT/pages/algorithms/node-similarity.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding duplicate nodes

Goal: find duplicates before merging.

- Exact key duplicates: `MATCH (p:Person) WITH p.email AS k, collect(p) AS ps WHERE size(ps) > 1 RETURN k, size(ps)`.
- Fuzzy name or text matches: APOC text functions include `apoc.text.distance`, `apoc.text.fuzzyMatch`, `apoc.text.jaroWinklerDistance`, `apoc.text.levenshteinSimilarity` and `apoc.text.sorensenDiceSimilarity`.- Structural similarity: GDS Node Similarity scores pairs by shared neighbours (Jaccard, Overlap or Cosine) on a bipartite graph, with `topK` or `bottomK` (default 10) limiting results per node. It finds nodes that connect to the same things, not nodes with similar text.
- Merge reviewed pairs with `apoc.refactor.mergeNodes(nodes, config)`, whose config controls how properties and relationships are combined.
- Profile counts per key before merging.

Verify: a human reviews a sample of each duplicate group, and counts before and after the merge differ only by the merged nodes.

## Checked
2026-11-09

Method: fetched the APOC text functions overview and mergeNodes pages from neo4j.com (real content), and read the GDS node-similarity docs page (raw asciidoc). Corrected: the "GDS Node Similarity for fuzzy matches" claim, since the page describes neighbour-set similarity not text similarity. Removed: unsupported detail on narrowing candidates. Not checked: mergeNodes config option semantics in detail.
