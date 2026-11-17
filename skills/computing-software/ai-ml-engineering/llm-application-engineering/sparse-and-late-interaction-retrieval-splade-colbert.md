---
id: computing-software.ai-ml-engineering.llm-application-engineering.sparse-and-late-interaction-retrieval-splade-colbert
name: sparse-and-late-interaction-retrieval-splade-colbert
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, splade, colbert, sparse-retrieval, late-interaction, hybrid-search]
level: practitioner
status: draft
description: "Add learned sparse (SPLADE) and late-interaction (ColBERT) retrieval: when they beat dense vectors, serving them in Qdrant or Elasticsearch, storage costs, and fusion with RRF."
sources:
  - https://qdrant.tech/documentation/concepts/vectors/#sparse-vectors
  - https://qdrant.tech/documentation/concepts/vectors/#multivectors
  - https://github.com/naver/splade
  - https://github.com/stanford-futuredata/ColBERT
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sparse and late-interaction retrieval (SPLADE, ColBERT)

**Goal:** better retrieval for keyword-heavy and precise queries (part numbers, names, rare terms) than single-vector dense search, at an acceptable cost.

## The approaches
- **SPLADE (learned sparse):** a transformer outputs a weight for each vocabulary term, including expansion terms not in the text. Stored in an inverted index like BM25 but learned; strong out-of-domain. Elastic ELSER and OpenSearch neural sparse are similar ideas.
- **ColBERT (late interaction):** one vector per token; score = sum over query tokens of the max similarity to any document token (MaxSim). Very accurate, but stores tens to hundreds of vectors per chunk.

## SPLADE in Qdrant
```python
from fastembed import SparseTextEmbedding
from qdrant_client import models
sparse = SparseTextEmbedding("prithivida/Splade_PP_en_v1")
client.create_collection("docs",
    vectors_config={"dense": models.VectorParams(size=1024, distance=models.Distance.COSINE)},
    sparse_vectors_config={"splade": models.SparseVectorParams()})
sv = next(sparse.embed(["reset error E-4021 on pump X200"]))
q_sparse = models.SparseVector(indices=sv.indices.tolist(), values=sv.values.tolist())
```

## ColBERT in Qdrant
```python
vectors_config={"colbert": models.VectorParams(size=128, distance=models.Distance.COSINE,
    multivector_config=models.MultiVectorConfig(comparator=models.MultiVectorComparator.MAX_SIM),
    hnsw_config=models.HnswConfigDiff(m=0))}      # no HNSW: used only for reranking
```
Common pattern: retrieve candidates with dense + sparse, rerank the top 100 with ColBERT MaxSim - most of the accuracy at a fraction of the cost. PLAID-style compression (ColBERTv2) cuts storage when ColBERT is the first stage.

## Hybrid fusion
```python
client.query_points("docs",
    prefetch=[models.Prefetch(query=q_dense, using="dense", limit=50),
              models.Prefetch(query=q_sparse, using="splade", limit=50)],
    query=models.FusionQuery(fusion=models.Fusion.RRF), limit=10)
```
Reciprocal rank fusion needs no score calibration. Follow with a cross-encoder reranker if latency allows.

## Costs
| Method | Index size | Query cost |
|---|---|---|
| Dense | 1 vector/chunk | low |
| SPLADE | sparse, roughly BM25-like | low-moderate |
| ColBERT first-stage | many vectors/chunk | high |
| ColBERT rerank | multivectors stored, no HNSW | moderate on top-k |

## Verify
- [ ] On an eval set with exact-term queries, hybrid recall@10 beats dense alone.
- [ ] Storage and p95 latency measured for the chosen combination.
