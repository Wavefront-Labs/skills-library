---
id: computing-software.ai-ml-engineering.feature-engineering.binary-encoding-high-cardinality
name: binary-encoding-high-cardinality
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, binary-encoding, category-encoders, high-cardinality, base-n-encoding, categorical-encoding, hashing]
level: practitioner
status: verified
description: "Encode high-cardinality categoricals with binary or base-N encoding via category_encoders: how it works versus one-hot, hashing and target encoding, plus unseen values."
sources:
  - https://contrib.scikit-learn.org/category_encoders/binary.html
  - https://contrib.scikit-learn.org/category_encoders/basen.html
  - https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Binary encoding

Assign each category an integer, write it in binary, and use each bit as a column. 1,000 categories need ceil(log2(1001)) = 10 columns instead of 1,000 one-hot columns.

```python
import category_encoders as ce
enc = ce.BinaryEncoder(cols=["zip_code", "merchant_id"], handle_unknown="value", handle_missing="value")
X_tr = enc.fit_transform(X_train); X_va = enc.transform(X_valid)
# base-N generalisation: ce.BaseNEncoder(cols=[...], base=3)
```
- `handle_unknown="value"` maps unseen categories to all-zero bits (a dedicated code); the integer mapping comes from training order.
- Works in scikit-learn Pipelines and ColumnTransformer.
- Checked with category_encoders 2.11.1: 1,000 categories give 10 columns; codes start at 1 in training order; an unseen value gives all-zero bits; `BaseNEncoder(base=3)` gives 8 columns for 1,000 categories.

## What it does to the information
Bits mix unrelated categories: categories 5 (0101) and 7 (0111) share bits for no reason. Linear models therefore get arbitrary similarity structure; trees can still separate categories with several splits. It is a compression of one-hot, not a meaningful representation.

## Comparing encoders for high cardinality
| Encoder | Columns | Pros | Cons |
|---|---|---|---|
| One-hot | k | exact, interpretable | wide; sparse; rare levels noisy |
| One-hot + `min_frequency`/`max_categories` | small | groups rare levels | loses rare-level identity |
| Binary / base-N | log k | compact, no target needed, deterministic | arbitrary bit sharing |
| Hashing (`FeatureHasher`) | fixed | streaming, no fitting, handles unseen | collisions, not invertible |
| Target / mean encoding (`TargetEncoder`) | 1 per class | very informative | leakage risk; needs cross-fitting |
| Count / frequency | 1 | simple, unsupervised | ties distinct categories with same counts |
| Native categorical (LightGBM, CatBoost, HistGB) | 0 extra | best for GBMs | model-specific |
| Learned embeddings | d | captures similarity | needs NN training |

## When binary encoding is a reasonable choice
- Tree models where native categorical support is unavailable and target encoding is undesirable (no target leakage risk, unsupervised).
- Memory-constrained pipelines with many medium-cardinality columns.
For linear models prefer one-hot with rare-level grouping or target encoding; for GBMs prefer native categorical handling.

## Gotchas
- Category-to-integer mapping must be persisted with the model; refitting on new data reorders codes and silently changes meaning.
- Ordinal relationships are not preserved; if categories are ordered, use an ordinal encoding instead.

## Verify
Compare CV scores of binary vs one-hot (with min_frequency) vs target encoding on the same model; pick the simplest one within noise of the best.
