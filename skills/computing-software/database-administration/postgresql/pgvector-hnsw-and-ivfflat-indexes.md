---
id: computing-software.database-administration.postgresql.pgvector-hnsw-and-ivfflat-indexes
name: pgvector-hnsw-and-ivfflat-indexes
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres-index-types, pgvector, hnsw, ivfflat, vector-search, embeddings, postgres-extensions]
level: practitioner
status: docs-checked
description: "Store embeddings with pgvector and choose, build and tune HNSW or IVFFlat indexes (ops class, m, ef_search, lists, probes) with filtering and recall checks."
sources:
  - https://github.com/pgvector/pgvector
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pgvector: HNSW and IVFFlat indexes

## Setup
```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE doc_chunks (
  id bigserial PRIMARY KEY,
  doc_id bigint NOT NULL,
  embedding vector(1536) NOT NULL         -- dimension must match the model
);
```
Other types: `halfvec` (half-precision; indexable up to 4,000 dimensions, where `vector` is indexable up to 2,000),
`sparsevec` (up to 1,000 non-zero elements), `bit` (binary quantization, up to 64,000 dimensions).

## Query shape the index can use
```sql
SELECT id FROM doc_chunks ORDER BY embedding <=> $1 LIMIT 10;   -- cosine distance
```
Operators: `<->` L2, `<#>` negative inner product, `<=>` cosine, `<+>` L1. The index ops class
must match the operator: `vector_cosine_ops`, `vector_l2_ops`, `vector_ip_ops`. The query
needs `ORDER BY` a distance operator (ascending, not an expression) and a `LIMIT` to use the index.

## HNSW (default choice)
```sql
SET maintenance_work_mem = '8GB';                     -- build in memory or it is very slow
SET max_parallel_maintenance_workers = 7;
CREATE INDEX CONCURRENTLY ON doc_chunks
  USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);
SET hnsw.ef_search = 100;                             -- query time; default 40
```
Better speed-recall trade-off than IVFFlat, no training step so it can be built on an empty table,
but slower to build and more memory. The notice
`hnsw graph no longer fits into maintenance_work_mem` means raise it (without exhausting server memory).

## IVFFlat
```sql
CREATE INDEX ON doc_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 1000);
SET ivfflat.probes = 30;
```
Faster to build and smaller than HNSW but a weaker speed-recall trade-off. Build **after** loading data
(there is a training step). Starting points: `lists` = rows/1000 up to 1M rows, sqrt(rows) beyond;
`probes` = sqrt(lists); `probes` defaults to 1.

## Filtering
`WHERE tenant_id = 42 ORDER BY embedding <=> $1 LIMIT 10`: filtering is applied after the index is
scanned, so with the default `ef_search` of 40 a condition matching 10% of rows leaves about 4 rows. Options:
- pgvector 0.8.0+: `SET hnsw.iterative_scan = relaxed_order;` (or `strict_order`) keeps scanning until enough rows
  (bounded by `hnsw.max_scan_tuples`); IVFFlat has `ivfflat.iterative_scan` and `ivfflat.max_probes`.
- Few distinct filter values: partial indexes. Many values: partitioning (list partitioning or separate tables for tenant isolation).
- B-tree on the filter column can give fast exact search in many cases.

## Measure recall
Compare index results with exact results on a sample:
```sql
BEGIN; SET LOCAL enable_indexscan = off;   -- exact
SELECT id FROM doc_chunks ORDER BY embedding <=> $1 LIMIT 10; COMMIT;
```
Recall = overlap / 10. Raise `ef_search` / `probes` for better recall at the cost of speed.

## Gotchas
- Load initial data first (`COPY` for bulk), then add the index; a higher `ef_construction` costs build time and insert speed.
- Check plans with `EXPLAIN (ANALYZE, BUFFERS)`: a missing `ORDER BY`/`LIMIT` or a non-matching operator gives a sequential scan.

## Verify
`EXPLAIN ANALYZE` of the top-k query uses the HNSW/IVFFlat index and the recall check meets the target.

## Checked

2026-10-31. Confirmed against the pgvector README: operators and ops classes, HNSW defaults (`m` 16, `ef_construction` 64, `ef_search` 40), `maintenance_work_mem` and `max_parallel_maintenance_workers` build advice, the graph-no-longer-fits notice, IVFFlat `lists`/`probes` starting points and training step, dimension limits (vector 2,000, halfvec 4,000, bit 64,000, sparsevec 1,000 non-zero), post-index filtering, iterative scans from 0.8.0, partial indexing/partitioning, `enable_indexscan = off` exact comparison, `CREATE INDEX CONCURRENTLY`. Removed unconfirmed: TOAST size and per-row byte figures, the claim that a distance WHERE clause alone cannot use the index, rebuild-on-drift advice, recall target 0.95, `halfvec` exact storage ratio.

Method: documentation only; no commands were run.
