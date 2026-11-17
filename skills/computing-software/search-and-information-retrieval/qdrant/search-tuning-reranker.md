---
id: computing-software.search-and-information-retrieval.qdrant.search-tuning-reranker
name: search-tuning-reranker
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [reranker, candidate-depth, relevance, evaluation, tuning-reranker]
level: advanced
status: docs-checked
description: "Decide when a cross-encoder reranker is worth adding: test 10 candidates against a tuned first stage on held-out queries."
sources:
  - "https://qdrant.tech/documentation/search-tuning/when-a-reranker-is-worth-it/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The Qdrant guide treats a reranker (a cross-encoder reading query and candidate together) as something to prove before adding. Every candidate takes a forward pass at query time, so it fits the reranking slot, not a first stage.

Three steps:

1. Set the baseline to beat: tuned fusion if you run hybrid search, otherwise your current ranking. Confirm the documents your labels mark relevant reach the candidate list; a reranker only reorders what it gets, and missing documents are a candidate depth or retrieval problem.
2. Rerank 10 candidates with the model you would serve (model choice moved results more than any other setting; read its card for languages, domains and window) and compare with the first-stage baseline on held-out labelled queries, using `nDCG@10`.
3. Raise the candidate count only if the reranker wins, and measure throughput on your document lengths first.

Compare against the strongest first stage: default RRF is a solid baseline, and tuned fusion is stronger, so a gain over the default may be one tuning would give for less query-time cost. Ship a gain only if it survives held-out validation. In the guide's five datasets only two wins (CodeSearchNet, DBPedia-entity) held in 100% of split-half draws; WANDS lost to tuned fusion at every count.

If it loses at 10 candidates, check fit: tokenise sample pairs and compare the 95th percentile length with the model's window (truncation means the model scores a document it only partly read), and check languages and domains. Long queries and a training-domain gap (code) explained the losses. If a fitting model still loses, keep the tuned first stage. In these datasets a deeper list never rescued a reranker that lost at 10, which is a finding to recheck on your own labels.

After a win, pick the smallest count that captures most of the gain: DBPedia-entity reached 96% of its gain by 50 candidates, and ArguAna turned a gain into a loss at 200. Measure the share of queries with relevant documents in the list at each count.

Size for production: measure pairs per second and tail latency on target hardware. The guide's CPU numbers (Apple M5 Pro, FastEmbed 0.8.x) ranged from under 2 docs per second for `jina-reranker-v2` up to 64 to 212 for MiniLM-L-6; some models need a GPU, and `jina-reranker-v2` is CC-BY-NC-4.0.

Other stages for other symptoms: late interaction or a cross-encoder for mis-ordered relevant candidates, maximal marginal relevance for near-duplicates (measure the direction, since `nDCG` does not reward diversity), grouping when one document's chunks fill the page, and a formula query for recency or popularity signals.

## Checked

Method: docs-checked 2026-11-09 against the Qdrant "When Is a Reranker Worth It?" page (landing_page repo, search-tuning/when-a-reranker-is-worth-it.md), read in full. Replaced the unconfirmed 100 to 200 candidate prefetch advice and JSON example with the page's start-at-10 procedure; removed the "before tuning" page claim, which was not read.
