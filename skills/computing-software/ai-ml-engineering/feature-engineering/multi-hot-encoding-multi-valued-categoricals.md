---
id: computing-software.ai-ml-engineering.feature-engineering.multi-hot-encoding-multi-valued-categoricals
name: multi-hot-encoding-multi-valued-categoricals
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, multi-hot-encoding, multilabelbinarizer, multi-valued-features, tags-features, countvectorizer, embedding-bag]
level: practitioner
status: verified
description: "Encode multi-valued categorical fields (tags, genres, item lists) as multi-hot or count vectors with MultiLabelBinarizer or CountVectorizer, weighting, rare values and embeddings."
sources:
  - https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MultiLabelBinarizer.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
  - https://pytorch.org/docs/stable/generated/torch.nn.EmbeddingBag.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multi-valued categorical features (multi-hot)

A row may have several values in one field: a movie's genres, a product's tags, the set of apps installed. One-hot assumes one value; multi-hot sets a 1 for each present value.

## scikit-learn
```python
from sklearn.preprocessing import MultiLabelBinarizer
df["tags"] = df["tags_str"].fillna("").str.split("|").apply(lambda xs: [x.strip().lower() for x in xs if x])
mlb = MultiLabelBinarizer(sparse_output=True)
T_train = mlb.fit_transform(train["tags"]); T_valid = mlb.transform(valid["tags"])   # unseen tags ignored with a warning ("unknown class(es) [...] will be ignored", checked)
```
`MultiLabelBinarizer` is designed for targets and does not plug directly into ColumnTransformer (it takes one column of lists). For pipelines, use `CountVectorizer` with a custom analyzer:
```python
from sklearn.feature_extraction.text import CountVectorizer
tag_vec = CountVectorizer(analyzer=lambda s: s.split("|") if isinstance(s, str) else [], binary=True, min_df=5)
ct = ColumnTransformer([("tags", tag_vec, "tags_str"), ("num", StandardScaler(), num_cols)])
```
`min_df` drops rare tags; `max_features` caps vocabulary; `binary=False` gives counts if repeats matter.

## Weighting and normalisation
- Rows with many values get many ones; normalise if the number of values should not dominate (`TfidfTransformer` or L2 `Normalizer`), and add the count of values as its own feature.
- TF-IDF weighting down-weights very common tags.

## High cardinality
- Thousands of tags: keep top-N by frequency, hash the rest (`HashingVectorizer`), or reduce with TruncatedSVD.
- Group rare tags into "other" before encoding.

## Neural nets
Use an embedding bag (mean or sum of tag embeddings):
```python
bag = torch.nn.EmbeddingBag(num_tags, 32, mode="mean", padding_idx=0)
vec = bag(tag_ids_flat, offsets)           # (batch, 32)
```
In Keras: `Embedding` + masking + `GlobalAveragePooling1D`, or `StringLookup(output_mode="multi_hot")` for the multi-hot vector directly (its first `num_oov_indices` columns are OOV slots).

## Derived features
- Count of values, presence of key tags, Jaccard similarity to user's historical tags, share of tags in a category.

## Gotchas
- Normalise spelling and case before encoding (`"Sci-Fi"` vs `"scifi"`).
- Order inside lists is lost by design; if order matters (sequence of visited pages), use sequence models instead.
- Fit vocabulary on training data only.
