---
id: computing-software.search-and-information-retrieval.qdrant.distance-metrics
name: distance-metrics
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [distance, cosine, dot, euclid, manhattan, coll-distance]
level: intro
status: docs-checked
description: "Choose among the Cosine, Dot, Euclid and Manhattan distance metrics and how Cosine is implemented."
sources:
  - "https://qdrant.tech/documentation/manage-data/collections/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The distance metric is set per vector when you create a collection. Qdrant supports:

- `Cosine`
- `Dot` (dot product)
- `Euclid` (Euclidean distance)
- `Manhattan`

```json
{ "vectors": { "size": 384, "distance": "Cosine" } }
```

Implementation note from the docs: for search efficiency, Cosine similarity is implemented as dot product over normalised vectors, and vectors are normalised automatically during upload.

Choosing a metric: the docs say the choice depends on how the vectors were obtained, in particular how the encoder was trained. All vectors in a collection (or each named vector) are compared by a single metric.

Interaction with quantization: the quantization guidance says Manhattan (L1) is significantly slower under TurboQuant, and suggests scalar quantization for 4x compression with that metric.

## Checked

2026-11-03. Confirmed on the Qdrant collections page: the four metric names (`Dot`, `Cosine`, `Euclid`, `Manhattan`), cosine implemented as dot product over vectors normalised on upload, one metric per vector; on the quantization page: the L1 note. Removed the unconfirmed 'since v1.7' gate, the claim that the metric cannot be changed, and generic model-card advice.

Method: documentation only; no commands were run.
