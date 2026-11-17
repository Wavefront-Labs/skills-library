---
id: computing-software.ai-ml-engineering.langchain.ensemble-retriever-and-contextual-compression
name: ensemble-retriever-and-contextual-compression
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, retriever, vector-store, ensembleretriever, contextual-compression, hybrid-search, reranking]
level: practitioner
status: gated
description: "Fuse BM25 and vector results with EnsembleRetriever (weighted RRF) and shrink or rerank results with ContextualCompressionRetriever, embeddings filters and cross-encoders."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EnsembleRetriever and contextual compression

## Hybrid: keyword + semantic
```python
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever      # langchain<1.0: langchain.retrievers
bm25 = BM25Retriever.from_documents(chunks, k=10)               # needs rank_bm25; in-memory
dense = vs.as_retriever(search_kwargs={"k": 10})
hybrid = EnsembleRetriever(retrievers=[bm25, dense], weights=[0.4, 0.6])
```
Run: BM25 + dense `EnsembleRetriever` and an `EmbeddingsFilter` `ContextualCompressionRetriever` returned results with fake embeddings; the imports below all resolve. Merging is weighted Reciprocal Rank Fusion (`c: int = 60` in the langchain-classic source), so scores from different retrievers need no normalisation. BM25 wins on exact identifiers (error codes, SKUs, names); dense wins on paraphrase.

`BM25Retriever` rebuilds in memory and does not scale or persist; at production size use the store's native hybrid search (Elasticsearch/OpenSearch, Qdrant sparse vectors, Weaviate hybrid, pgvector + Postgres full-text) and keep the ensemble for prototypes.

## Compression / reranking
```python
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker, EmbeddingsFilter, DocumentCompressorPipeline
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
rerank = CrossEncoderReranker(model=HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base"), top_n=4)   # (gated: unconfirmed, source is paywalled or blocked) model download and scoring not run here
retriever = ContextualCompressionRetriever(base_compressor=rerank, base_retriever=hybrid)
```
Options, cheapest first:
- `EmbeddingsFilter(embeddings=emb, similarity_threshold=0.75)` - drops weakly related docs.
- Cross-encoder reranker (local) or hosted rerankers (`CohereRerank` from `langchain_cohere`, Voyage rerank) - best quality per cost; retrieve 20-50, keep 3-8.
- `LLMChainExtractor` / `LLMChainFilter` - LLM call per document; slow and costly, use rarely.
- `DocumentCompressorPipeline([splitter, redundant_filter, relevant_filter])` chains transformations.

## Gotchas
- Thresholds are model-specific; calibrate on your eval set, never copy defaults.
- Reranking adds latency (cross-encoder on CPU over 50 docs can take hundreds of ms (gated: unconfirmed, source is paywalled or blocked)); batch on GPU or reduce candidates.
- Compression changes text that you cite; keep the original chunk id in metadata for citations.

## Verify
- [ ] recall@k and MRR measured for dense, BM25, hybrid and hybrid+rerank on the same eval set.
- [ ] p95 retrieval latency within budget after adding the reranker.
