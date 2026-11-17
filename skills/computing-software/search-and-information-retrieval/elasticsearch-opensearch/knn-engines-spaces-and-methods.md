---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.knn-engines-spaces-and-methods
name: knn-engines-spaces-and-methods
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, knn-engines-spaces-and-methods]
level: advanced
status: docs-checked
description: "Choose the OpenSearch k-NN engine (lucene, faiss, jvector), space_type and method (hnsw, ivf, flat) from filtering, memory and recall needs."
sources:
  - https://docs.opensearch.org/latest/mappings/supported-field-types/knn-methods-engines/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choose OpenSearch k-NN engine, space and method

**Goal:** pick settings once. In the method definition, `name`, `space_type`, `engine` and `parameters` are all "not updatable after index creation", so a change means a new index and a reindex.
```
PUT test-index
{"settings":{"index":{"knn":true,"knn.algo_param.ef_search":100}},
 "mappings":{"properties":{"my_vector1":{"type":"knn_vector","dimension":1024,
  "method":{"name":"hnsw","space_type":"l2","engine":"faiss","parameters":{"ef_construction":128,"m":24}}}}}}
```
- Methods: `hnsw`, `ivf`, `flat`, `disk_ann`; engines: `faiss` (default), `lucene`, `nmslib` (deprecated), `jvector` (needs the `opensearch-jvector` plugin, which cannot be installed in the same cluster as `opensearch-knn`). `space_type` defaults to `l2`.
- Lucene: `hnsw` with `l2`, `cosinesimil`, `innerproduct` (innerproduct from OpenSearch 2.13). It ignores `ef_search` and sets it to the request's `k`. Filters are applied during search ("smart filtering"). `m` and `ef_construction` default to 16 and 100.
- Faiss: `hnsw` (l2, innerproduct, hamming; cosinesimil from 2.19) and `ivf` (needs training; same spaces). Filters are post-filters in the page's comparison table. Faiss `ef_search` defaults to 100 (256 for binary indexes). With `cosinesimil` Faiss normalizes vectors at indexing, so stored values differ from input.
- IVF parameters: `nlist` (default 4) and `nprobes` (default 1). Training uses the Train API with the IVF method definition; training data must have at least `nlist` points, and fewer causes the model to enter the `failed` state. With a `pq` encoder, the data needs at least 2^code_size vectors (more than 1,000 if `code_size` is unset).
- Encoders (Faiss): `flat` (default, no memory saving), `pq` (needs training; `m` default 1, `code_size` default 8 and must be 8 for `hnsw`), `sq` (`bits` 1, 2, 4 or 16; `type` fp16 or bf16 for 16-bit).
- Page guidance: HNSW when memory is not a concern; evaluate IVF for less memory and faster indexing at similar quality; add `pq` when memory is a concern (lossy). Faiss for large scale; Lucene for smaller deployments (the table says fewer than 10 million vectors). All four options list a 16,000 maximum dimension.
- Memory estimates from the page: HNSW is 1.1 * (4 * dimension + 8 * m) bytes per vector; IVF is 1.1 * (4 * dimension * num_vectors + 4 * nlist * d) bytes. Native indexes use the share of RAM set by `circuit_breaker_limit` (default 50%); a replica doubles the vector total.

## Verify
- [ ] Compare recall@k against an exact scan on a sample and record the settings used.

## Scope
OpenSearch only. Elasticsearch `dense_vector` options are in knn-hnsw-index-options.

## Checked

Checked 2026-11-08 against the OpenSearch Methods and engines page (latest docs). Confirmed: methods, engines, spaces per engine, parameter defaults, training minimums, encoders, the engine comparison table and the memory formulas. Removed: the training endpoint path (the page names only the Train API), the Elasticsearch source root, and the "unconfirmed" quantization hedge (the page documents `pq` and `sq`).

Method: documentation only; no commands were run.
