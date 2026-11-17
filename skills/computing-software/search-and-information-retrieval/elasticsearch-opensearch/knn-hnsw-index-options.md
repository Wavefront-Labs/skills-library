---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.knn-hnsw-index-options
name: knn-hnsw-index-options
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, knn-hnsw-index-options]
level: advanced
status: docs-checked
description: "Tune dense_vector index_options (type, m, ef_construction, quantization, rescore_vector) for the memory and recall trade-off in Elasticsearch."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dense-vector
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HNSW parameters and quantization on dense_vector

**Goal:** balance RAM, recall and speed for Elasticsearch `dense_vector` fields.
```
PUT my-index
{"mappings":{"properties":{"my_vector":{"type":"dense_vector","dims":384,"index":true,
 "index_options":{"type":"int8_hnsw","m":16,"ef_construction":100,"rescore_vector":{"oversample":3.0}}}}}}
```
- `m` (neighbours per node, default 16) and `ef_construction` (candidates tracked per new node, default 100) apply only to `hnsw`, `int8_hnsw`, `int4_hnsw` and `bbq_hnsw`. Raising them improves accuracy at the cost of slower indexing.
- `index_options.type` values: `hnsw`, `int8_hnsw`, `int4_hnsw`, `bbq_hnsw`, `flat` (brute force, exact), `int8_flat`, `int4_flat`, `bbq_flat`, `bbq_disk` (needs an Enterprise subscription per the page). Quantized types accept only `float` or `bfloat16` element types.
- Memory saved by quantization per the page: `int8` 75% (4x), `int4` 87% (8x), `bbq` 96% (32x), at a cost in accuracy. The raw float vectors stay on disk for rescoring and reindexing, so disk use rises by about 25% (`int8`), 12.5% (`int4`) and 3.1% (`bbq`).
- Constraints: `int4` needs an even number of dimensions; `bbq` supports only dimensions greater than 64; `dims` cannot exceed 4096.
- Defaults when `index_options` is omitted: `byte` and `bit` vectors use `hnsw`; float vectors use `bbq_hnsw` at 384 or more dimensions and `int8_hnsw` below that (the page notes version differences: Elastic Stack 9.0 always used `int8_hnsw`; `bbq_disk` is the float default when available under the license).
- `rescore_vector.oversample` (quantized types only) must be greater than 1.0 and less than 10.0, or exactly 0 for no oversampling and rescoring; a `rescore_vector` in the knn query overrides it. `on_disk_rescore: true` reads raw vectors from disk instead of memory, which helps when vectors exceed RAM.
- The index type can be changed with the Update Mapping API along flat -> int8_flat -> int4_flat -> bbq_flat -> hnsw -> int8_hnsw -> int4_hnsw -> bbq_hnsw (jumps allowed; the page also shows a shorter chain without the bbq types). For HNSW-to-HNSW changes `m` must stay the same or increase. Already-indexed vectors keep their old type until reindex or force-merge.
- `similarity` defaults to `cosine` (`l2_norm` for `bit`); it can be set only when `index` is true.
- Failure mode: vectors that do not fit in memory degrade search; quantize or use a disk-based type rather than only raising `m`.

## Verify
- [ ] Measure recall at k against an exact search (the page describes a `script_score` brute-force scan, or a `flat` index) on a sample before and after tuning.

## Scope
Elasticsearch `dense_vector` only. The OpenSearch k-NN equivalents are in knn-engines-spaces-and-methods.

## Checked

Checked 2026-11-08 against the Elasticsearch dense_vector mapping reference page. Confirmed: every `index_options` value, default and constraint above. Removed: the claim that small segments multiply graph searches and the page-cache sizing advice (neither stated on the page), the OpenSearch source root, and the "unconfirmed for your release" hedges, replaced by the version notes the page gives.

Method: documentation only; no commands were run.
