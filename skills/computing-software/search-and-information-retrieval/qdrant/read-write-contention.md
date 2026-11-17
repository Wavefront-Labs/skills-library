---
id: computing-software.search-and-information-retrieval.qdrant.read-write-contention
name: read-write-contention
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [read-write-contention, prevent-unoptimized, latency, optimizer]
level: advanced
status: docs-checked
description: "Keep search latency steady under heavy writes with the prevent_unoptimized setting and optimizer tuning."
sources:
  - "https://qdrant.tech/documentation/ops-optimization/read-write-contention/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Heavy writes can create many small, unindexed segments that slow queries. The read-write contention guide covers ways to keep reads predictable.

An experimental setting, available from v1.17.1, is `prevent_unoptimized`: with it set to true, searches do not scan unindexed data. Points written to an oversized unindexed segment are stored durably but stay invisible in search until the optimizer has indexed the segment.

```http
PATCH /collections/{collection_name}
{ "optimizers_config": { "prevent_unoptimized": true } }
```

Trade-off: it changes `wait=true` to wait until every deferred point has been indexed, which can take long under continuous writes and likely causes client timeouts; the guide says to set `wait=false` on all writes when it is enabled.

Other levers from the guide:

- `optimizer_cpu_budget` is a node-level setting under `performance` in the configuration file; lowering it leaves more CPU for queries.
- `max_optimization_threads` is the maximum number of parallel optimization jobs per shard; the guide suggests 1 to smooth CPU spikes.
- `max_segment_size` caps segment size: smaller segments rebuild faster, but each search fans out across more segments.

## Checked

2026-11-03. Confirmed on the Qdrant read-write contention guide: v1.17.1 and experimental status of `prevent_unoptimized`, deferred points, the `wait` semantics, `optimizer_cpu_budget` under `performance`, `max_optimization_threads`, `max_segment_size` trade-off. Corrected the description of `prevent_unoptimized` (writes are accepted but hidden, not delayed). Removed the unconfirmed batching, `max_search_threads` and telemetry advice.

Method: documentation only; no commands were run.
