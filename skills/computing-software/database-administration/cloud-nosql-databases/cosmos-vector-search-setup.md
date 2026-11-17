---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-vector-search-setup
name: cosmos-vector-search-setup
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-vector-search-setup, cosmos-vector-and-ai, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Store embeddings and query by similarity."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/vector-search
  - https://learn.microsoft.com/en-us/azure/cosmos-db/gen-ai/hybrid-search
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vector search setup

**Goal:** Store embeddings and query by similarity.

## Steps
- Define a vector embedding policy on the container: path, dataType (float32, float16, int8 or uint8), dimensions and distanceFunction (cosine by default, dotproduct, euclidean).
- Add a vectorIndexes entry with type flat, quantizedFlat or diskANN and add the vector path to excludedPaths of the indexing policy. flat allows at most 505 dimensions; quantizedFlat and diskANN at most 4,096 and need at least 1,000 indexed vectors.
- Query: SELECT TOP 10 c.title, VectorDistance(c.contentVector, [1,2,3]) AS SimilarityScore FROM c ORDER BY VectorDistance(c.contentVector, [1,2,3])
- Vector policies and vector indexes are immutable after container creation; create a new container to change them.

## Gotcha
Always use TOP N, or the vector search returns many more results at higher RU and latency; vector search is not supported on accounts with shared throughput.

## Checked

2026-11-03. Confirmed against "Vector search in Azure Cosmos DB for NoSQL" and the hybrid search page: policy fields and data types, distance functions and cosine default, index types, dimension limits, 1,000-vector minimum, excluded vector path in the example policies, VectorDistance query form with TOP N, shared-throughput limitation, immutable policy and index.
Removed: the "vector path in range index may be rejected" claim (not on the page); the query now mirrors the page example instead of an unverified parameter form.
Method: documentation only; no commands were run.

## Verify
- [ ] A top-k query returns expected nearest neighbours and the RU charge is acceptable.
