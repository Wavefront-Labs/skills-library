---
id: computing-software.ai-ml-engineering.llm-application-engineering.query-rewriting-hyde-and-multi-query
name: query-rewriting-hyde-and-multi-query
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, rag, query-rewriting, hyde, multi-query, query-decomposition, step-back-prompting, retrieval]
level: practitioner
status: docs-checked
description: "Improve RAG recall by transforming queries before retrieval: LLM rewriting with chat history, HyDE, multi-query with rank fusion, decomposition, and measuring gains."
sources:
  - https://arxiv.org/abs/2212.10496
  - https://arxiv.org/abs/2310.06117
  - https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query rewriting, HyDE and multi-query retrieval

**Goal:** retrieve the right chunks when users' questions are short, conversational or phrased differently from the documents.

## 1. Conversational rewrite (do this first)
Follow-ups like "what about for contractors?" retrieve nothing on their own. Before retrieval, rewrite with history:
```
Given the conversation and the follow-up question, write a standalone search query.
Include entities from earlier turns. Output only the query.
```
Use a small fast model.

## 2. Multi-query + reciprocal rank fusion
Generate several paraphrases, retrieve for each, fuse:
```python
def rrf(result_lists, k=60):
    scores = {}
    for results in result_lists:
        for rank, doc_id in enumerate(results):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return sorted(scores, key=scores.get, reverse=True)
```
RRF (Cormack et al., 2009) needs only ranks, so it fuses dense and BM25 results too.

## 3. HyDE (Hypothetical Document Embeddings)
Ask the LLM to write a plausible answer passage, embed that, and search with it (Gao et al., 2022). Answer-shaped text lands closer to answer-shaped chunks than a terse question does. Works best zero-shot on domains where queries and docs differ in style; risky when the LLM's hypothetical answer is confidently wrong in a way that pulls retrieval toward wrong documents - keep the original query in the mix (fuse both).

## 4. Decomposition and step-back
- **Decomposition:** split multi-part questions ("compare plan A and B pricing") into sub-queries, retrieve per part, answer with all contexts.
- **Step-back prompting** (Zheng et al., 2023): also retrieve for a more general version of the question ("what are the eligibility rules for parental leave?" for a specific case) to pull in principles.

## 5. Metadata extraction
Have the LLM extract filters (date range, product, region) into structured fields and apply them as metadata filters; this often beats any semantic trick for "latest" or "for EU customers" queries.

## Costs and measurement
- Each transform adds an LLM call and extra retrievals. Route: skip rewriting for standalone queries.
- Measure on a labelled retrieval set: recall@k and MRR with and without each transform. Keep only transforms that help on your data.

## Verify
- [ ] Follow-up questions retrieve the same chunks as their fully specified equivalents.
- [ ] Recall@k improvement per transform measured on an eval set.
- [ ] Added latency within the product's budget.

## Checked
2026-11-01. Confirmed from the papers: Reciprocal Rank Fusion (Cormack et al., SIGIR 2009) score is the sum of 1/(k + rank) with k = 60 and k = 60 near-optimal but not critical; HyDE is Gao et al. 2022 (Precise Zero-Shot Dense Retrieval without Relevance Labels); step-back prompting is Zheng et al. (Take a Step Back, arXiv 2310.06117). Removed: the LangChain MultiQueryRetriever claim and source (the fetched page was not that page), latency and paraphrase-count figures, and the 'fixes most failures' claim. Decomposition and metadata filters are process guidance.
Method: documentation only; no commands were run.
