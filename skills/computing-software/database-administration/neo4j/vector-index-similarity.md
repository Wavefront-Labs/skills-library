---
id: computing-software.database-administration.neo4j.vector-index-similarity
name: vector-index-similarity
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, vector-index-create, db-index-vector, embedding-search, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Embedding similarity"
sources:
  - https://neo4j.com/docs/cypher-manual/current/indexes/search-indexes/vector-indexes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vector indexes

Goal: nearest-neighbour search over embeddings.
- `CREATE VECTOR INDEX docs FOR (d:Doc) ON d.embedding OPTIONS {indexConfig:{`vector.dimensions`:1536, `vector.similarity_function`:'cosine'}}`.
- As of Neo4j 2026.01 the preferred query is the Cypher `SEARCH` clause; `db.index.vector.queryNodes` is deprecated in Cypher 25 (2026.04) and replaced by `SEARCH`.
- Providing dimensions is recommended; mismatches then fail clearly at query time.
Verify: known neighbours return at top.

## Checked

2026-11-02. Confirmed in the vector indexes page (OPTIONS keys, SEARCH clause preferred from 2026.01, dimensions recommendation) and the Operations Manual deprecations page (`db.index.vector.queryNodes` replaced by SEARCH). Removed: the "confirm syntax" hedge.
Method: documentation only; no commands were run.
