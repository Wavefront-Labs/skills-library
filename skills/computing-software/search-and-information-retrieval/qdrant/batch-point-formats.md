---
id: computing-software.search-and-information-retrieval.qdrant.batch-point-formats
name: batch-point-formats
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [batch, upload, column-oriented, record-oriented, pts-batch]
level: practitioner
status: docs-checked
description: "Send Qdrant points in record-oriented or column-oriented batches and follow the bulk-upload guide for batch size, threads and shards."
sources:
  - https://qdrant.tech/documentation/manage-data/bulk-upload/
  - https://qdrant.tech/documentation/manage-data/points/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Qdrant supports two ways of creating batches; internally they are equivalent and only provided for convenience.

Record-oriented: a list of point objects.

```json
{ "points": [
  { "id": 1, "vector": [0.9, 0.1], "payload": { "color": "red" } },
  { "id": 2, "vector": [0.1, 0.9], "payload": { "color": "blue" } }
] }
```

Column-oriented: parallel arrays.

```json
{ "batch": {
  "ids": [1, 2],
  "vectors": [[0.9, 0.1], [0.1, 0.9]],
  "payloads": [{ "color": "red" }, { "color": "blue" }]
} }
```

Both go to `PUT /collections/{collection_name}/points`.

Bulk-upload guide recommendations:

- Upsert in batches, not one point at a time; each request has overhead (round trip, WAL write, routing). Aim for 64 to 256 points per batch: smaller batches under-use the network, larger ones raise server memory pressure and the cost of a retry. Experiment for your data.
- Split the dataset across two to four concurrent threads. With several shards, start with one upload thread per shard.
- The Python client's `upload_points` (as of v1.7.1; it replaced the now deprecated `upload_records`) and `upload_collection` handle batching and parallelization: parallelization, retries and lazy batching, so data can be read from disk without holding it all in RAM. They accept both record and column formats. For other clients you implement batching and parallelism yourself.
- Collections default to one shard; two to four shards per machine is a reasonable number to parallelize upload.
- Create payload indexes before uploading (order: create collection, create payload indexes, upload points), so the HNSW graph is built once with the extra filter links.
- If vectors do not fit in RAM, set the per-vector `memory` parameter to `cold` at collection creation rather than relying on `memmap_threshold`.
- Bulk writes compete with searches for CPU, memory bandwidth and I/O; see the Read-Write Contention guide if you must serve queries during the load.

## Checked

2026-11-08. Confirmed against the Bulk Upload page (read in full) and the Points page (batch section and Python client optimizations; remaining sections skipped). Removed unconfirmed claims: that the column form avoids repeating keys, and a 32 MB default maximum request size.
Method: documentation only; no commands were run.
