---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.match-query-operators
name: match-query-operators
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, match-query-operators, es-full-text-queries]
level: practitioner
status: docs-checked
description: "Use match with operator, fuzziness and minimum_should_match to tune recall for analysed text fields."
sources:
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-match-query
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-minimum-should-match
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Match query: operator, fuzziness, minimum_should_match

**Goal:** control how many query terms must match.
```
GET my-index/_search
{"query":{"match":{"title":{"query":"quick brown fox","operator":"and","fuzziness":"AUTO"}}}}
```
- `match` analyses the text and builds a boolean query. `operator` is `or` (default) or `and`; with `and` every term is required. `minimum_should_match` (for example `"75%"`) sets how many optional clauses must match.
- `fuzziness` sets the maximum edit distance; `prefix_length` is the number of beginning characters left unchanged for fuzzy matching (default `0`).
- `zero_terms_query` is `none` (default) or `all`; `all` behaves like `match_all` when the analyzer removes every token (for example a `stop` filter).
- If `search.allow_expensive_queries` is `false`, a `match` query that sets `fuzziness` returns an error.

## Verify
- [ ] Compare hit counts for `or`, `and` and `75%` on a sample query.

## Scope
The Elasticsearch reference pages were checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch reference Match query and `minimum_should_match` pages. Confirmed: `operator` values and default, `prefix_length`, `zero_terms_query`, the `allow_expensive_queries` behaviour with fuzziness. Removed: "fuzziness on short words is noisy, raise `prefix_length`" and the keyword-casing failure mode (not on the pages), and the OpenSearch source root.

Method: documentation only; no commands were run.
