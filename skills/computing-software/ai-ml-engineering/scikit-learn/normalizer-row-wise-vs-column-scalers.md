---
id: computing-software.ai-ml-engineering.scikit-learn.normalizer-row-wise-vs-column-scalers
name: normalizer-row-wise-vs-column-scalers
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, normalizer, row-normalization, l2-normalization, cosine-similarity, feature-scaling, tf-idf]
level: practitioner
status: verified
description: "Know when to use scikit-learn Normalizer (per-sample unit norm) instead of column scalers, for text vectors, cosine-similarity models and combining with StandardScaler."
sources:
  - https://scikit-learn.org/stable/modules/preprocessing.html#normalization
  - https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.Normalizer.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Normalizer (row-wise) vs column scalers

**Column scalers** (`StandardScaler`, `MinMaxScaler`, `RobustScaler`) learn statistics per feature across samples and make features comparable to each other.

**`Normalizer`** rescales each *sample* (row) to unit norm. It learns nothing from the data (`fit` only records `n_features_in_`), so it cannot leak, and it changes the geometry: only the direction of each row vector remains.

```python
from sklearn.preprocessing import Normalizer
X_unit = Normalizer(norm="l2").fit_transform(X)     # each row ||x||_2 = 1 ; "l1" or "max" also available
```
Works on sparse matrices without densifying.

## When to use it
- **Text / count vectors** where document length should not matter: TF-IDF already applies `norm="l2"` by default (`TfidfVectorizer(norm="l2")`), so adding Normalizer is redundant. Do not assume raw `CountVectorizer` output benefits: on a 4-class 20 newsgroups subset (3-fold CV accuracy) `Normalizer` after `CountVectorizer` lowered logistic regression from 0.780 to 0.762 and KNN from 0.423 to 0.407, so test it. `Normalizer` after `TfidfVectorizer` changed nothing (outputs identical).
- **Cosine similarity models**: with unit rows, Euclidean distance and dot product are monotone in cosine similarity: `||a-b||^2 = 2 - 2 cos(a, b)`. KMeans on normalised vectors approximates spherical k-means; KNN with euclidean on normalised data equals cosine ranking.
- **Embeddings** (sentence embeddings, image features) before nearest-neighbour search or clustering.
- **Compositional data / proportions** where only relative amounts matter (`norm="l1"`).

## When not
- Tabular features with different units (age, income): row norms mix units meaninglessly. Use column scalers.
- Dense features where magnitude carries signal (total spend): normalising throws that away. Keep the norm as an extra feature if needed:
```python
norms = np.linalg.norm(X, axis=1, keepdims=True)
X_aug = np.hstack([X / norms, np.log1p(norms)])
```

## Combining
Order matters: `StandardScaler` then `Normalizer` makes features comparable first, then projects rows to the unit sphere. The reverse is rarely what you want. Zero rows stay zero (no division error; checked for l2, l1 and max). All three norms gave row norm 1 on non-zero rows, and sparse input stays sparse (`csr`).

## Verify
`np.allclose(np.linalg.norm(X_unit, axis=1), 1)` for non-zero rows, and compare model CV score with and without the step inside a Pipeline.
