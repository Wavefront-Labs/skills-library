---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.scroll-api-and-slicing
name: scroll-api-and-slicing
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, scroll-api-and-slicing]
level: advanced
status: docs-checked
description: "Use scroll with a keep-alive for bulk export, clear it afterwards, and parallelise with slices."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/paginate-search-results
  - https://www.elastic.co/docs/deploy-manage/production-guidance/optimize-performance/search-speed
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scroll API and sliced scroll

**Goal:** reading all documents of an index.
- `POST my-index/_search?scroll=1m {"size":1000,"query":{...}}` returns a `_scroll_id`; then `POST _search/scroll {"scroll":"1m","scroll_id":"<id>"}` repeatedly until `hits` is empty. Only the most recently received `_scroll_id` should be used. Results reflect the index state at the initial search.
- The `scroll` value only has to keep the context alive until the next request, not the whole export. Open scroll contexts keep old segments from being deleted.
- Parallel: `"slice":{"id":0,"max":4}` per worker (`id` is the slice, `max` the number of slices). If there are more slices than shards, the slice filter is slow on the first calls.
- Free resources: `DELETE _search/scroll {"scroll_id":"<id>"}`; `DELETE /_search/scroll/_all` clears all.
- The docs no longer recommend scroll for deep pagination: use `search_after` with a PIT; PIT with slicing is recommended over scroll when possible.
- The maximum number of open scrolls is 500 by default, changed with the `search.max_open_scroll_context` cluster setting.

## Verify
- [ ] `GET /_nodes/stats/indices/search` shows `open_contexts` back at zero after clearing the scrolls.

## Scope
The Elasticsearch reference pages were checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch reference page Paginate search results (Scroll search results) and the Search speed tuning page (`open_contexts`). Confirmed: all statements above. Removed: the exception name `too_many_scroll_contexts_exception` (not stated) and the OpenSearch source root.

Method: documentation only; no commands were run.
