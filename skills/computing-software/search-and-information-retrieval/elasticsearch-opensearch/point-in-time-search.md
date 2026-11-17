---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.point-in-time-search
name: point-in-time-search
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, point-in-time-search, es-point-in-time]
level: advanced
status: docs-checked
description: "Open a PIT for a stable view, search with it plus search_after, extend keep_alive and close it."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/paginate-search-results
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Point in time (PIT) searches

**Goal:** consistent paging while indexing continues.
- Open: `POST my-index/_pit?keep_alive=1m` returns a PIT ID.
- Search: `{"pit":{"id":"<id>","keep_alive":"1m"},"sort":[...],"search_after":[...]}`; omit the target data stream or index from the request path. Each search can extend the PIT's retention with its `keep_alive`.
- The search response returns an updated PIT `id`; use the latest PIT ID in the next request.
- Close: `DELETE /_pit` with the PIT `id` in the body, when you are finished.
- PIT searches add an implicit tiebreaker `_shard_doc` to the sort.
- A PIT preserves the index state, so refreshes between paged requests do not change the results seen.

## Verify
- [ ] Documents indexed after opening the PIT do not appear in results.

## Scope
Only the Elasticsearch request shapes were checked. OpenSearch uses different PIT endpoints, which were not checked here.

## Checked

Checked 2026-11-02 against the Elasticsearch reference page Paginate search results (Search after, with a PIT). Confirmed: `_pit?keep_alive`, `pit.id` and `pit.keep_alive` in the search body, omitting the index from the path, updated `id` in the response, `DELETE /_pit`, implicit `_shard_doc`. Removed: the OpenSearch endpoints and the `search_context_missing_exception` failure mode (neither stated on the page).

Method: documentation only; no commands were run.
