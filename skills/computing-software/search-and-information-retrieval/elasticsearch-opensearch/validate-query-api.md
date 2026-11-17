---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.validate-query-api
name: validate-query-api
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, validate-query-api]
level: practitioner
status: docs-checked
description: "Use the OpenSearch _validate/query API to check a query without running it, with all_shards, lenient and rewrite options."
sources:
  - https://docs.opensearch.org/latest/api-reference/search-apis/validate/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validate query API

**Goal:** catch invalid queries before running them. The query goes in the body or as `q=` (Lucene string syntax).
```
GET my-index/_validate/query
{"query":{"query_string":{"query":"@timestamp:foo","lenient":false}}}
```
- Endpoint: `GET {index}/_validate/query`. The response has `_shards` and `valid`: `true` if the query passes, `false` if not.
- `all_shards=true` validates against every shard instead of one shard per index (default `false`).
- `explain` (default `false`) returns information about how the score is computed. `rewrite` sets how multi-term queries are rewritten and scored: `constant_score` (default), `scoring_boolean`, `constant_score_boolean`, `top_terms_N`, `top_terms_boost_N` or `top_terms_blended_freqs_N`.
- `lenient=true` ignores format-based query failures (for example text against a numeric field); default `false`.
- Other query string options: `analyzer` (only with `q`), `analyze_wildcard` (default `false`), `default_operator` (`AND` or `OR`, default `OR`), `df`, `expand_wildcards` (default `open`), `allow_no_indices` (default `true`), `ignore_unavailable` (default `false`).
- Useful in CI for stored queries and templates.
- The page's failing example is a query_string `@timestamp:foo` with `lenient` false; with `lenient` true such format failures are ignored, so a query can pass validation yet not do what you intend.

## Verify
- [ ] An intentionally malformed query (the page's `@timestamp:foo` example with `"lenient": false`) returns `"valid": false`.

## Scope
OpenSearch page checked. The Elasticsearch Validate API page was not fetched; the shape of `explanations` in responses is not on the OpenSearch page and is not covered here.

## Checked

Checked 2026-11-08 against the OpenSearch Validate Query API page. Confirmed: endpoint, parameters and defaults, the `valid` response field and the failing example. Removed: the `explanations` field and the Lucene-form claim (not on the page), the guessed `rewrite=true` usage (the page lists enumerated values), and the Elasticsearch source root.

Method: documentation only; no commands were run.
