---
id: computing-software.database-administration.elasticsearch.force-merge-and-shrink
name: force-merge-and-shrink
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, opensearch, ilm, snapshot, force-merge, shrink-index, segment-count, read-only-indices, deleted-docs, warm-phase]
level: advanced
status: docs-checked
description: "Force-merge read-only Elasticsearch indices to few segments and shrink shard counts after rollover, safely, via ILM warm phase or manual APIs."
sources:
  - https://github.com/elastic/elasticsearch-specification/blob/main/specification/indices/forcemerge/IndicesForceMergeRequest.ts
  - https://github.com/elastic/elasticsearch-specification/blob/main/specification/indices/shrink/IndicesShrinkRequest.ts
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/index-lifecycle-actions/ilm-shrink.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/index-lifecycle-actions/ilm-forcemerge.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/configuration-reference/thread-pool-settings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Force merge and shrink

**Goal:** indices that no longer receive writes use fewer segments and shards:
less heap, faster searches, cheaper snapshots.

## Force merge
Only on indices that are **no longer written to** (rolled-over, older time-based).
```json
POST /logs-2026.10.01/_forcemerge?max_num_segments=1
GET _cat/segments/logs-2026.10.01?v
GET _tasks?actions=*forcemerge*&detailed
```
- Merging an index that still receives writes creates huge segments that are
  never merged again efficiently, and deleted docs pile up in them.
- It is I/O heavy. Each shard is merged on the `force_merge` thread pool, a fixed pool of `max(1, allocated processors / 8)` threads per node, and the merge can need free space up to triple the shard size with `max_num_segments=1`: schedule off-peak or let ILM do it (hot or warm phase).
- `only_expunge_deletes=true` to reclaim deleted docs without merging to 1 segment.

## Shrink
Reduce primaries, e.g. 6 hot-tier shards → 1 for a small, finished index.
```json
PUT /logs-2026.10.01/_settings
{ "index.routing.allocation.require._name": "es-w1", "index.blocks.write": true }
// wait until a copy of every shard (primary or replica) is on es-w1: GET _cat/shards/logs-2026.10.01
POST /logs-2026.10.01/_shrink/logs-2026.10.01-shrunk
{ "settings": { "index.number_of_shards": 1, "index.number_of_replicas": 1,
                "index.routing.allocation.require._name": null, "index.blocks.write": null } }
```
Before shrinking the index must be read-only, a copy of every shard must be on one node and health must be green. The target shard count must be a factor of the source count (a prime count can only shrink to 1), the target index must not exist, and the node doing the shrink needs free disk for a second copy of the index. Then swap aliases and
delete the source.

## Let ILM do it
```json
"warm": { "min_age": "2d", "actions": {
    "shrink": { "number_of_shards": 1 },
    "forcemerge": { "max_num_segments": 1 },
    "allocate": { "number_of_replicas": 1 } } }
```

## Gotchas
- The current write index of a data stream cannot be shrunk; roll over first.
- The ILM `shrink` action (hot or warm phase) also accepts `max_primary_shard_size` instead of `number_of_shards` (not both) and keeps aliases pointing at the shrunken index.
- ILM's searchable snapshot action force merges first by default (`force_merge_index`).
- Force-merged indices that later receive updates lose the benefit.

## Verify
`GET _cat/segments` shows 1 segment per shard; `_cat/indices` shows the expected
shard count; heap used by segments (`GET _nodes/stats/indices/segments`) drops.

## Checked

Checked 2026-10-25 against the elasticsearch-specification and elastic/elasticsearch `main` docs (Stack 9.x). Confirmed: force merge only on read-only indices and the large-segment warning; `max_num_segments`, `only_expunge_deletes` and `wait_for_completion` parameters; `force_merge` pool size `max(1, processors/8)`; shrink prerequisites (read-only, copy of every shard on one node, green, factor rule, disk for a second copy); ILM `forcemerge` and `shrink` phases (hot, warm) and `shrink` parameters. The exact `_cat` and `_nodes/stats` Verify calls were not re-read.

Method: documentation only; no commands were run.
