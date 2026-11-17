---
id: computing-software.ai-ml-engineering.feature-engineering.tfidf-vectorizer-tuning
name: tfidf-vectorizer-tuning
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, text-features, tf-idf, tfidfvectorizer, n-grams, char-ngrams, hashingvectorizer, text-classification]
level: practitioner
status: verified
description: "Build strong sparse text features with TfidfVectorizer: word and char n-grams, min_df/max_df, sublinear tf, vocabulary size, HashingVectorizer for streams, and linear baselines."
sources:
  - https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction
  - https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
  - https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TfidfVectorizer tuning

**Goal:** a fast, strong text baseline (often hard to beat on short-text classification with little data) and good sparse features for linear models.

## A solid starting point
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline, make_union
from sklearn.linear_model import LogisticRegression

word = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.9, sublinear_tf=True, strip_accents="unicode")
char = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=3, sublinear_tf=True)
pipe = make_pipeline(make_union(word, char), LogisticRegression(C=4, max_iter=2000))
```
- `ngram_range=(1, 2)`: bigrams capture negation and phrases ("not good").
- `min_df`: drop terms in fewer than N docs (noise, typos, IDs); `max_df`: drop near-ubiquitous terms (corpus-specific stop words).
- `sublinear_tf=True`: `1 + log(tf)` - repeated words don't dominate.
- `char_wb` n-grams: robust to typos, morphology, and unknown words; very effective for short noisy text and languages with rich morphology.
- `max_features` caps vocabulary by frequency when memory matters.
- Default L2 normalisation per document; leave it on for linear models.

## Tuning
Search `C`, `ngram_range`, `min_df`, `sublinear_tf` jointly in a pipeline with `GridSearchCV`; the vectorizer is fitted per fold (vocabulary/IDF from training folds only). Use pipeline caching to avoid re-vectorising for every `C`.

## Large or streaming data
`HashingVectorizer(n_features=2**20, alternate_sign=False, ngram_range=(1, 2))` + `TfidfTransformer` (or none): no vocabulary to store, works with `partial_fit` models, but no feature names and possible hash collisions.

## Inspecting
For linear models, `get_feature_names_out()` with coefficients lists the top terms per class - a fast sanity check for leakage (e.g. a signature line or ticket template text predicting the label).

## Gotchas
- Default `token_pattern` drops single-character tokens (checked: `TfidfVectorizer().fit(["C and R"])` keeps only `and`); change it if "C" or "R" matter.
- Stop-word lists remove negations ("not", "no") that matter for sentiment; usually skip `stop_words="english"`.
- Vocabulary is frozen at fit time: new jargon is ignored until retraining (char n-grams degrade more gracefully).

## Verify
- [ ] Vectorizer inside the CV pipeline.
- [ ] Top-weighted terms reviewed for leakage.
- [ ] Compared against an embedding-based model before choosing heavier approaches.
