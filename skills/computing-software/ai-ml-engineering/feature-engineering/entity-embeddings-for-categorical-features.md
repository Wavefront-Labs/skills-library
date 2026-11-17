---
id: computing-software.ai-ml-engineering.feature-engineering.entity-embeddings-for-categorical-features
name: entity-embeddings-for-categorical-features
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, categorical-encoding, entity-embeddings, embedding-layers, high-cardinality, tabular-deep-learning]
level: practitioner
status: draft
description: "Learn dense embeddings for high-cardinality categoricals in neural nets, size them, handle unknowns, and reuse them as features in gradient-boosted models."
sources:
  - https://arxiv.org/abs/1604.06737
  - https://docs.fast.ai/tabular.model.html
  - https://pytorch.org/docs/stable/generated/torch.nn.Embedding.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Entity embeddings for categorical features

**Goal:** represent categories like store ID, product, or ZIP code as learned vectors that capture similarity, instead of thousands of one-hot columns.

## Model
```python
class TabularNet(nn.Module):
    def __init__(self, cardinalities, n_num):
        super().__init__()
        dims = [min(50, (c + 1) // 2) for c in cardinalities]       # fast.ai-style rule of thumb
        self.embs = nn.ModuleList(nn.Embedding(c + 1, d) for c, d in zip(cardinalities, dims))  # +1 for unknown
        self.drop = nn.Dropout(0.1)
        self.mlp = nn.Sequential(nn.Linear(sum(dims) + n_num, 256), nn.ReLU(), nn.Linear(256, 1))
    def forward(self, x_cat, x_num):
        e = torch.cat([emb(x_cat[:, i]) for i, emb in enumerate(self.embs)], dim=1)
        return self.mlp(torch.cat([self.drop(e), x_num], dim=1))
```
- Encode each category to an integer index fitted on training data; reserve index 0 for unknown/rare values so unseen categories at serving don't crash.
- Size: `min(50, (n+1)//2)` (fast.ai) or `round(1.6 * n**0.56)` (fast.ai's later heuristic, capped around 600). Too large overfits rare categories.
- Embedding dropout (or dropping whole categories to "unknown" with small probability during training) teaches the model a useful unknown vector.

## Reusing embeddings in other models
Guo & Berkhahn (2016) showed embeddings learned by a NN improved KNN, random forests and GBMs when used as input features. Extract `emb.weight[idx]` per row and add the vector as numeric columns. Learn the embeddings using training folds only; using the whole dataset leaks the target into the features.

## When to use
- High-cardinality categoricals with many rows per category and meaningful similarity between categories (stores, products, users).
- For GBMs alone, target encoding or native categorical handling is usually cheaper and just as strong; embeddings pay off when you are already training a NN or need similarity (nearest-neighbour lookups, clustering).

## Gotchas
- Categories with very few rows get near-random vectors; collapse them to a rare bucket (threshold e.g. < 20 rows).
- Index mapping must be versioned with the model; a reordered mapping silently scrambles every prediction.
- Inspect embeddings (PCA/t-SNE coloured by known attributes); if similar stores aren't near each other, the embedding learned nothing useful.

## Verify
- [ ] Unknown-category handling tested with an unseen value.
- [ ] Category-to-index mapping saved alongside the model.
- [ ] Ablation vs one-hot/target encoding shows the gain.
