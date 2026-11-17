---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.function-score-decay
name: function-score-decay
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, function-score-decay, es-function-score]
level: advanced
status: docs-checked
description: "Blend text relevance with recency or popularity using function_score decay functions and field_value_factor."
sources:
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-function-score-query
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# function_score with decay and field_value_factor

**Goal:** rank fresh or popular documents higher without hiding relevance.
```
{"query":{"function_score":{"query":{"match":{"title":"phone"}},
 "functions":[{"gauss":{"published":{"origin":"now","scale":"30d","decay":0.5}}},{"field_value_factor":{"field":"likes","modifier":"log1p","missing":0}}],
 "score_mode":"multiply","boost_mode":"multiply"}}}
```
- `score_mode` combines the functions (multiply default; sum, avg, first, max, min; avg is weighted). `boost_mode` combines that result with the query score (multiply default; replace, sum, avg, max, min).
- Decay functions are `gauss`, `exp` and `linear` on numeric, date or geo_point fields. `scale` is required; `origin` is required for numeric and geo fields and defaults to `now` for dates; `offset` defaults to 0; `decay` defaults to 0.5 (the score at distance `scale`).
- `gauss` and `exp` never reach zero; `linear` hits 0 at twice the scale. A document missing the field gets 1 from a decay function.
- `field_value_factor` options: `factor` (default 1), `modifier` (none default; log, log1p, log2p, ln, ln1p, ln2p, square, sqrt, reciprocal) and `missing` (value for documents lacking the field; modifier and factor still apply).
- Use `log1p`, `ln1p` or `sqrt` so popularity does not swamp text relevance. `log` and `ln` go negative for values between 0 and 1 and cause errors (scores must be non-negative); log of 0 or sqrt of a negative throws.
- `max_boost` caps the function score; `min_score` drops low scorers but forces all matches to be scored first.
- Failure mode: large raw multipliers hide the text score.

## Verify
- [ ] `explain=true` shows the function parts and the final multiplication.

## Checked
Date: 2026-11-08
Method: Read the Elasticsearch function score query page in full; OpenSearch was not checked.
