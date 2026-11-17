---
id: computing-software.ai-ml-engineering.langchain.mmr-search-and-score-thresholds
name: mmr-search-and-score-thresholds
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, mmr, similarity-score-threshold, vector-store, retriever, search-kwargs, diversity]
level: practitioner
status: verified
description: "Tune vector store retrieval: similarity vs MMR (fetch_k, lambda_mult) for diverse results, similarity_score_threshold, score semantics per store and k selection."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://reference.langchain.com/python/langchain-core
  - https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MMR search and similarity score thresholds

## Search types
```python
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
retriever = vectorstore.as_retriever(search_type="mmr",
                                     search_kwargs={"k": 6, "fetch_k": 30, "lambda_mult": 0.5})
retriever = vectorstore.as_retriever(search_type="similarity_score_threshold",
                                     search_kwargs={"score_threshold": 0.75, "k": 10})
```

## MMR (maximal marginal relevance)
Fetches `fetch_k` nearest chunks, then greedily selects `k` balancing relevance to the query and dissimilarity to already-selected chunks. `lambda_mult=1` = pure relevance, `0` = max diversity; 0.5-0.7 is a common starting range; tune on your eval set.
Use when retrieval returns near-duplicate chunks (overlapping splits, repeated boilerplate, multiple versions of a doc), wasting the context window.

## Score thresholds
- `score_threshold` must be a float in 0..1 or the retriever raises a pydantic `ValidationError` ("not specified with a float value(0~1)", run). Returns only docs whose relevance score is above the threshold, possibly zero docs. Handle empty results explicitly ("I don't know" path).
- Score meaning differs per store and distance: some return distances (lower is better), LangChain normalizes to a 0-1 relevance via `_select_relevance_score_fn`; verify with `vectorstore.similarity_search_with_relevance_scores(q)` on known queries before picking a threshold. Not every store implements it: `InMemoryVectorStore` raised `NotImplementedError` for both that call and `search_type="similarity_score_threshold"`, while FAISS worked (run, langchain-core 1.6.12 / langchain-community 0.4.2).
- Thresholds depend on the embedding model; re-tune after changing models.

## Choosing k
Measure recall@k on a labeled query set; pick the smallest k that captures the answer most of the time, then rerank (cross-encoder) to cut to the 3-5 best for the prompt.

## Metadata filters
`search_kwargs={"k": 5, "filter": {"source": "handbook"}}` (syntax varies by store) to restrict scope before similarity.

## Verify
- [ ] Recall@k and duplicate rate in top-k compared for similarity vs MMR on the eval set.
