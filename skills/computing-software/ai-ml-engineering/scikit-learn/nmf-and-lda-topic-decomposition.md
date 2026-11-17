---
id: computing-software.ai-ml-engineering.scikit-learn.nmf-and-lda-topic-decomposition
name: nmf-and-lda-topic-decomposition
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, nmf, latent-dirichlet-allocation, topic-modeling, matrix-factorization, text-mining, decomposition]
level: practitioner
status: gated
description: "Extract topics from text with scikit-learn NMF and LatentDirichletAllocation: vectoriser setup, choosing n_components, top words per topic, document-topic features."
sources:
  - https://scikit-learn.org/stable/modules/decomposition.html#non-negative-matrix-factorization-nmf-or-nnmf
  - https://scikit-learn.org/stable/modules/decomposition.html#latent-dirichlet-allocation-lda
  - https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NMF and LDA topic decomposition

Both factor a document-term matrix into documents x topics and topics x terms with non-negative weights.

## Inputs differ
- **NMF**: TF-IDF works best. `TfidfVectorizer(max_df=0.95, min_df=2, stop_words="english", max_features=20000)`.
- **LDA**: raw counts (it is a probabilistic model of word counts). `CountVectorizer(...)` with the same filtering.

## Fit
```python
from sklearn.decomposition import NMF, LatentDirichletAllocation
nmf = NMF(n_components=20, init="nndsvda", beta_loss="frobenius", alpha_W=0.0, l1_ratio=0.0, max_iter=400, random_state=0)
W = nmf.fit_transform(tfidf)          # docs x topics
H = nmf.components_                   # topics x terms
lda = LatentDirichletAllocation(n_components=20, learning_method="online", batch_size=512,
                                doc_topic_prior=None, topic_word_prior=None, random_state=0, n_jobs=-1)
theta = lda.fit_transform(counts)     # rows sum to 1
```
- NMF with `beta_loss="kullback-leibler"` needs `solver="mu"`; with the default `solver="cd"` it raises `Invalid beta_loss parameter: solver 'cd' does not handle beta_loss = 'kullback-leibler'` (checked 1.9.1). It behaves closer to probabilistic topic models.
- LDA `learning_method="online"` scales to large corpora; the default is `"batch"`. `partial_fit` ran on the fitted online model. `fit_transform` rows sum to 1 (checked). On the 2236-document subset with 8 topics, top NMF words per topic were clean (`space, nasa, shuttle, launch, orbit`; `car, cars, dealer, engine`).

## Top words
```python
terms = vec.get_feature_names_out()
for k, comp in enumerate(H):
    print(k, ", ".join(terms[i] for i in comp.argsort()[-12:][::-1]))
```

## Choosing n_components
- No single correct value. Fit 10/20/40, read top words, and check topic coherence (gensim `CoherenceModel` with `c_v` or `c_npmi`) for a quantitative signal (gated: unconfirmed, source is paywalled or blocked). Gensim has no wheel for Python 3.14 here and was not run; verify the coherence names in its docs.
- LDA `perplexity()` is not a safe way to pick the number of topics. On a 4-class 20 newsgroups subset (online LDA, `max_iter=10`) held-out perplexity got worse as topics were added: 13600 at 4 topics, 20500 at 10, 28300 at 20, 43100 at 40. Do not choose the topic count by minimising it; prefer coherence plus reading the top words.
- Duplicate or junk topics (dates, boilerplate) indicate too many topics or missing stop words.

## Use as features
`W` / `theta` are dense low-dimensional document features for classifiers or clustering. Fit the decomposition inside the Pipeline so CV does not leak vocabulary or topic structure from validation docs.

## Practical tips
- Preprocess consistently (lowercase, lemmatise, remove boilerplate); topics reflect cleaning choices more than algorithm choice.
- Results vary with `random_state`; check stability over seeds.
- For short texts or semantic topics, embedding-based BERTopic often gives more coherent topics, at higher cost (gated: unconfirmed, source is paywalled or blocked). Not run here.
