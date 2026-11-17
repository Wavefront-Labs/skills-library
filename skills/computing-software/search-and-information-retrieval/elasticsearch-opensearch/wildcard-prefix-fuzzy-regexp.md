---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.wildcard-prefix-fuzzy-regexp
name: wildcard-prefix-fuzzy-regexp
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, wildcard-prefix-fuzzy-regexp]
level: advanced
status: docs-checked
description: "Use the pattern queries carefully, with their performance costs, and prefer n-grams or wildcard field type at scale."
sources:
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-wildcard-query
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-regexp-query
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-prefix-query
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-fuzzy-query
  - https://www.elastic.co/docs/reference/query-languages/querydsl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wildcard, prefix, fuzzy and regexp queries

**Goal:** pattern search without cluster pain.
- `wildcard` uses `?` (one character) and `*` (zero or more); avoid patterns that begin with `*` or `?`, which slow the search. `wildcard` queries using `*` can be resource-intensive; the docs suggest the n-gram tokenizer as an alternative.
- `case_insensitive: true` (added in 7.10.0) is available on `wildcard`, `prefix` and `regexp` queries.
- `prefix` queries can be sped up with the `index_prefixes` mapping parameter.
- `regexp` has `max_determinized_states` (default `10000`), the maximum number of automaton states the query may need.
- Setting `search.allow_expensive_queries` to `false` (cluster setting) stops `wildcard`, `prefix`, `regexp` and `fuzzy` queries from running (and `match` with fuzziness, and range on `text`/`keyword`); set it deliberately.
- For `fuzzy`, avoid a high `max_expansions` especially with `prefix_length` of `0`.
- The `wildcard` field type (a specialised keyword type) is optimised for grep-like `wildcard` and `regexp` queries on large or high-cardinality machine-generated values.

## Verify
- [ ] Compare `took` before and after switching to an n-gram or `wildcard` field.

## Scope
The Elasticsearch reference pages were checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch reference pages for wildcard, regexp, prefix, fuzzy queries, the Query DSL page and the keyword mapping page (wildcard type). Confirmed: all statements above. Removed: "edge n-grams for prefixes", "regexp on large fields causes high CPU" (not stated) and the OpenSearch source root.

Method: documentation only; no commands were run.
