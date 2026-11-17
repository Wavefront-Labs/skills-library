---
id: computing-software.ai-ml-engineering.feature-engineering.bertopic-topic-features
name: bertopic-topic-features
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, bertopic, topic-modeling, text-features, sentence-embeddings, hdbscan, topic-distributions]
level: practitioner
status: draft
description: "Build topic features from text with BERTopic: embeddings + UMAP + HDBSCAN + c-TF-IDF, topic distributions as model features, outlier reduction and leakage-safe fitting."
sources:
  - https://maartengr.github.io/BERTopic/
  - https://maartengr.github.io/BERTopic/getting_started/distribution/distribution.html
  - https://arxiv.org/abs/2203.05794
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Topic model features (BERTopic)

BERTopic clusters document embeddings and describes clusters with class-based TF-IDF, giving coherent topics for short and long texts. Topic assignments and distributions become features for downstream models or analysis.

## Fit
```python
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
emb_model = SentenceTransformer("all-MiniLM-L6-v2")
emb_train = emb_model.encode(train_docs, batch_size=64, show_progress_bar=True)
topic_model = BERTopic(embedding_model=emb_model,
    umap_model=UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric="cosine", random_state=42),
    hdbscan_model=HDBSCAN(min_cluster_size=30, metric="euclidean", prediction_data=True),
    vectorizer_model=CountVectorizer(stop_words="english", min_df=5, ngram_range=(1, 2)),
    calculate_probabilities=True)
topics, probs = topic_model.fit_transform(train_docs, emb_train)
topic_model.get_topic_info().head(20)
```
- `random_state` on UMAP makes runs reproducible (and slower, single-threaded).
- Topic -1 is HDBSCAN's outlier group; often 20-50% of docs.

## Features
- **Topic id** (categorical): `topic_model.transform(docs, emb)` for new docs.
- **Topic distribution** (dense vector): `calculate_probabilities=True` gives HDBSCAN soft membership; or `topic_model.approximate_distribution(docs)` for token-window based distributions, better for multi-topic documents.
- Reduce outliers: `new_topics = topic_model.reduce_outliers(docs, topics, strategy="embeddings")`, then `update_topics`.
- Combine with the raw embedding itself; topics add interpretability, embeddings often add more accuracy.

## Leakage-safe use
Fit BERTopic on training documents only (or on a large unlabelled corpus excluding test), then `transform` validation/test. Fitting on all documents leaks cluster structure from test data, and topics shift between refits, so persist the fitted model (`topic_model.save("bt", serialization="safetensors", save_ctfidf=True, save_embedding_model=emb_name)`).

## Controlling granularity
- `min_cluster_size` larger -> fewer, broader topics.
- `nr_topics="auto"` or `reduce_topics(docs, nr_topics=30)` merges similar topics.
- Hierarchical view: `topic_model.hierarchical_topics(docs)`.
- Guided/seeded topics with `seed_topic_list` when you know categories in advance.

## Evaluate
Inspect top words and representative docs per topic (`get_representative_docs`), topic sizes, coherence (c_npmi via gensim), and downstream lift from topic features in CV. Over time, `topics_over_time` shows trend features.
