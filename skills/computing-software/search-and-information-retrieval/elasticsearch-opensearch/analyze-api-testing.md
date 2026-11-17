---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.analyze-api-testing
name: analyze-api-testing
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, analyze-api-testing]
level: practitioner
status: docs-checked
description: "Use the _analyze API to inspect tokens from analyzers, tokenizer plus filter chains, and fields before debugging queries."
sources:
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-analyze
  - https://docs.opensearch.org/latest/api-reference/analyze-apis/
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/search-analyzer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test analysis with the _analyze API

**Goal:** see the real tokens for a string, which explains most "why no match" cases.
- By analyzer: `POST _analyze {"analyzer":"standard","text":"Quick Foxes"}`. With no index, or an index with no default analyzer, the standard analyzer is used.
- By chain: `POST _analyze {"tokenizer":"standard","filter":["lowercase"],"text":"The Foxes"}`. Filters can also be inline objects such as `{"type":"stop","stopwords":["a","is","this"]}`.
- By field (uses that index mapping): `POST my-index/_analyze {"field":"title","text":"..."}`. `field` needs an index. `analyzer`, `normalizer` and `field` cannot be combined with `tokenizer`, `filter` or `char_filter`.
- Add `"explain":true` (default false) to see token attributes and per-stage detail.
- Compare index-time and search-time analyzers if they differ: queries use the field's mapped analyzer unless the field sets `search_analyzer`.
- Failure mode: testing with the standard analyzer when the field uses another one gives misleading results; pass the index and `field`.

## Verify
- [ ] The tokens from `_analyze` on the field equal the terms you put in a `term` query that must match.

## Checked
Date: 2026-11-07
- Elasticsearch analyze API page, read in full: GET/POST `/_analyze` and `/{index}/_analyze`, body fields `analyzer`, `tokenizer`, `filter`, `char_filter`, `field` (index required), `normalizer`, `explain` (default false), `text`; standard analyzer default; examples including the inline `stop` filter.
- OpenSearch Analyze API page: read from the start through the request-body-field table and its combination rules, and searched the examples for the inline `stop` filter; the response and remaining examples were not read in full.
- Elasticsearch `search_analyzer` mapping page, read in full: queries use the field mapping's analyzer unless `search_analyzer` overrides.
- Removed: the bare `"stop"` filter name in the chain example (only the inline `{"type":"stop"}` form appears on the pages), replaced with `lowercase`, which appears in the Elasticsearch example.
Method: documentation only; no commands were run.
