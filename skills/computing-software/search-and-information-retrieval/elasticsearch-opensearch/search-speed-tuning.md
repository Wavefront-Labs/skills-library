---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.search-speed-tuning
name: search-speed-tuning
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, search-speed-tuning]
level: advanced
status: docs-checked
description: "Speed up Elasticsearch searches: filesystem cache, preference, fewer fields, pre-indexed values, keyword ids, rounded dates, no scripts, profiling."
sources:
  - https://www.elastic.co/docs/deploy-manage/production-guidance/optimize-performance/search-speed
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tune search speed (Elasticsearch)

**Goal:** lower p95 latency. Measure first with the Profile API (`"profile": true`); the page notes profiling adds overhead, so use it for the relative cost of query parts, not as a timing.
- Filesystem cache: leave at least half of the available memory to it; Elasticsearch sets the JVM heap to follow this by default.
- Use faster storage (SSDs beat spinning disks) when I/O-bound, more or faster CPUs when CPU-bound; local storage generally beats remote.
- Linux readahead: the page recommends 128KiB; software raid, LVM or dm-crypt can leave it at several MiB. Check with `lsblk -o NAME,RA,MOUNTPOINT,TYPE,SIZE`; `blockdev --setra` takes 512-byte sectors (256 = 128KiB).
- `index.store.preload` warms the cache after restart, but preloading more than RAM makes search slower.
- Replicas can add throughput but fewer shards per node gives each a larger cache share. For `num_nodes`, `num_primaries` and tolerated `max_failures`, the page's formula is `max(max_failures, ceil(num_nodes / num_primaries) - 1)`.
- `preference` set to a user or session id sends repeat searches to the same shard copies so node-level caches help.
- Searches never time out by default; set `search.default_search_timeout`. Check open scroll contexts with `GET _nodes/stats/indices/search` and clear scrolls when done.
- Avoid joins: `nested` can slow queries several times and parent-child hundreds of times; denormalise instead.
- Search few fields: copy values into one field with `copy_to` rather than a `multi_match` over many.
- Pre-index values (for example a keyword `price_range`) so a `terms` aggregation replaces a `range` aggregation.
- Map identifiers you never range-query as `keyword`; `term` searches on keyword are often faster than on numerics.
- `constant_keyword` lets Elasticsearch skip a filter on an index where it always matches, or return no hits where it cannot match.
- `text` options `index_phrases` (phrase queries without slop) and `index_prefixes` (prefix queries; 2 to 5 characters by default) speed those queries. `index_phrases` has no effect on `match_only_text`.
- Rounded dates: `now-1h/m` instead of `now-1h` lets the query cache work. Splitting ranges into cached and uncached parts can be slower.
- Avoid script sorting, scripts in aggregations and `script_score`.
- `eager_global_ordinals: true` on heavily bucketed fields pre-builds global ordinals at the cost of heap and refresh time.
- Force-merge only read-only indices; never ones still being written.
- OpenSearch: not covered; no equivalent page was read.

## Verify
- [ ] Benchmark with the same queries before and after under a realistic workload, with several runs.

## Checked
Checked 2026-11-08 against the Elasticsearch page "Tune Elasticsearch for search speed" (all items above are from it). Only Elasticsearch was checked. Removed because the page does not state them: filter-context advice, leading-wildcard warning, `_source_includes`/`docvalue_fields`, time-based indices and routing as shard reduction, and the slow-log advice.
Method: documentation only; no commands were run.
