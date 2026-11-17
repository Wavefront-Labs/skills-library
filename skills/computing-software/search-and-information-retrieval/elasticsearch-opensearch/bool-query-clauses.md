---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.bool-query-clauses
name: bool-query-clauses
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, bool-query-clauses, es-bool-query]
level: practitioner
status: docs-checked
description: "Combine must, filter, should and must_not clauses and understand which of them contribute to the score."
sources:
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-bool-query
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-filter-context
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bool query: must, filter, should, must_not

**Goal:** structure a search with scored text and unscored filters.
```
{"query":{"bool":{"must":[{"match":{"title":"phone"}}],"filter":[{"term":{"in_stock":true}},{"range":{"price":{"lte":500}}}],"must_not":[{"term":{"brand":"x"}}],"should":[{"term":{"featured":true}}]}}}
```
- `must` and `should` clauses contribute to `_score` (the scores of matching clauses are added together); `filter` and `must_not` run in filter context, so scoring is ignored and the clauses are considered for caching.
- `minimum_should_match` default: `1` if the bool has at least one `should` and no `must` or `filter`; otherwise `0` (so `should` is optional next to a `must` or `filter`).
- `must_not` returns a score of `0` for all documents.
- Failure mode: exact conditions in `must` are scored needlessly and shift the ranking; move them to `filter`.

## Verify
- [ ] Moving a `term` clause from `must` to `filter` leaves the same hits but changes the scores.

## Scope
The Elasticsearch reference pages were checked; OpenSearch behaviour was not (see its query DSL docs).

## Checked

Checked 2026-11-02 against the Elasticsearch reference (Boolean query, Query and filter context pages, from the elastic/elasticsearch docs source). Confirmed: the four occurrence types and which score, the `minimum_should_match` defaults, filter context and caching for `filter`/`must_not`, score `0` for `must_not`. Removed: the OpenSearch source root (the OpenSearch behaviour is not covered) and the unverified `explain=true` check.

Method: documentation only; no commands were run.
