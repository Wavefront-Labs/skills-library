---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.from-size-and-max-result-window
name: from-size-and-max-result-window
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, from-size-and-max-result-window, es-pagination]
level: practitioner
status: docs-checked
description: "Page with from and size, and understand the index.max_result_window limit of 10000 and its cost."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/paginate-search-results
  - https://www.elastic.co/docs/reference/elasticsearch/index-settings/index-modules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# from/size paging and the result window

**Goal:** know when from/size stops working.
- `GET my-index/_search {"from":20,"size":10,"sort":[{"created":"desc"},{"_id":"asc"}]}`.
- `from + size` is limited by `index.max_result_window` (default `10000`); by default you cannot page through more than 10,000 hits this way. For more, use `search_after`.
- Each shard must load its requested hits and the hits of previous pages into memory, so deep pages raise memory and CPU use and can degrade performance or fail nodes. Search requests take heap memory and time proportional to `from + size`.
- Elasticsearch uses Lucene internal doc IDs as tie-breakers, and these can differ between replicas, so documents with equal sort values may be ordered inconsistently across pages. Sort on a unique field as the last key to avoid that.

## Verify
- [ ] Walk pages 1-3 and confirm no duplicates or gaps.

## Scope
The Elasticsearch reference pages were checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch reference pages Paginate search results and Index modules. Confirmed: the 10,000 limit and setting, the memory and tie-breaker warnings. Removed: the advice that a window of 1e6 "invites out-of-memory" as a specific figure (the page only warns of memory use in general), and the OpenSearch source root.

Method: documentation only; no commands were run.
