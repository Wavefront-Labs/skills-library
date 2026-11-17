---
id: computing-software.search-and-information-retrieval.qdrant.multivectors
name: multivectors
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [multivector, maxsim, late-interaction, colbert, vec-multi]
level: advanced
status: docs-checked
description: "Store several vectors per point as a multivector and compare them with MaxSim, within the size limit."
sources:
  - "https://qdrant.tech/documentation/manage-data/vectors/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A multivector stores a list of dense vectors on one point, for models such as ColBERT that produce a vector per token. Qdrant scores them with the `max_sim` comparator.

```http
PUT /collections/late
{
  "vectors": {
    "size": 2,
    "distance": "Cosine",
    "multivector_config": { "comparator": "max_sim" }
  }
}
```

An upsert supplies a list of lists:

```json
{ "id": 1, "vector": [[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]] }
```

Constraint from the docs: a hard limit of number of sub-vectors times vector size under 1,048,576, not configurable. For 4096-dimension vectors that means at most 255 sub-vectors per point.

Details:

- All sub-vectors on a point share the collection's dimensionality.
- Different points can have different numbers of sub-vectors.
- `max_sim` is currently the only comparator: the sum of the maximum similarities between each pair of vectors in the two matrices, giving one score per point.

## Checked

2026-11-03. Confirmed on the Qdrant vectors page: `multivector_config` with `max_sim`, the ColBERT use case, the 1,048,576 limit and the 255 sub-vector figure, a variable number of vectors per point. Set the example collection size to match its 2-component sub-vectors. Removed the unconfirmed prefetch and memory advice.

Method: documentation only; no commands were run.
