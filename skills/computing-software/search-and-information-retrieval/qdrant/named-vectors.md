---
id: computing-software.search-and-information-retrieval.qdrant.named-vectors
name: named-vectors
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [named-vectors, multiple-vectors, using, vectors-config, vec-named]
level: practitioner
status: docs-checked
description: "Store several vectors per Qdrant point, each with its own size and distance, search one with the using parameter, add or remove them later."
sources:
  - https://qdrant.tech/documentation/manage-data/vectors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A point can carry multiple vectors of different sizes and types (for example image, text or video embeddings). Create a separate named vector space for each in the collection's `vectors` map, with its own size and distance. Each name must be unique.

```http
PUT /collections/{collection_name}
{
  "vectors": {
    "image": { "size": 4, "distance": "Dot" },
    "text":  { "size": 5, "distance": "Cosine" }
  },
  "sparse_vectors": { "text-sparse": {} }
}
```

When upserting, provide a value for each name in the point's `vector` object:

```json
{ "id": 1, "vector": { "image": [0.9, 0.1, 0.1, 0.2], "text": [0.4, 0.7, 0.1, 0.8, 0.1],
                       "text-sparse": { "indices": [1, 3, 5, 7], "values": [0.1, 0.2, 0.3, 0.4] } } }
```

Search selects one vector space with `using` (Query API):

```json
{ "query": [0.2, 0.1, 0.9, 0.7], "using": "image", "limit": 5 }
```

Notes from the docs:

- Named vectors can be defined at creation or added later and managed independently. Adding or removing a named vector on an existing collection needs no recreation (available as of v1.18.0, `PUT /collections/{collection_name}/vectors/{vector_name}`).
- Sparse vectors live in separate storage and a separate index, configured under `sparse_vectors`, and are named in the same way.
- A collection without named vectors uses the empty name `""`.
- Datatype (Float32 default, Float16, Uint8, or a TurboQuant datatype) is configured per vector.
- For per-representation control across title, summary and chunk embeddings, the docs point to named vectors rather than multivectors, because MaxSim returns one combined score per point.

## Checked

2026-11-08. Confirmed against the Vectors page: named vectors definition and example, upsert and `using` query shape, add/remove (v1.18.0), per-vector datatype, multivector/MaxSim note, empty name for unnamed collections (from the Filtering page). Page read by section (dense, sparse, multivector, named, datatypes); inference and client tabs skipped. Removed unconfirmed claims: points need not have every named vector, sparse vectors must always be named, per-vector `hnsw_config`, quantization and memory tier on named vectors, and the advice to prefer named vectors over separate collections.
Method: documentation only; no commands were run.
