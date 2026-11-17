---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.script-score-query
name: script-score-query
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, script-score-query]
level: advanced
status: docs-checked
description: "Compute custom scores with a script_score query using _score, doc values, params and the predefined saturation, sigmoid, decay and vector functions."
sources:
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-script-score-query
  - https://docs.opensearch.org/latest/query-dsl/specialized/script-score/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# script_score query

**Goal:** a custom ranking formula over the documents a query returns.
```
{"query":{"script_score":{"query":{"match":{"message":"elasticsearch"}},"script":{"source":"saturation(doc['my-int'].value, 1)"}}}}
```
- `query` and `script` are required. `min_score` excludes documents scoring lower (also from aggregations); `boost` (default 1.0) multiplies the script score.
- Final scores from `script_score` cannot be negative: Lucene requires scores to be positive or 0.
- Inside the script, `_score` is the child query's score and `_termStats` gives term statistics of the child query.
- Elasticsearch predefined functions (preferred over hand-written equivalents): `saturation(value, k)` = value/(k + value); `sigmoid(value, k, a)` = value^a/(k^a + value^a); `randomScore(seed, fieldName)`; `decayNumeric*`, `decayGeo*`, `decayDate*` (Linear, Exp, Gauss); and vector functions `cosineSimilarity`, `dotProduct`, `l1norm`, `l2norm`, `hamming`.
- Missing values: guard with `doc['field'].size() == 0`.
- Cost: the script runs for every matching document. The page notes the query can be skipped entirely when `search.allow_expensive_queries` is false, and suggests `rank_feature` (static field boosts) or `distance_feature` (date or geo proximity) as faster alternatives.
- Vector functions scan all matched documents linearly, so limit the matches with the inner `query`; call each vector function once per script, not in a loop; `cosineSimilarity` is not supported for bit vectors.
- Decay functions on dates use only the default date format and time zone, and `now` is not supported.
- Use `params` for changing values: the page says it lets the script compile once even when the params change.
- Replacing `function_score`: `weight` becomes `params.weight * _score`, and `field_value_factor` becomes a `Math.log10`, `Math.log`, `Math.sqrt` and similar expression on `doc['f'].value`.

## Verify
- [ ] Result order matches a hand-computed score for three documents.

## Scope
The Elasticsearch page was checked in full. The OpenSearch page confirms `min_score`, the non-negative rule (a negative value fails the search), `saturation`, `sigmoid` (pivot-based wording) and `search.allow_expensive_queries`. OpenSearch vector functions come from the k-NN plugin (`l2Squared`, `cosineSimilarity`, `hamming`), so the Elasticsearch vector-function list does not carry over; the other Elasticsearch function names were not compared.

## Checked

Checked 2026-11-08 against the Elasticsearch Script score query page. Confirmed: required parameters, `min_score`, `boost`, the non-negative rule, predefined functions and formulas, the missing-value guard, vector-function warnings, expensive-queries setting and the function_score migration table. Removed: the unverified claim that varying literal values causes compilation rate-limit errors (the page says only that `params` compile once) and the page-root sources.

Method: documentation only; no commands were run.
