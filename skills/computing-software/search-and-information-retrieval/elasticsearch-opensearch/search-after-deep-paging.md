---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.search-after-deep-paging
name: search-after-deep-paging
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, search-after-deep-paging]
level: advanced
status: docs-checked
description: "Page deeply with sort values plus search_after, with a tiebreaker field and a point in time for consistency."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/paginate-search-results
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# search_after deep pagination

**Goal:** efficient paging past the 10,000-hit `from`/`size` limit.
- The first request sorts by several fields, the last being a tiebreaker with a unique value per document (the docs' example sorts by `date` and `tie_breaker_id`). The next request repeats the same `query` and `sort` and passes the last hit's `sort` values as `"search_after":[...]`.
- If you cannot use a PIT, include a unique tiebreaker field in `sort`; without one, paged results could miss or duplicate hits.
- If a refresh happens between requests, result order may change; create a point in time (PIT) to preserve the index state across the searches. PIT searches add an implicit tiebreaker `_shard_doc`, and the `sort` values returned include it.
- Repeat the search with the last hit's sort values (including the tiebreaker). The `query` and `sort` must stay unchanged; if `from` is given it must be `0` (default) or `-1`.

## Verify
- [ ] Paging the whole result set returns each document exactly once.

## Scope
The Elasticsearch reference page was checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch reference page Paginate search results (Search after). Confirmed: tiebreaker advice, PIT purpose and implicit `_shard_doc`, unchanged `query`/`sort` requirement. Removed: "forward-only, no random jump to page N" and "sorting on a field that changes" failure mode (not stated), and the OpenSearch source root.

Method: documentation only; no commands were run.
