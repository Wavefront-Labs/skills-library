---
id: computing-software.database-administration.elasticsearch.deep-pagination-search-after-and-pit
name: deep-pagination-search-after-and-pit
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, query-dsl, search-after, point-in-time, deep-pagination, max-result-window, scroll-deprecation, tiebreaker-sort, shard-doc]
level: practitioner
status: verified
description: "Page through Elasticsearch results beyond 10,000 hits with search_after and a point in time (PIT), replacing deep from/size and scroll."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/point-in-time-api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deep pagination (search_after / point in time)

**Goal:** stable, efficient paging or export over millions of hits.

## Why not from/size
`from + size` above `index.max_result_window` (10,000) is rejected; below it, each page makes every shard collect `from + size` hits, so deep pages get slow and memory-heavy. Raising the window is a trap.

## PIT + search_after
```json
POST orders/_pit?keep_alive=2m
-> { "id": "46ToAwMDaWR..." }

GET _search
{ "size": 1000,
  "query": { "range": { "created": { "gte": "2026-01-01" } } },
  "pit": { "id": "46ToAwMDaWR...", "keep_alive": "2m" },
  "sort": [ { "created": "asc" }, { "_shard_doc": "asc" } ] }
```
Next page: same request plus `"search_after": <sort values of the last hit>` and the (possibly updated) PIT id from the response. Stop when hits are empty.
```json
DELETE _pit { "id": "46ToAwMDaWR..." }
```
- PIT gives a consistent snapshot: documents indexed after opening do not shift pages.
- `_shard_doc` is a cheap unique tiebreaker available with PIT. Without PIT, add a unique field (e.g. an `id` keyword) as the last sort.

## Without PIT (live paging)
`search_after` alone works for "load more" UIs on live data; results may shift as data changes.

## Scroll
`scroll` still works but the docs say they no longer recommend it for deep pagination; use `search_after` with a PIT. Scroll contexts hold resources; never use for user-facing paging.

## Export at scale
Parallelise with `slice` + PIT: `"slice": { "id": 0, "max": 4 }` in each of 4 workers.

## Gotchas
- Every open PIT keeps old segments from being deleted (disk) and uses heap: always close, keep_alive short (it is extended per request).
- Sorting on `text` fields is not allowed; use keyword/numeric/date.
- Jumping to page N is impossible with search_after; design UIs as next/previous.

## Verify
Iterating to the end returns exactly `hits.total` documents (with `track_total_hits: true`) with no duplicates.
