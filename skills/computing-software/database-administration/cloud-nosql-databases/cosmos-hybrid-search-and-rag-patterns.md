---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-hybrid-search-and-rag-patterns
name: cosmos-hybrid-search-and-rag-patterns
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-hybrid-search-and-rag-patterns, cosmos-vector-and-ai, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Combine vector search with filters and full text."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/vector-search
  - https://learn.microsoft.com/en-us/azure/cosmos-db/gen-ai/hybrid-search
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hybrid search and RAG patterns

**Goal:** Combine vector search with filters and full text.

## Steps
- Combine vector search with other supported query filters in the WHERE clause; filters and partition keys narrow the set of vectors searched.
- Hybrid search combines vector search with full-text (BM25) scoring using the Reciprocal Rank Fusion (RRF) function; the container needs a vector policy, full text policy, vector index and full text index.
- Store text, metadata and vectors in the same document.

## Gotcha
All vectors in a path should have the same number of dimensions, and vector policies and vector indexes are immutable after creation; create a new container to change them.

## Checked

2026-11-03. Confirmed against "Hybrid search in Azure Cosmos DB for NoSQL" and the vector search page: RRF with full-text scoring, required policies and indexes, metadata and vectors in one document, WHERE filters with vector search, same dimensions per path, immutable vector policy and index.
Removed: the embedding-cache advice and the "inserts fail" claim (not on the pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Hybrid query returns relevant chunks and RU per query is within budget.
