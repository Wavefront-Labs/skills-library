---
id: computing-software.search-and-information-retrieval.qdrant.edge-embedded
name: edge-embedded
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [edge, embedded, python-bindings, rust-crate]
level: advanced
status: docs-checked
description: "Run Qdrant Edge in-process from Python or Rust against a local directory instead of a server."
sources:
  - "https://qdrant.tech/documentation/edge/edge-quickstart/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Qdrant Edge runs vector search inside your own process. It is installed from the PyPI package qdrant-edge-py (Python bindings) or the Rust crate qdrant-edge.

The core unit is an Edge Shard, which stores its data in a local directory on disk. Flow from the quickstart:

1. Create the storage directory, then build an `EdgeConfig` defining the dense and sparse vectors the shard can store, like a collection configuration. All quantization methods (scalar, product, binary, TurboQuant) are supported, set globally on `EdgeConfig.quantization_config` or per vector on `EdgeVectorParams.quantization_config`.
2. Create the shard with `EdgeShard.create` (Python) or `EdgeShard::new` (Rust). This fails if the directory already holds data; reopen existing data with `load`, where unset config parameters keep the values persisted with the shard.
3. Add points with `update`, fetch by id with `retrieve`, and search with `query`. Filters are accepted by most read methods, and `facet` builds facets. Create payload indexes first on fields used for filtering and faceting.
4. Call `optimize` yourself: Edge has no background optimizer, so run it at a suitable time such as after a batch of updates. Tune it with the `optimizers` parameter of `EdgeConfig`.
5. Close the shard on shutdown so data is flushed (Python); in Rust there is no `close` and the shard flushes on drop.

You can add or remove named vectors on an existing shard (for example to move to a new embedding model); existing points are not populated with a new vector until re-upserted.

Tuning:

- The WAL file is pre-allocated to 32 MiB by default; `wal_options` (Rust only) shrinks it. Setting `wal_enabled` to false skips the WAL, and updates are then durable only once `flush` returns.
- Each shard has a search thread pool, by default four threads per CPU core. `max_search_threads` sets the count and `search_pool_core` pins threads to one core (best effort, and only a hint on macOS). In Python `EdgeConfig` must still declare vectors or sparse vectors.

## Checked

Method: docs-checked 2026-11-09 against the Qdrant Edge quickstart (landing_page repo, edge/edge-quickstart.md), read in full; code snippets are Hugo includes and were not read. Removed the unconfirmed `from qdrant_edge import EdgeShard` import, the server sync step, the claim that replication does not apply, and the source-control advice.
