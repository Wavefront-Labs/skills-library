---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.rank-feature-query
name: rank-feature-query
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, rank-feature-query]
level: practitioner
status: docs-checked
description: "Boost relevance from a numeric signal with rank_feature fields and the rank_feature query: saturation, log, sigmoid, linear, and field limits."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/rank-feature
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-rank-feature-query
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rank_feature field and query

**Goal:** cheap, fast signal-based boosting (popularity, page rank, freshness score).
- Mapping: `"pagerank":{"type":"rank_feature"}`. Use `"positive_score_impact":false` (default `true`) for a feature that correlates negatively with score, such as URL length.
- The field accepts only single-valued, strictly positive values; multi-valued fields and negative values are rejected. Use the `rank_features` type for a map of named values (for example topics), queried as `topics.sports`.
- A `rank_feature` field cannot be queried, sorted or aggregated; it can only be used inside `rank_feature` queries. It keeps 9 significant bits, a relative error of about 0.4%.
- Typical use is a `should` clause beside a `must` text query so the rank score is added:
```
{"query":{"bool":{"must":{"match":{"content":"2016"}},"should":{"rank_feature":{"field":"pagerank","saturation":{"pivot":8}}}}}}
```
- Parameters: `field` (required), `boost` (default 1.0) and exactly one function: `saturation` (default; `S / (S + pivot)`, scores in (0,1); with a negative impact it is `pivot / (S + pivot)`), `log` (`log(scaling_factor + S)`, positive-impact features only), `sigmoid` (adds an `exponent`, typically in [0.5, 1]) or `linear`.
- If `pivot` is omitted for saturation, Elasticsearch uses roughly the geometric mean of the field's values in the index.
- With `positive_score_impact:false`, give every participating document a value: a missing value adds nothing in a `should` clause, which ranks it above documents that have the (bad) feature.
- Unlike `function_score` and other ways to change scores, `rank_feature` skips non-competitive hits when `track_total_hits` is not `true`, which can dramatically improve speed.

## Verify
- [ ] With equal text scores, documents with higher `pagerank` rank higher.
- [ ] Indexing a negative or multi-valued `pagerank` is rejected.

## Checked
2026-11-08. Confirmed against the Elasticsearch rank_feature field type and rank_feature query pages: mapping parameters, value restrictions, query-only usage, precision, function formulas and defaults, pivot default, missing-value advice, non-competitive hit skipping.
Removed: the claim of being faster than `script_score` (the docs compare to `function_score`), the "zero value rejected" wording (docs say strictly positive), and the OpenSearch root source. OpenSearch behaviour was not checked here.
Method: documentation only; no commands were run.
