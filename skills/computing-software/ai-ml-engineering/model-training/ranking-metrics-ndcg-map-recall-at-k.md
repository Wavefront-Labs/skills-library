---
id: computing-software.ai-ml-engineering.model-training.ranking-metrics-ndcg-map-recall-at-k
name: ranking-metrics-ndcg-map-recall-at-k
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, metrics, ndcg, ranking-metrics, mean-average-precision, mrr, recall-at-k, recommender-evaluation]
level: practitioner
status: gated
description: "Evaluate rankers and recommenders: NDCG@k with graded relevance, MAP, MRR, recall@k, per-query averaging, empty-query handling and position-biased click labels."
sources:
  - https://scikit-learn.org/stable/modules/model_evaluation.html#normalized-discounted-cumulative-gain
  - https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html
  - https://github.com/usnistgov/trec_eval
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ranking metrics: NDCG, MAP, MRR, recall@k

**Goal:** measure ranking quality in a way that matches how users consume results.

## Which metric
| Metric | Measures | Use when |
|---|---|---|
| Recall@k | share of relevant items in top k | retrieval stage feeding a reranker/LLM (did we fetch it at all?) |
| Precision@k | share of top k that are relevant | fixed-size result lists |
| MRR | 1 / rank of first relevant item, averaged | one right answer (QA, navigational search) |
| MAP | mean over queries of average precision across all relevant items | binary relevance, many relevant items |
| NDCG@k | discounted gain with graded relevance, normalised by ideal ordering | graded labels (perfect/good/fair), position matters |

## NDCG
`DCG@k = sum_{i=1..k} (2^{rel_i} - 1) / log2(i + 1)`; NDCG = DCG / IDCG (DCG of the ideal ordering). Some implementations use `rel_i` instead of `2^{rel_i}-1`; state which. scikit-learn's `ndcg_score` uses the linear gain `rel_i` (tested on 1.9.1: 0.9608 for relevances [3,2,3,0,1,2] against my linear-gain DCG, versus 0.9488 for the exponential form).
```python
from sklearn.metrics import ndcg_score
ndcg_score(y_true_relevance, y_scores, k=10)    # 2D arrays: one row per query, columns = candidate items; needs at least 2 columns
```
For production evaluation, `trec_eval` (qrels + run files; usnistgov/trec_eval, and its Python wrapper `pytrec_eval`, not run here (gated: unconfirmed, source is paywalled or blocked)) is the reference implementation and handle variable candidate lists per query.

## Practicalities
- **Average per query**, then across queries (macro). Pooling all items across queries is wrong.
- **Queries with no relevant items:** NDCG is undefined (IDCG = 0). scikit-learn returns 0.0 for an all-zero relevance row (tested), which silently drags the mean down. Decide: exclude, or count as 0/1, and report how many.
- **Ties in scores:** different libraries break ties differently; scikit-learn averages over tied scores by default and `ignore_ties=True` assumes an arbitrary order (tested: all-equal scores gave 0.848 vs 0.807). Add a deterministic tie-breaker.
- **Candidate set:** metrics computed over a reranker's candidates ignore what retrieval missed - measure recall@k of retrieval separately.
- **Segments:** head vs tail queries often differ hugely; report both.

## Labels from clicks
Clicks are biased by position (top results get clicked because they're on top). Using raw clicks as relevance rewards the current ranker. Options: human-judged relevance sets, interleaving experiments online, or click models / inverse propensity weighting to correct position bias.

## Verify
- [ ] Metric choice justified by user behaviour (one answer vs list browsing).
- [ ] Per-query averaging and empty-query handling documented.
- [ ] Offline gains confirmed with an online test (A/B or interleaving) before claiming wins.
