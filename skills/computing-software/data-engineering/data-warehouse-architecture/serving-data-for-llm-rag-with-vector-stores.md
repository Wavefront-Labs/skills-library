---
id: computing-software.data-engineering.data-warehouse-architecture.serving-data-for-llm-rag-with-vector-stores
name: serving-data-for-llm-rag-with-vector-stores
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, vector-database, rag, embeddings, pgvector, hybrid-search, vector-index]
level: practitioner
status: draft
description: "Serve data for LLM retrieval-augmented generation: chunking and embedding pipelines, choosing a vector store, hybrid search, freshness, access control and evaluating retrieval."
sources:
  - https://github.com/pgvector/pgvector
  - https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview
  - https://docs.databricks.com/en/generative-ai/vector-search.html
  - https://www.pinecone.io/learn/series/rag/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Serving for LLM / RAG (vector stores)

RAG retrieves relevant passages from your data and puts them in the LLM prompt. The data engineering problem is a pipeline: source -> clean text -> chunks -> embeddings -> index -> retrieval with filters - kept fresh and access-controlled.

## Pipeline
1. **Extract** documents and records (wikis, tickets, PDFs, product tables) with stable IDs, timestamps and ACL metadata.
2. **Clean and chunk**: split by structure (headings, paragraphs), ~200-800 tokens with small overlap; keep title/section path in each chunk.
3. **Embed** with a fixed, versioned embedding model; store `embedding_model` and `chunk_version` with vectors - changing models means re-embedding everything.
4. **Index** in a vector store with metadata for filtering.
5. **Incremental updates**: CDC or `updated_at` watermarks; delete vectors for deleted/changed documents (tombstones), not just insert.

## Choosing a store
| Option | Fits |
|---|---|
| pgvector (Postgres) | moderate scale (millions), transactional data already in Postgres, SQL filters |
| Warehouse/lakehouse native (Snowflake Cortex Search, Databricks Vector Search, BigQuery vector search) | data already there, governance reuse, managed sync from tables |
| OpenSearch/Elasticsearch | hybrid keyword + vector in one engine |
| Dedicated (Pinecone, Weaviate, Qdrant, Milvus) | large scale, low latency, rich ANN tuning |
```sql
-- pgvector
CREATE EXTENSION vector;
CREATE TABLE chunks (id bigserial PRIMARY KEY, doc_id text, tenant_id text, content text, embedding vector(1536), updated_at timestamptz);
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
SELECT id, content FROM chunks WHERE tenant_id = $1 ORDER BY embedding <=> $2 LIMIT 8;
```

## Retrieval quality
- **Hybrid search** (BM25 keyword + vector, fused with reciprocal rank fusion) beats pure vector for names, codes and exact terms.
- Re-rank top 50 with a cross-encoder/reranker model, send top 5-10 to the LLM.
- Metadata filters (product, date, language, tenant) before or during ANN search; check filtered recall - aggressive filters with HNSW can return too few results (use iterative scans/`ef_search` tuning).

## Access control
Retrieval must enforce the same permissions as the source: store ACL/tenant attributes per chunk and filter on the requesting user's entitlements server-side. A RAG bot that ignores ACLs leaks documents.

## Evaluate
- Build a test set of questions with known relevant documents; measure recall@k and MRR for retrieval, separately from answer quality.
- Monitor freshness lag (source update -> searchable), index size, query latency p95, and empty-result rate.

## Verify
- [ ] Deleted or permission-revoked documents disappear from retrieval within the freshness SLA.
- [ ] Retrieval recall@k measured on a labelled set and tracked across embedding/model changes.
