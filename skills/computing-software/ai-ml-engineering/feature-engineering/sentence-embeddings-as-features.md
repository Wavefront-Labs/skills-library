---
id: computing-software.ai-ml-engineering.feature-engineering.sentence-embeddings-as-features
name: sentence-embeddings-as-features
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, text-features, sentence-embeddings, sentence-transformers, embedding-features, setfit, text-classification]
level: practitioner
status: draft
description: "Use pretrained sentence embeddings as model features: encoder choice, prefixes and normalization, caching, dimensionality reduction for GBMs, and SetFit fine-tuning."
sources:
  - https://sbert.net/docs/sentence_transformer/usage/usage.html
  - https://huggingface.co/spaces/mteb/leaderboard
  - https://github.com/huggingface/setfit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sentence embeddings as features

**Goal:** dense semantic features from text that work with classic models (logistic regression, GBMs, clustering) and need little labelled data.

## Encode
```python
from sentence_transformers import SentenceTransformer
enc = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cuda")
E = enc.encode(texts, batch_size=256, normalize_embeddings=True, show_progress_bar=True)   # (n, 384)
```
- Choose by task and language from the MTEB leaderboard (classification/clustering scores), then by size/latency. Small models (~384 dims) are often enough for features; multilingual models for mixed-language data.
- Some models need **prefixes** (e5: `"query: "`/`"passage: "`; instruction-tuned models need a task instruction) - wrong prefixes silently cost accuracy.
- Long texts are truncated at the model's max sequence length (often 256-512 tokens); chunk and average for long documents.

## Use as features
```python
clf = LogisticRegression(C=1.0, max_iter=2000).fit(E_train, y_train)
```
- Linear models on normalised embeddings are a strong baseline.
- For GBMs, many dense dims make trees slow and less effective; reduce with PCA/TruncatedSVD (fit on train) to 32-64 dims, or combine embedding-based model predictions as a single stacked feature (out-of-fold).
- Combine with tabular features via `ColumnTransformer`/`hstack`; scale considerations differ (embeddings already normalised).

## Operational concerns
- Cache embeddings keyed by (text hash, model name, model version); recomputing is the main cost.
- Record the encoder name and revision with the downstream model; changing the encoder invalidates the downstream model.
- Serving latency: encoder inference dominates; batch requests, use ONNX/quantized encoders on CPU.

## Few labels? Fine-tune contrastively
SetFit fine-tunes a sentence transformer on pairs built from few labelled examples (8-64 per class) and then trains a head; often much better than frozen embeddings + LR when labels are scarce.

## Verify
- [ ] Encoder choice and prefix usage documented; revision pinned.
- [ ] Compared with TF-IDF baseline on the same CV folds.
- [ ] Embedding cache invalidates on model change.
