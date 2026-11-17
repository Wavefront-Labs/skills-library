---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.match-phrase-and-slop
name: match-phrase-and-slop
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, match-phrase-and-slop]
level: practitioner
status: docs-checked
description: "Use match_phrase and slop to require term order and proximity, and combine it with match for ranking."
sources:
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-match-query-phrase
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-match-query-phrase-prefix
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/index-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Phrase matching and slop

**Goal:** exact or near-exact phrase hits.
- `{"match_phrase":{"body":{"query":"quick fox","slop":2}}}`: `match_phrase` analyses the text and builds a phrase query; `slop` is the maximum number of positions allowed between matching tokens (default `0`). Transposed terms have a slop of `2`.
- Phrase and proximity queries use term positions. `index_options` defaults to `positions`; `docs` and `freqs` store less than that (each value includes the ones before it), so keep `positions` (or `offsets`) on fields you phrase-search.
- `zero_terms_query` (`none` default, or `all`) controls what happens if the analyzer removes all tokens, for example with a `stop` filter.
- `match_phrase_prefix` treats the last term as a prefix; `max_expansions` (default `50`) limits how many terms that last term expands to.

## Verify
- [ ] "fox quick" does not match with slop 0 but does with slop 2 (transposition).

## Scope
The Elasticsearch reference pages were checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch reference pages for match phrase, match phrase prefix and `index_options`. Confirmed: `slop` meaning, default and the transposition value, `zero_terms_query`, `max_expansions` default, `index_options` values and the `positions` default. Removed: the "recall with match, precision with match_phrase boost" pattern and the stop-word position-shift claim (neither is stated on the pages read), and the OpenSearch source root.

Method: documentation only; no commands were run.
