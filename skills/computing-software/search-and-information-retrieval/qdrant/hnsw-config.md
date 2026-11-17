---
id: computing-software.search-and-information-retrieval.qdrant.hnsw-config
name: hnsw-config
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [hnsw, m, ef-construct, full-scan-threshold, idx-hnsw]
level: practitioner
status: docs-checked
description: "The Qdrant HNSW parameters m, ef_construct and full_scan_threshold with their config-file defaults, per-collection hnsw_config and ef at search."
sources:
  - https://qdrant.tech/documentation/manage-data/indexing/
  - https://qdrant.tech/documentation/manage-data/collections/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Qdrant uses HNSW as its only dense vector index. HNSW limits the maximum degree of nodes on each layer of the graph to `m`, and uses `ef_construct` (building) or `ef` (searching) to set the search range.

Defaults from the configuration file (`storage.hnsw_index`), which can be overridden per collection or per named vector (as of v1.1.1) with `hnsw_config`:

- `m`: 16, the number of edges per node. A larger value gives more accurate search and needs more space.
- `ef_construct`: 100, the number of neighbours considered while building the index. A larger value gives more accurate search and a longer build.
- `full_scan_threshold`: 10000 (in KB; the config comment says 1KB is one vector of size 256). When the maximum estimated number of points a condition matches is smaller than the threshold, the query planner uses a full scan instead of HNSW traversal.

Update an existing collection (the collection update API accepts `hnsw_config`):

```http
PATCH /collections/{collection_name}
{ "hnsw_config": { "m": 32, "ef_construct": 200 } }
```

At query time `params.hnsw_ef` sets `ef`, the search width; by default it equals `ef_construct`. `params.exact: true` skips the index and scans everything.

Notes:

- A small change to `hnsw_config`, such as bumping `ef_construct` by 1, forces the optimizer to re-index all segments. Rebuilding is resource-intensive and can take a long time, so avoid it when possible.
- To make the graph suit filtered search, create payload indexes before ingesting data: Qdrant adds extra graph edges per payload index. The ACORN search algorithm (as of v1.16.0) helps when strict filters combine several indexed fields, at the cost of performance.
- The collection update call may block while optimizers finish, and the docs advise against it in production because of index rebuild overhead.

## Checked

2026-11-08. Confirmed against the Indexing page (Vector Index and Filterable HNSW sections, rebuild procedure) and the Collections page (update parameters). Removed unconfirmed claims: defaults and meaning of `max_indexing_threads` (including the 8 to 16 advice), `on_disk` deprecation, `payload_m`, and that changing `m` rebuilds the graph (only the `ef_construct` rebuild is documented).
Method: documentation only; no commands were run.
