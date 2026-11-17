---
id: computing-software.ai-ml-engineering.llm-application-engineering.similarity-metrics-and-embedding-normalization
name: similarity-metrics-and-embedding-normalization
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, cosine-similarity, embeddings, vector-search, normalization, score-thresholds]
level: practitioner
status: gated
description: "Choose cosine, dot product or L2 to match the embedding model, normalise vectors correctly, configure index operators, and calibrate similarity thresholds per model."
sources:
  - https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html
  - https://github.com/pgvector/pgvector#querying
  - https://qdrant.tech/documentation/concepts/search/#metrics
  - https://platform.openai.com/docs/guides/embeddings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Similarity metrics and normalization

**Goal:** vector search ranks results the way the embedding model intends, and score thresholds mean something.

## The relationships
For unit-length vectors: cosine similarity = dot product, and squared L2 distance = 2 - 2 x cosine (checked numerically on random unit vectors; FAISS `IndexFlatIP` and `IndexFlatL2` returned identical top-10 lists on normalised data). So with normalised vectors all three give the same ranking; dot product is cheapest to compute.
Without normalisation they differ: dot product rewards vector magnitude (some models encode confidence or popularity in norm), L2 penalises it.

## Rule: use what the model was trained with
- Most sentence-embedding models: cosine (normalise, then dot product).
- Some models are trained for dot product and documented as such (e.g. some retrieval models with unnormalised output); normalising them can hurt.
- Many embedding models and APIs return unit-length vectors already; check and assert `np.allclose(np.linalg.norm(v, axis=1), 1)`. Measured: `all-MiniLM-L6-v2` and `intfloat/e5-small-v2` both returned raw norms of exactly 1.0 from `model.encode`, so `normalize_embeddings=True` changed nothing for them (it still matters for models without a Normalize layer). Hosted-API claim: the current OpenAI embeddings guide (fetched) no longer has a "which distance function" section, so the older statement that its vectors are unit length is unconfirmed (gated: unconfirmed, source is paywalled or blocked); assert norms yourself.
- sentence-transformers: `model.encode(texts, normalize_embeddings=True)`; `model.similarity_fn_name` shows the intended metric (ran: `cosine` for both models above) and `model.similarity(a, b)` applies it.

## Index configuration
| Store | Cosine | Dot | L2 |
|---|---|---|---|
| pgvector | `<=>` with `vector_cosine_ops` (returns distance = 1 - cos) | `<#>` (negative inner product) with `vector_ip_ops` | `<->` with `vector_l2_ops` (all from the pgvector README; the README also lists `<+>` for L1; SQL not executed here) |
| Qdrant | `Distance.COSINE` (normalises on insert: stored `[3, 0, 4]` came back as `[0.6, 0.0, 0.8]`; a `DOT` collection kept `[3.0, 0.0, 4.0]`) | `Distance.DOT` | `Distance.EUCLID` (`Distance.MANHATTAN` also exists) |
| FAISS | normalise + `IndexFlatIP` | `IndexFlatIP` | `IndexFlatL2` |
The index operator class must match the query operator or the planner cannot use the index and falls back to a sequential scan (standard Postgres behaviour; not run here).

## Thresholds
Raw similarity scores are not comparable across models (one model's 0.75 is another's 0.45), and many models have a compressed range (anisotropy) where unrelated texts still score 0.6+. Measured on four short sentences: `all-MiniLM-L6-v2` scored unrelated pairs at -0.02 to 0.12 and a paraphrase at 0.56, while `intfloat/e5-small-v2` scored the same unrelated pairs at 0.68 to 0.73 and the paraphrase at 0.85. Calibrate:
1. Label a few hundred query-document pairs as relevant / not relevant.
2. Plot score distributions for both classes; pick the threshold for your precision/recall target.
3. Re-calibrate whenever the model changes.
Prefer top-k plus a reranker over a hard threshold for RAG; use thresholds for dedupe and "no good match" detection.

## Gotchas
- Mixing vectors from different models or versions in one index produces meaningless scores - re-embed everything on model change.
- Query and document prefixes (e.g. `query:` / `passage:`) are required by some models (E5); on the one pair tested they moved the paraphrase score only from 0.858 (no prefixes) to 0.831 (`query:` vs `passage:`), so the effect varies, but follow the model card.

## Verify
- [ ] Metric matches the model card; norms checked in a test.
- [ ] Thresholds derived from labelled data for the current model version.
