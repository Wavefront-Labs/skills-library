---
id: computing-software.search-and-information-retrieval.qdrant.optimizers
name: optimizers
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [optimizers, segments, indexing-threshold, vacuum, optimizer]
level: advanced
status: docs-checked
description: "How Qdrant optimizers vacuum, merge and index segments, and the main optimizers_config settings."
sources:
  - "https://qdrant.tech/documentation/ops-optimization/optimizer/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Qdrant stores points in segments. Background optimizers keep them efficient. Each segment is wrapped in a proxy, and changed data goes to a copy-on-write segment that has priority for retrieval and updates, so the collection stays available during optimization. Three optimizers work on segments:

- Vacuum optimizer rewrites segments with many deleted points.
- Merge optimizer combines small segments.
- Indexing optimizer enables indexes and memmap storage once the minimal number of records is reached.

Settings in `optimizers_config` with defaults from the configuration reference:

- `deleted_threshold`: 0.2, the minimum fraction of deleted records in a segment before it is considered for vacuum.
- `vacuum_min_vector_number`: 1000, the minimum number of vectors a segment needs to qualify.
- `default_segment_number`: 0 selects the number of CPUs automatically; the docs recommend a factor of the number of search threads.
- `indexing_threshold_kb`: 10000.
- `flush_interval_sec`: 5.
- `max_segment_size_kb` caps segment size (unset: scaled by CPU count). Larger segments can improve search but take longer to index.
- `max_optimization_threads` limits parallel optimization jobs per shard (default `null`, no limit).

Change a collection's values with:

```http
PATCH /collections/{collection_name}
{ "optimizers_config": { "indexing_threshold": 20000 } }
```

The docs note that below about 10000 points a brute-force scan is more efficient than any index, which is why indexing starts only above the threshold.

## Checked

2026-11-03. Confirmed on the Qdrant optimizer and configuration pages: proxy and copy-on-write segments, the three optimizers, `deleted_threshold` 0.2, `vacuum_min_vector_number` 1000, `default_segment_number` 0, `indexing_threshold_kb` 10000, `flush_interval_sec` 5, `max_segment_size_kb`, `indexing_threshold` in the PATCH body, the 10000-point brute-force note. Removed the unconfirmed claim about raising the indexing threshold.

Method: documentation only; no commands were run.
