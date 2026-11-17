---
id: computing-software.cloud-infrastructure-engineering.google-cloud.firestore-vector-search-and-knn-queries
name: firestore-vector-search-and-knn-queries
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, firestore, firestore-vector-search, knn, embeddings, rag]
level: practitioner
status: docs-checked
description: "Store embeddings in Firestore, create vector indexes with gcloud, run find_nearest KNN queries with prefilters, and know the dimension, distance and result limits."
sources: ["https://docs.cloud.google.com/firestore/docs/vector-search", "https://github.com/googleapis/google-cloud-python/blob/main/packages/google-cloud-firestore/google/cloud/firestore_v1/base_vector_query.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firestore vector search

## 1. Store vectors
```python
from google.cloud.firestore_v1.vector import Vector
db.collection("docs").add({"text": t, "lang": "en", "embedding": Vector(emb)})  # emb: list[float]
```
Wrap embeddings in the `Vector` type; Firestore does not generate embeddings, so produce them with an embedding model.

## 2. Create the vector index
```bash
gcloud firestore indexes composite create --collection-group=docs --query-scope=collection \
  --field-config=field-path=lang,order=ascending \
  --field-config=field-path=embedding,vector-config='{dimension=768,flat}' \
  --database='(default)'
```
- Prefilter fields (here `lang`) go before the vector field in the same composite index.
- Maximum dimension is 2048; the index `dimension` must match your embedding model's output.
- The vector index type is `flat`.
- Index builds are asynchronous: poll `gcloud firestore indexes composite list` until the index is ready.

## 3. Query
```python
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
q = (db.collection("docs").where("lang", "==", "en")
       .find_nearest(vector_field="embedding", query_vector=Vector(qemb),
                     distance_measure=DistanceMeasure.COSINE, limit=10,
                     distance_result_field="dist"))
for d in q.stream(): print(d.id, d.get("dist"))
```
- Distance measures: `EUCLIDEAN`, `COSINE`, `DOT_PRODUCT`. With normalised vectors all three give the same ordering and `DOT_PRODUCT` is usually the most efficient; with non-normalised vectors test `COSINE` or `EUCLIDEAN`. If unsure, use `COSINE`.
- Nearest-neighbour queries return at most 1000 documents (Standard edition). `distance_threshold` keeps results at or below the threshold for `EUCLIDEAN` and `COSINE`, and at or above it for `DOT_PRODUCT`.
- Vector search does not support real-time snapshot listeners.

## Gotchas
- Prefiltering with `where()` before `find_nearest()` needs a composite vector index that includes the prefilter fields.
- Re-embedding with a model of a different dimension needs a new field and a new index; switch queries once it is ready.

## Verify
- [ ] Querying with a stored document's own vector returns that document first with a near-zero distance.

## Checked
Checked 2026-10-24 against the Firestore vector search documentation, the gcloud `firestore indexes composite create` reference and the google-cloud-python `google-cloud-firestore` `base_query.py`, `base_vector_query.py` (`find_nearest` signature, `DistanceMeasure` members) (docs.cloud.google.com, GitHub). Confirmed `Vector`, the flat index with `dimension`, the 2048 maximum, distance measures and threshold semantics, `distance_result_field`, prefilter index requirement and the 1000-result limit. Removed the claim that results are exact and the "exactly those equality fields" requirement. The gcloud `firestore indexes composite create` reference confirmed the `--field-config` syntax (`order=ascending|descending`, `vector-config={dimension=int,flat}`) and the lowercase `--query-scope` values.
Method: documentation only; no commands were run.
