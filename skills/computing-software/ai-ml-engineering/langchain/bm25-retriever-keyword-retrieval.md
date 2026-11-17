---
id: computing-software.ai-ml-engineering.langchain.bm25-retriever-keyword-retrieval
name: bm25-retriever-keyword-retrieval
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, bm25retriever, bm25, keyword-search, sparse-retrieval, hybrid-search, rank-bm25]
level: practitioner
status: verified
description: "Add keyword retrieval with BM25Retriever: building from documents, custom preprocessing/tokenization, k, persistence limits and combining with dense retrieval in an ensemble."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://github.com/dorianbrown/rank_bm25
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BM25Retriever keyword retrieval

**Why:** dense embeddings miss exact identifiers (error codes, SKUs, function names, rare acronyms). BM25 matches them exactly, and hybrid (BM25 + dense) is often better than either alone; measure on your own queries (see Verify).

## Build
```python
from langchain_community.retrievers import BM25Retriever
import re
def preprocess(text: str) -> list[str]:
    return re.findall(r"[a-z0-9_\-\.]+", text.lower())     # keep identifiers like ERR-4012 and foo.bar

bm25 = BM25Retriever.from_documents(chunks, k=10, preprocess_func=preprocess)
docs = bm25.invoke("ERR-4012 when uploading")
```
- Requires `pip install rank_bm25`. Default preprocessing is whitespace split: punctuation sticks to words and case matters (run: query `err-4012` did not match the document word `ERR-4012:`, query `ERR-4012:` did), so supply your own.
- Add stemming/stopwords (e.g. nltk/snowball) for prose; skip them for code/IDs.
- `bm25_params={"k1": 1.5, "b": 0.75}` to tune term saturation and length normalization.

## Hybrid
```python
from langchain_classic.retrievers import EnsembleRetriever   # not in langchain 1.x: `langchain.retrievers` is gone (pip install langchain-classic)
hybrid = EnsembleRetriever(retrievers=[bm25, vectorstore.as_retriever(search_kwargs={"k": 10})],
                           weights=[0.4, 0.6])     # weighted reciprocal rank fusion
```

## Limits
- In-memory index rebuilt from documents; fine for small to medium corpora (benchmark your size). Pickle the retriever for reuse or move to a search engine (Elasticsearch/OpenSearch BM25, or vector DBs with built-in sparse/hybrid search such as Qdrant, Weaviate, pgvector + tsvector) at scale or when the corpus changes often.
- No metadata filtering; filter documents before building or post-filter results.

## Verify
- [ ] On a labeled query set split into "identifier" and "natural language" queries, compare recall@10 for BM25, dense and hybrid.
