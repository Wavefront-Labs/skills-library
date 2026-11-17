---
id: computing-software.ai-ml-engineering.feature-engineering.handcrafted-text-statistics-features
name: handcrafted-text-statistics-features
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, text-features, text-statistics-features, readability, stylometric-features, meta-features]
level: practitioner
status: draft
description: "Add cheap text statistics (length, casing, punctuation, URLs, readability, lexical diversity) alongside TF-IDF or embeddings, and check them for dataset artifacts."
sources:
  - https://scikit-learn.org/stable/modules/compose.html#columntransformer-for-heterogeneous-data
  - https://github.com/textstat/textstat
  - https://aclanthology.org/N18-2017/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Handcrafted text statistics features

**Goal:** capture style and structure signals that bag-of-words and embeddings miss, at almost no cost.

## Useful features
```python
import re, numpy as np, pandas as pd
def text_stats(s: pd.Series) -> pd.DataFrame:
    words = s.str.split()
    return pd.DataFrame({
        "n_chars": s.str.len(),
        "n_words": words.str.len(),
        "avg_word_len": s.str.len() / words.str.len().clip(lower=1),
        "upper_ratio": s.str.count(r"[A-Z]") / s.str.len().clip(lower=1),
        "n_exclaim": s.str.count("!"),
        "n_question": s.str.count(r"\?"),
        "n_urls": s.str.count(r"https?://"),
        "n_digits_ratio": s.str.count(r"\d") / s.str.len().clip(lower=1),
        "type_token_ratio": words.map(lambda w: len(set(w)) / max(len(w), 1)),
    })
```
Plus domain-specific: number of line items, presence of a phone number, mentions of competitor names, readability scores (`textstat.flesch_reading_ease`) for content-quality tasks.

Spam, abuse, fraud and quality tasks benefit most (all-caps, many links, excessive punctuation).

## Combine with text vectors
```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer, StandardScaler
pre = ColumnTransformer([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2), "text"),
    ("stats", make_pipeline(FunctionTransformer(lambda X: text_stats(X.iloc[:, 0])), StandardScaler()), ["text"]),
])
```
Scale the statistics (log-transform counts) for linear models; trees don't need it.

## Check for artifacts
Simple statistics can reveal dataset artifacts rather than real signal - e.g. in NLI datasets, hypothesis length and certain words predicted labels without reading the premise (Gururangan et al., 2018). If `n_chars` alone gets high AUC, ask whether that holds in production or reflects how the dataset was collected (labelled examples from one source being longer).

## Verify
- [ ] Each statistic's single-feature predictive power reviewed for artifacts.
- [ ] Ablation shows stats add over TF-IDF/embeddings.
- [ ] Computed by the same function at serving time.
