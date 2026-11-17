---
id: computing-software.search-and-information-retrieval.qdrant.dense-vector-limits
name: dense-vector-limits
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [dense-vectors, dimensions, limits, embeddings, vec-dense]
level: intro
status: docs-checked
description: "Dense vectors in Qdrant may have 1 to 65,536 dimensions; datatypes, quantization and multivector limits that follow from the size."
sources:
  - https://qdrant.tech/documentation/manage-data/vectors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A dense vector is the most common vector type: a fixed-length list of floating-point numbers. A dense vector can have between 1 and 65,536 dimensions. Most neural networks create dense vectors, so they work with Qdrant without extra processing.

```json
{ "id": 1, "vector": [0.05, 0.61, 0.76, 0.74] }
```

Practical points:

- By default each dimension is stored as a 32-bit float, so memory and storage grow linearly with dimensionality (a 1536-dimension OpenAI embedding needs 6KB in float32).
- Per-vector datatype (available as of v1.9.0): Float32 (default), Float16, Uint8, or a TurboQuant datatype (Turbo16, Turbo8, Turbo4). Uint8 requires values in the range 0 to 255, which many embedding models do not produce, so check first.
- Datatypes are distinct from quantization. Quantization builds a separate quantized copy alongside the original vectors (applied in the background during optimization) to select candidates quickly or even search directly; the Quantization docs cover it.
- Qdrant always stores vectors on disk; a memory tier can additionally load a copy into memory for lower latency.
- Multivectors (a matrix of vectors per point) use a comparator such as `max_sim`; there is a hard limit of number_of_sub_vectors * vector_size < 1,048,576 (about 255 sub-vectors for a 4096-dimension model).
- For keyword-style retrieval the docs describe sparse vectors, which have no fixed length.

## Checked

2026-11-08. Confirmed against the Vectors page: the 1 to 65,536 range, float32 default and 6KB example, datatype list and v1.9.0 gate, Uint8 range, quantization vs datatype note, disk storage and memory tier, multivector limit formula, sparse vectors. Page read by section; client tabs and inference part skipped. Removed unconfirmed claims: that a wrong-length upsert is rejected, the list "scalar, binary, product" quantization on this page, and the "doubling dimensions doubles memory" rule of thumb (replaced by the documented linear growth).
Method: documentation only; no commands were run.
