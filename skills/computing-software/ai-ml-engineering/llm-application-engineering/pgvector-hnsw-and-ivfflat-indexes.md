---
id: computing-software.ai-ml-engineering.llm-application-engineering.pgvector-hnsw-and-ivfflat-indexes
name: pgvector-hnsw-and-ivfflat-indexes
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, embeddings, vector-search, pgvector, hnsw, ivfflat, ann-index, postgres]
level: practitioner
status: docs-checked
description: "Run vector search in Postgres with pgvector: column types, HNSW vs IVFFlat parameters, ef_search/probes tuning, filtered queries with iterative scans, build memory and halfvec."
sources:
  - https://github.com/pgvector/pgvector
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pgvector indexes (HNSW / IVFFlat)

## Schema and exact search
```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE chunks (id bigserial PRIMARY KEY, tenant_id bigint NOT NULL, doc_id text, content text,
                     embedding vector(1024));
SELECT id, content FROM chunks WHERE tenant_id = $1 ORDER BY embedding <=> $2 LIMIT 10;   -- exact without index
```
Operators: `<->` L2, `<=>` cosine distance, `<#>` negative inner product, `<+>` L1. Use the index opclass that matches the operator (`vector_cosine_ops` for `<=>`).

## HNSW (default choice)
```sql
SET maintenance_work_mem = '8GB';                    -- build is much faster if the graph fits
SET max_parallel_maintenance_workers = 7;
CREATE INDEX CONCURRENTLY chunks_emb_hnsw ON chunks USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);
SET hnsw.ef_search = 100;                            -- per session/transaction; default 40
```
Better recall/latency trade-off than IVFFlat, no training step, can be built on an empty table; slower builds and more memory. Results are limited by `ef_search` (default 40), so raise it for recall.

## IVFFlat
```sql
CREATE INDEX ON chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 1000);
SET ivfflat.probes = 32;                             -- default 1
```
IVFFlat has a training step, so build it after loading data (unlike HNSW, which can be built on an empty table). Starting points from the README: lists = rows/1000 up to 1M rows and sqrt(rows) above; probes = sqrt(lists). IVFFlat builds faster and uses less memory than HNSW but has a worse speed-recall trade-off.

## Filtering
With approximate indexes the filter is applied after the index scan, so selective filters can return fewer rows than LIMIT (a condition matching 10% of rows yields about 4 rows at the default `ef_search` of 40). Options:
- pgvector 0.8+: `SET hnsw.iterative_scan = relaxed_order;` (or `strict_order`) keeps scanning until enough rows pass the filter or it reaches `hnsw.max_scan_tuples` (HNSW) or `ivfflat.max_probes` (IVFFlat); IVFFlat has `ivfflat.iterative_scan` too.
- Partial indexes when filtering by only a few distinct values; list partitioning (or separate tables) for many values or tenant isolation.

## Size limits and memory
- `vector` indexes support up to 2,000 dimensions; `halfvec` (float16) up to 4,000 and halves memory: `USING hnsw ((embedding::halfvec(3072)) halfvec_cosine_ops)`. `bit` supports up to 64,000 dimensions with Hamming distance (`bit_hamming_ops`).
- HNSW builds are much faster when the graph fits in `maintenance_work_mem` (Postgres emits a NOTICE when it no longer fits); do not set it so high it exhausts server memory.

## Verify
- [ ] The query plan uses the index.
- [ ] Recall@10 vs exact (unindexed) search on a sample of queries at the chosen ef_search.
- [ ] Filtered queries return LIMIT rows (iterative scan or partial index in place).

## Checked
2026-11-01. Confirmed against the pgvector README: operators including `<+>` (L1) and negative inner product, dimension limits (vector 2,000, halfvec 4,000, bit 64,000), HNSW defaults (`m` 16, `ef_construction` 64, `ef_search` 40), `maintenance_work_mem` and `max_parallel_maintenance_workers` build tips, IVFFlat `probes` default 1 and the lists/probes starting points, iterative scans from 0.8.0 (`relaxed_order`, `strict_order`, `hnsw.max_scan_tuples`), partial indexes and partitioning, `CREATE INDEX CONCURRENTLY`. Removed (not on the pages read): the planner-ignores-index remark, rebuild-on-drift advice, B-tree exact-search tip, shared_buffers and `pg_relation_size` notes, explain/enable_indexscan steps.
Method: documentation only; no commands were run.
