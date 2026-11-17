---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.shrink-split-clone-index
name: shrink-split-clone-index
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, shrink-split-clone-index]
level: advanced
status: docs-checked
description: "Change primary shard count with the shrink, split or clone index APIs, including the write block, co-location and health prerequisites."
sources:
  - https://docs.opensearch.org/latest/api-reference/index-apis/shrink-index/
  - https://docs.opensearch.org/latest/api-reference/index-apis/split/
  - https://docs.opensearch.org/latest/api-reference/index-apis/clone/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shrink, split and clone indices

**Goal:** resize primary shards without a full reindex. Checked against the OpenSearch pages; Elasticsearch has the same APIs but its pages were not checked.

All three need: source `index.blocks.write: true`, cluster health green, a target index that does not exist yet, and free disk on the node doing the work (a second copy of the index; for clone, when hard links are unsupported). Mappings cannot be given in the shrink or split request: the target inherits them. Segments are hard-linked from the source; without file system hard-link support they are copied, which is much slower.

- Shrink: also needs a copy of every shard on one node, for example `PUT src/_settings {"settings":{"index.routing.allocation.require._name":"<NODE>","index.blocks.write":true}}`. Then `POST src/_shrink/target {"settings":{"index.number_of_shards":2,"index.number_of_replicas":0,"index.routing.allocation.require._name":null,"index.blocks.write":null}}`. Target primary count must be a factor of the source count and smaller (8 shrinks to 4, 2 or 1; 7 only to 1). The source can hold at most 2,147,483,519 documents across the shards merged into one target shard.
- `max_shard_size` in the shrink body picks the smallest factor of the source count that keeps shards under that size; it cannot be combined with `index.number_of_shards`.
- Split: `POST src/_split/target {"settings":{"index.number_of_shards":4}}`. Target count must be a multiple of the source and larger. The possible split paths depend on `index.number_of_routing_shards`; if unset, the default allows repeated doubling up to 1,024 shards. Documents are rehashed to their new shards.
- Clone: `POST src/_clone/target`; target has the same primary shard count and keeps mappings and settings. The write block can be set on the source while metadata changes such as deleting the index remain allowed.
- All three accept `PUT` or `POST`. Shrink and split return once the target is in cluster state and do not wait for completion; shrink also takes `wait_for_completion=false` to return a task. Track with CAT recovery, or the Cluster Health API with `wait_for_status=yellow`.
- Failure mode: shrink stuck because the shards could not be co-located on one node; shard relocation takes time on large indices.

## Verify
- [ ] `GET _cat/shards/target?v` shows the intended primary count and green state, and the write block is cleared on the target if you need to write to it.

## Checked

Checked 2026-11-08 against the OpenSearch Shrink Index, Split Index and Clone Index API pages. Confirmed: prerequisites, factor and multiple rules, `max_shard_size`, routing shard defaults, endpoints and monitoring behaviour. Removed: the unfetched Elasticsearch source root.

Method: documentation only; no commands were run.
