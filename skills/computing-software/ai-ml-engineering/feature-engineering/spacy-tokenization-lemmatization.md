---
id: computing-software.ai-ml-engineering.feature-engineering.spacy-tokenization-lemmatization
name: spacy-tokenization-lemmatization
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, spacy, lemmatization, tokenization, stemming, text-preprocessing, nlp-pipeline]
level: practitioner
status: draft
description: "Preprocess text for classical NLP features with spaCy: lean pipelines, nlp.pipe batching, lemmas vs stems, stopword care, and when transformers need none of it."
sources:
  - https://spacy.io/usage/linguistic-features
  - https://spacy.io/usage/processing-pipelines
  - https://www.nltk.org/api/nltk.stem.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Tokenization, stemming and lemmatization with spaCy

**When this matters:** bag-of-words/TF-IDF models, keyword extraction, rule-based features and search indexing. Transformer models use their own subword tokenizers: do not lemmatize or remove stopwords before feeding them.

## Efficient pipeline
```python
import spacy
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])   # keep tagger + lemmatizer only
def lemmatize_docs(texts):
    out = []
    for doc in nlp.pipe(texts, batch_size=1000, n_process=4):
        out.append(" ".join(t.lemma_.lower() for t in doc
                            if not (t.is_stop or t.is_punct or t.is_space or t.like_num)))
    return out
```
- `nlp.pipe` with batching is 10-100x faster than calling `nlp(text)` in a loop.
- Disable components you do not need; the lemmatizer depends on POS tags (keep `tagger`/`attribute_ruler`).
- Multiprocessing (`n_process`) pays off for large corpora; watch memory.

## Lemma vs stem
- Lemmatization ("better" -> "good", "running" -> "run") uses vocabulary and POS; produces real words; slower.
- Stemming (NLTK `SnowballStemmer("english")`) chops suffixes ("studies" -> "studi"); fast and language-agnostic-ish; fine for retrieval features.

## Stopwords and domain terms
Default stopword lists remove negations ("not", "no") that matter for sentiment: customize (`nlp.Defaults.stop_words -= {"not", "no"}`). Keep domain tokens (product codes) intact with tokenizer exceptions or custom regex.

## In sklearn
Wrap as a FunctionTransformer or pass `tokenizer=`/`preprocessor=` to `TfidfVectorizer` (set `token_pattern=None` when using a custom tokenizer). Precompute lemmas once and cache; spaCy inside CV loops is slow.

## Verify
- [ ] Compare CV score of TF-IDF on raw lowercase tokens vs lemmatized vs stemmed; keep the simplest that wins.
