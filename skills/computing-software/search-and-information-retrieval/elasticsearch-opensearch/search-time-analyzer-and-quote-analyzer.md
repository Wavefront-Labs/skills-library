---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.search-time-analyzer-and-quote-analyzer
name: search-time-analyzer-and-quote-analyzer
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, search-time-analyzer-and-quote-analyzer]
level: advanced
status: docs-checked
description: "Set search_analyzer, search_quote_analyzer and the per-query analyzer so query text matches indexed tokens, for example with edge n-grams or stop words."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/search-analyzer
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/analyzer
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-match-query
  - https://docs.opensearch.org/latest/analyzers/search-analyzers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Index-time versus search-time analyzers

**Goal:** make query text analysis consistent with indexed tokens.
- Usually use the same analyzer at index and search time. A different search analyzer makes sense for `edge_ngram` autocomplete or search-time synonyms.
- Field mapping (Elasticsearch page's example): `{"type":"text","analyzer":"autocomplete","search_analyzer":"standard"}`. With edge-ngram indexing, "Quick Brown Fox" is indexed as q, qu, qui, quic, quick, b, br, ... and the query "Quick Br" with `operator: and` searches the terms [quick, br].
- Elasticsearch `match`: the query-level `analyzer` defaults to the field's mapped analyzer (the Elasticsearch text says the field's explicit mapping or the default search analyzer in another place, so use `_analyze` to confirm the effective one). If an analyzer removes all tokens (a stop filter), `zero_terms_query` decides: `none` (default) or `all`.
- OpenSearch picks the search analyzer in this order: the query's `analyzer`, the field's `search_analyzer`, the `analysis.analyzer.default_search` index setting, the field's `analyzer`, then `standard`. It also warns that a different search analyzer is rarely needed and can hurt relevance.
- `search_quote_analyzer` (Elasticsearch) is used for phrases (quoted text). To keep stop words in phrase queries only, use three settings: `analyzer` indexes all terms, `search_analyzer` removes stop words, `search_quote_analyzer` keeps them. A quoted `query_string` such as `"the quick brown fox"` then matches only the document containing "The".
- Updating an existing field: `search_analyzer` and `search_quote_analyzer` can be updated with the update mapping API (repeat the existing `analyzer` and `type` in the new definition); `analyzer` cannot. Only `text` fields support `analyzer`.
- Test analyzers before production use (`_analyze`).
- Failure mode (a judgment, not stated on the pages): using the n-gram analyzer at search time as well would n-gram the query and likely give false matches.

## Verify
- [ ] Searching a prefix finds the doc and `_analyze` with the search analyzer produces one token per query word, not n-grams.

## Checked
Checked 2026-11-08 against the Elasticsearch "search_analyzer", "analyzer" and "Match query" pages and the OpenSearch "Search analyzers" page. Removed: the claim that the `analyzer` setting in the `match` query is always overridden by `search_analyzer` precedence for Elasticsearch (the Elasticsearch page does not give an order).
Method: documentation only; no commands were run.
