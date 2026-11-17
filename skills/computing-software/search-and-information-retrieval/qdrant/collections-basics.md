---
id: computing-software.search-and-information-retrieval.qdrant.collections-basics
name: collections-basics
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [collection, create, vectors-config, points, coll-create]
level: intro
status: docs-checked
description: "A Qdrant collection is a named set of points with one vector dimensionality and metric; how to create one, its options and how to update it."
sources:
  - https://qdrant.tech/documentation/manage-data/collections/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A collection is a named set of points (vectors with a payload) that you can search. The vector of each point in a collection has the same dimensionality and is compared by a single metric. Named vectors let a point carry several vectors, each with its own dimensionality and metric.

```http
PUT /collections/{collection_name}
{
  "vectors": { "size": 300, "distance": "Cosine" }
}
```

Supported distance metrics: `Dot`, `Cosine`, `Euclid` and `Manhattan`. Cosine is implemented as a dot product over normalized vectors, and vectors are normalized automatically at upload.

Besides the required options, the creation request accepts:

- `hnsw_config` for index parameters
- `wal_config` for the write-ahead log
- `optimizers_config` for optimizer behaviour
- `shard_number` for how many shards the collection has
- `payload.memory` for the memory tier of payload storage
- `quantization_config` for quantization
- `strict_mode_config` for strict mode

Defaults for the optional parameters come from the configuration file. For rare use cases a collection can be created without any vector storage.

Guidance from the docs: in most cases use a single collection with payload-based partitioning (multitenancy) rather than one collection per user. Multiple collections suit a limited number of users who need isolation, but creating many collections adds resource overhead and the collections must not affect each other's performance.

Vectors are always stored on disk, and a per-vector memory tier controls how much also lives in memory (as of v1.2.0). Collection parameters such as optimization and index settings can be changed at any time with `PATCH /collections/{collection_name}`, which accepts `optimizers_config`, `hnsw_config`, `quantization_config`, `vectors_config`, `params` and `strict_mode_config`. The call may block while existing optimizers finish, and the docs advise against using it in a production database because rebuilding indexes can cause large overhead. Updating vector parameters always needs a vector name (use `""` when the collection has no named vectors).

## Checked

2026-11-08. Confirmed against the Collections page: create request, metric list and cosine normalization, optional creation parameters, vector-less collections, multitenancy guidance, memory tier (v1.2.0), update endpoint and its parameters and warning. Page read by section (intro, create, options, named vectors, update); client tabs and later sections skipped. Corrected: the `payload` option is `payload.memory`. Removed unconfirmed claim that vector size and distance are fixed at creation (the page says other settings can be changed at any time but does not state this).
Method: documentation only; no commands were run.
