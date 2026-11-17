---
id: computing-software.search-and-information-retrieval.qdrant.bulk-import-recipe
name: bulk-import-recipe
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [bulk-import, indexing-threshold, upload, parallel]
level: practitioner
status: docs-checked
description: "Load a large dataset quickly by deferring indexing, batching points and building payload indexes first."
sources:
  - "https://qdrant.tech/documentation/production-operations/bulk-data-import/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The bulk import guide describes the fast path for loading a large collection.

1. Create payload indexes for fields you will filter on before uploading. Qdrant builds extra HNSW links per payload index; indexing afterwards leaves filtered search on slower strategies until the graph is rebuilt, which is expensive.
2. If nothing needs to search the collection during the load, create it with `indexing_threshold` set to 0 to defer HNSW indexing.
3. Upload in batches; 64 to 256 points is a reasonable starting range. Larger batches raise throughput but cost memory and make retries dearer.
4. Use two to four parallel workers, raising only while throughput keeps rising. Multiple shards (two to four per machine is a reasonable start) give independent write paths.
5. When the load is done, set the indexing threshold back so the optimizer builds the index.

```python
client.create_collection(
    collection_name="my_collection",
    vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
    optimizers_config=models.OptimizersConfigDiff(indexing_threshold=0),
)

client.upload_points(collection_name="my_collection", points=points, batch_size=256, parallel=4)

client.update_collection(
    collection_name="my_collection",
    optimizers_config=models.OptimizersConfigDiff(indexing_threshold=10000),
)
```

The default `indexing_threshold` is 10,000 KB. While indexing is off, searches run as full scans, so defer indexing only when the collection need not serve queries during the upload; otherwise keep indexing on. The Python client starts worker processes for `parallel`, so on Windows and macOS run the upload under an `if __name__ == "__main__":` guard or the workers can hang silently. The docs also advise gRPC (`prefer_grpc=True`) for bulk work.

Confirm the upload has finished before serving production traffic, because the upload call returns before the optimizer is done:

- Collection status `yellow` means the optimizer is still working and `green` means done; `grey` means optimizations are pending but paused (often after a restart), and any update triggers them.
- Right after turning indexing back on, status can read `green` briefly. Wait until `indexed_vectors_count` catches up with the vector count.
- From v1.17 the `/collections/{collection_name}/optimizations` endpoint shows queued and running optimizations.
- Small collections may never be indexed, so an `indexed_vectors_count` of 0 is expected for small data.

Memory options at creation time (v1.19 `memory` setting): the `cold` tier stores dense vectors on disk from the start, and TurboQuant with pinned memory keeps a compressed copy in RAM for search, with originals read only to rescore.

## Checked

Method: docs-checked 2026-11-09 against the Qdrant bulk uploading page (landing_page repo, operate-and-maintain/bulk-data-import.md, which carries the cited URL as an alias), read in full. Corrected the restored threshold from 20000 to the documented default of 10,000 KB and the worker guidance from one per shard to two to four workers. Removed the unconfirmed PATCH request examples.
