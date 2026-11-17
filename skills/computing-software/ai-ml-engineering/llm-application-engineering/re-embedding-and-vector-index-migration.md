---
id: computing-software.ai-ml-engineering.llm-application-engineering.re-embedding-and-vector-index-migration
name: re-embedding-and-vector-index-migration
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, embeddings, vector-search, re-embedding, index-migration, blue-green-index, collection-alias]
level: practitioner
status: docs-checked
description: "Migrate a vector index to a new embedding model or chunking without downtime: dual-write, background backfill, shadow evaluation, alias cutover, rollback and cost planning."
sources:
  - https://qdrant.tech/documentation/concepts/collections/#collection-aliases
  - https://opensearch.org/docs/latest/im-plugin/index-alias/
  - https://github.com/pgvector/pgvector
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Re-embedding and index migration

Vectors from different models (or different chunking) live in incompatible spaces: you cannot mix them in one index or compare old queries to new documents. A model change is a full rebuild.

## Plan
1. **Record lineage:** every collection/column stores `embedding_model`, version, dimension, chunker version. Without it you cannot tell what is in the index.
2. **Estimate cost and time:** total tokens x price (batch APIs or self-hosted GPUs for large corpora), throughput limits, index build time.
3. **Choose the target** via offline evaluation (recall@k on your eval set) before touching production.

## Blue/green procedure
1. Create the new index alongside the old (`chunks_v2` collection, or a second vector column with its own index).
2. **Dual-write:** ingestion writes new/changed docs to both old and new from now on.
3. **Backfill:** background job re-embeds the existing corpus into v2 in idempotent batches keyed by chunk id; checkpoint progress; throttle to protect production DB and API quotas.
4. **Verify completeness:** counts per tenant/source match between v1 and v2.
5. **Shadow evaluate:** run live queries against both (embedding queries with the matching model), compare recall on the eval set and overlap of top-k; review differences.
6. **Cut over** atomically: switch the alias (Qdrant `update_collection_aliases`, OpenSearch `POST /_aliases` with remove and add in one request), or a config flag that selects model + column together. Query embedding model and index must switch in the same step.
7. Keep v1 read-only for a rollback window, then drop it and stop dual-writing.

## Gotchas
- Caches of query embeddings or retrieval results keyed without model version serve stale v1 results after cutover.
- Hybrid search weights and reranker thresholds were tuned on v1 scores; re-tune.
- Rate limits during backfill can throttle live ingestion if both share an API key; separate keys or priority.
- Chunking changes alter chunk ids; citations stored in conversations may point at chunks that no longer exist - keep a mapping or keep doc-level references.

## Verify
- [ ] v2 counts equal v1 counts per source before cutover.
- [ ] Eval recall on v2 >= v1 (or the agreed trade-off) and rollback via alias tested.

## Checked
2026-11-01. Confirmed: Qdrant docs say a second collection can be built in the background and the alias switched, with alias changes atomic, via `update_collection_aliases`; OpenSearch docs show `POST /_aliases` and that combining remove and add in one request moves the alias atomically. Removed: the pgvector `CONCURRENTLY` and `vector(1024)` details and the Elasticsearch claim (not in the pages read). The lineage fields, backfill and shadow-evaluation steps are suggested practice.
Method: documentation only; no commands were run.
