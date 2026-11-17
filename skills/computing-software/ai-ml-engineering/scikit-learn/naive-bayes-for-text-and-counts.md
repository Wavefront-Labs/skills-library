---
id: computing-software.ai-ml-engineering.scikit-learn.naive-bayes-for-text-and-counts
name: naive-bayes-for-text-and-counts
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, multinomialnb, complementnb, naive-bayes, text-classification, bernoullinb, gaussiannb]
level: practitioner
status: verified
description: "Use scikit-learn Naive Bayes for text and count data: MultinomialNB vs ComplementNB vs BernoulliNB, alpha smoothing, imbalance, calibration and partial_fit."
sources:
  - https://scikit-learn.org/stable/modules/naive_bayes.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.ComplementNB.html
  - https://people.csail.mit.edu/jrennie/papers/icml03-nb.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Naive Bayes for text and counts

Fast, strong baselines for bag-of-words text, trainable in seconds on millions of documents.

## Pick the variant
| Model | Features | Notes |
|---|---|---|
| `MultinomialNB` | counts or TF-IDF | classic text classifier |
| `ComplementNB` | counts / TF-IDF | estimates from the complement of each class; better on imbalanced text (Rennie et al. 2003); often beats MultinomialNB |
| `BernoulliNB` | binary presence | short texts; penalises absent words explicitly; `binarize=0.0` |
| `CategoricalNB` | integer-coded categories | tabular categorical |
| `GaussianNB` | continuous | weak on most real data; baseline only |

## Pipeline
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB
pipe = make_pipeline(TfidfVectorizer(sublinear_tf=True, min_df=2, ngram_range=(1, 2)), ComplementNB())
grid = {"complementnb__alpha": [0.01, 0.1, 0.3, 1.0], "tfidfvectorizer__ngram_range": [(1, 1), (1, 2)]}
GridSearchCV(pipe, grid, cv=5, scoring="f1_macro").fit(texts, y)
```
- `alpha` (Laplace/Lidstone smoothing) is the main hyperparameter; default 1.0 is often too strong for large vocabularies (macro-F1 on the subset: MultinomialNB 0.880 at alpha 1.0 vs 0.896 at 0.01; ComplementNB 0.898 vs 0.904; the grid picked 0.3).
- Features must be non-negative: `MultinomialNB` raises `Negative values in data passed to MultinomialNB (input X)` after `TruncatedSVD`, and for the same reason after `HashingVectorizer()` with its default `alternate_sign=True`. A sparse TF-IDF matrix cannot go through a default `StandardScaler` (`Cannot center sparse matrices: pass with_mean=False`); TF-IDF and counts need no scaling.

## Imbalance and priors
- `fit_prior=True` learns class priors from data; with heavy imbalance the majority class dominates. Options: ComplementNB, `class_prior=[...]` set explicitly, or tune the decision threshold.
- `sample_weight` in `fit` is supported.

## Probabilities
NB probabilities are poorly calibrated, and the direction depends on the features. On a 4-class 20 newsgroups subset (`fetch_20newsgroups`, headers/footers/quotes removed): `MultinomialNB` on raw counts was overconfident (82% of test rows with max probability above 0.99, log loss 1.24, accuracy 0.865), while on TF-IDF it was underconfident (mean max probability 0.63 at accuracy 0.88, log loss 0.565, which `CalibratedClassifierCV(method="sigmoid", cv=3)` cut to 0.338). Rank order is usable; if you need probabilities, wrap in `CalibratedClassifierCV(pipe, method="sigmoid", cv=5)`.

## Streaming
`partial_fit(X_batch, y_batch, classes=all_classes)` for out-of-core training; combine with `HashingVectorizer(alternate_sign=False)` (NB needs non-negative features).

## Interpreting
`model.feature_log_prob_` (classes x vocab) gives per-class token weights, but the raw top tokens per class are stop words (`the`, `to`, `of`, `and` for every class in the run above). Rank by the difference from the other classes instead: `np.argsort(lp[k] - np.delete(lp, k, 0).mean(0))[-20:]` with `lp = model.feature_log_prob_`, mapped through `vectorizer.get_feature_names_out()`; that gave `orbit, spacecraft, lunar, moon, solar` for sci.space.

## When to move on
If a linear SVM or logistic regression on the same TF-IDF beats NB by several points, use those (on the subset above ComplementNB macro-F1 0.905 vs LinearSVC 0.898 vs LogisticRegression 0.885, so NB was not behind); NB stays useful as a sanity baseline and for very small training sets.
