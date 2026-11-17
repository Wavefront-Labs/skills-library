---
id: computing-software.ai-ml-engineering.llm-application-engineering.qdrant-collections-and-payload-filters
name: qdrant-collections-and-payload-filters
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, qdrant, pinecone, vector-database, payload-filtering, hybrid-search, vector-search]
level: practitioner
status: verified
description: "Run Qdrant (and Pinecone-style) vector collections: vector params, payload indexes for filtered search, named and sparse vectors for hybrid, quantization and snapshots."
sources:
  - https://qdrant.tech/documentation/concepts/collections/
  - https://qdrant.tech/documentation/concepts/filtering/
  - https://docs.pinecone.io/guides/search/filter-by-metadata
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Qdrant collections and payload filters

## Create a collection
```python
from qdrant_client import QdrantClient, models
qc = QdrantClient(url="http://localhost:6333")      # or QdrantClient(":memory:") for local-mode tests
# Ran every block below against a qdrant v1.19.2 server binary and qdrant-client 1.19.1 (size=8 here instead of 1024)
qc.create_collection("docs",
    vectors_config={"dense": models.VectorParams(size=1024, distance=models.Distance.COSINE)},
    sparse_vectors_config={"bm25": models.SparseVectorParams(modifier=models.Modifier.IDF)},
    hnsw_config=models.HnswConfigDiff(m=16, ef_construct=200),
    quantization_config=models.ScalarQuantization(scalar=models.ScalarQuantizationConfig(type=models.ScalarType.INT8, always_ram=True)))
qc.create_payload_index("docs", field_name="tenant_id", field_schema=models.PayloadSchemaType.KEYWORD)
qc.create_payload_index("docs", field_name="updated_at", field_schema=models.PayloadSchemaType.DATETIME)
```
Create payload indexes for every field you filter on; unindexed filters on large collections are slow and can hurt recall. A filter on the unindexed `text` field still worked (returned the right point), so the penalty is speed, not correctness. The indexing docs say to create payload indexes before ingesting data: the filterable HNSW graph only gets the extra filter-aware edges when it is built after the indexes exist, and indexes added later need the HNSW index rebuilt. `get_collection(...).payload_schema` listed `tenant_id` keyword and `updated_at` datetime.

## Upsert and filtered search
```python
qc.upsert("docs", points=[models.PointStruct(id=pid, vector={"dense": emb}, payload={"tenant_id": "acme", "text": t})])
hits = qc.query_points("docs", query=q_emb, using="dense", limit=10,
    query_filter=models.Filter(must=[models.FieldCondition(key="tenant_id", match=models.MatchValue(value="acme"))]))
```
Qdrant applies filters during HNSW traversal (filterable HNSW), keeping recall high even with selective filters. Measured on 200 random 8-d points with 20 matching the tenant filter: all 10 hits had `tenant_id == "acme"` and recall@10 against brute-force cosine over the same 20 points was 1.0 (a tiny set, so it shows the filter is honoured, not a recall benchmark). `QdrantClient.search` no longer exists in 1.19.1; use `query_points`.

## Hybrid
Query both dense and sparse with `prefetch` and fuse with `models.FusionQuery(fusion=models.Fusion.RRF)` (ran: returned 5 fused ids from a dense prefetch plus a `bm25` sparse prefetch against the `Modifier.IDF` sparse vector). The multitenancy guide adds that in v1.19.0+ BM25-style IDF statistics are shard-wide by default and an `idf` search parameter scopes them to one tenant.

## Multitenancy
One collection with an indexed `tenant_id` (mark `is_tenant=True`) beats one collection per tenant for many small tenants: the multitenancy guide recommends a single collection with payload partitioning for large numbers of small tenants, multiple collections only for a limited number of tenants needing strict isolation, and notes Qdrant Cloud caps a cluster at 1000 collections by default. `create_payload_index(..., field_schema=models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD, is_tenant=True))` ran without error. Always enforce tenant filters server-side in your API layer.

## Operations
Snapshots for backup (`create_snapshot` ran and returned a snapshot name), replication factor and shards in distributed mode (cluster settings: see the Qdrant docs; not exercised on a single node), `search_params=models.SearchParams(hnsw_ef=128)` to trade latency for recall, rescoring with original vectors when quantized (`quantization=models.QuantizationSearchParams(rescore=True)` ran; `get_collection` echoed the INT8 `always_ram=True` config and `m=16, ef_construct=200`).

## Pinecone equivalents
Metadata filters in queries (`filter={"tenant_id": {"$eq": "acme"}}`, `$eq` confirmed on Pinecone's filter-by-metadata page), namespaces for tenant isolation (Pinecone's indexing overview: all reads and writes target one namespace, one per customer for multitenancy), sparse-dense vectors for hybrid.

## Verify
- [ ] Recall@10 with filters vs brute-force exact search on a sample; p99 latency under load.
