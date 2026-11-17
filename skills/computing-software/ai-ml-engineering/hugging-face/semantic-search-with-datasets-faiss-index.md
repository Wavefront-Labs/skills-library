---
id: computing-software.ai-ml-engineering.hugging-face.semantic-search-with-datasets-faiss-index
name: semantic-search-with-datasets-faiss-index
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, datasets, faiss-index, add-faiss-index, get-nearest-examples, semantic-search, embeddings]
level: practitioner
status: verified
description: "Build semantic search over a Hugging Face Dataset: embed with map, add_faiss_index, query get_nearest_examples, cosine vs L2, save/load the index and scaling limits."
sources:
  - https://huggingface.co/learn/llm-course/chapter5/6
  - https://huggingface.co/docs/datasets/faiss_es
  - https://github.com/facebookresearch/faiss/wiki/Faiss-indexes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Semantic search with Datasets and FAISS

**Goal:** quick nearest-neighbour search over a dataset's embeddings for retrieval prototypes, dedup or example lookup - without standing up a vector database.

## Embed
```python
from sentence_transformers import SentenceTransformer
enc = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cuda")
ds = ds.map(lambda b: {"emb": enc.encode(b["text"], batch_size=128, normalize_embeddings=True)},
            batched=True, batch_size=1024)
```
`normalize_embeddings=True` makes inner product equal cosine similarity.

## Index and query
```python
import faiss
ds.add_faiss_index(column="emb", metric_type=faiss.METRIC_INNER_PRODUCT)
q = enc.encode(["how do I reset my password"], normalize_embeddings=True)[0]
scores, hits = ds.get_nearest_examples("emb", q, k=5)
for s, t in zip(scores, hits["text"]):
    print(round(float(s), 3), t[:80])
```
- Default index is exact (flat) search with L2 distance (checked: `IndexFlat`; a near-duplicate query scored 0.012 versus 0.994 with `METRIC_INNER_PRODUCT` on normalised all-MiniLM-L6-v2 embeddings) - lower score is better for L2, higher is better for inner product. Mixing up the two inverts your ranking.
- Query vectors must have the same dimension and normalisation as the indexed ones; use float32 NumPy arrays (a float64 query also worked in datasets 5.1).
- `get_nearest_examples_batch` for many queries at once.

## Approximate indexes for scale
```python
ds.add_faiss_index(column="emb", string_factory="IVF1024,Flat", metric_type=faiss.METRIC_INNER_PRODUCT,
                   train_size=100_000)
ds.get_index("emb").faiss_index.nprobe = 16       # recall/speed knob
```
Flat search is exact but scans every vector, so cost grows linearly with dataset size (a ~1M-vector threshold is a rule of thumb, not measured here); beyond that consider IVF/HNSW indexes or a vector DB. The IVF16 variant of the snippet (`string_factory="IVF16,Flat"`, `train_size=2000`, `nprobe=4`) ran on 3,000 random vectors.

## Persist
```python
ds.save_faiss_index("emb", "emb.faiss")
ds.drop_index("emb")                     # required before save_to_disk (checked: it raises ValueError "please remove all the indexes using `dataset.drop_index` before saving a dataset")
ds.load_faiss_index("emb", "emb.faiss")
```
The index isn't saved with the dataset; store it separately and keep row order identical.

## Gotchas
- `add_faiss_index` needs `faiss-cpu` or `faiss-gpu` installed.
- `shuffle`, `filter` and `select` on a dataset with an attached index raise `DatasetTransformationNotAllowedError` (checked in datasets 5.1; `map` is allowed and drops the index from the result), so transform first and build the index last.
- Use the same model for queries and documents; asymmetric retrieval models document their own query/passage prefixes on their model cards, so follow the card.

## Verify
- [ ] Known-relevant queries return expected rows in the top 5.
- [ ] Metric type and score direction documented.
- [ ] Index file versioned with the embedding model name.
