---
id: computing-software.database-administration.elasticsearch.relevance-tuning-multi-match-and-function-score
name: relevance-tuning-multi-match-and-function-score
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, query-dsl, relevance-tuning, function-score, multi-match, field-boosting, best-fields, cross-fields, decay-function, rank-feature, explain-api]
level: practitioner
status: verified
description: "Tune Elasticsearch relevance: multi_match types and field boosts, function_score with decay and field_value_factor, rank_feature, and measuring with rank_eval."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-function-score-query.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-rank-eval.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relevance tuning (multi_match / function_score)

**Goal:** the results users expect come first, and changes are measured rather than guessed.

## multi_match types
```json
GET products/_search
{ "query": { "multi_match": {
    "query": "running shoes waterproof",
    "fields": ["title^3", "brand^2", "description"],
    "type": "best_fields", "tie_breaker": 0.3
} } }
```
| Type | Use |
|---|---|
| `best_fields` (default) | Words expected together in one field; tie_breaker blends others |
| `most_fields` | Same text indexed several ways (stemmed + exact subfields) |
| `cross_fields` | Terms spread over fields (first/last name, title/brand) treated as one big field |
| `phrase` / `phrase_prefix` | Phrase match per field; search-as-you-type |
| `bool_prefix` | With `search_as_you_type` fields |

Boost exact matches with a `should` clause on a `.keyword` or shingle subfield.

## function_score: business signals
```json
{ "query": { "function_score": {
    "query": { "multi_match": { "query": "tent", "fields": ["title^3", "description"] } },
    "functions": [
      { "field_value_factor": { "field": "sales_30d", "modifier": "log1p", "factor": 0.5, "missing": 0 } },
      { "gauss": { "published": { "origin": "now", "scale": "30d", "decay": 0.5 } } },
      { "filter": { "term": { "in_stock": true } }, "weight": 1.5 }
    ],
    "score_mode": "sum", "boost_mode": "multiply", "max_boost": 10
} } }
```
`rank_feature` fields + the `rank_feature` query (usually in a `should` clause) are the purpose-built way to add static signals such as popularity.

## Debug and measure
- `"explain": true` or `GET products/_explain/<id>` shows BM25 and function contributions.
- `_rank_eval` with a judged query set computes precision@k / NDCG/ MRR before and after changes:
```json
GET products/_rank_eval
{ "requests": [ { "id": "tent", "request": { "query": { "match": { "title": "tent" } } },
    "ratings": [ { "_index": "products", "_id": "42", "rating": 3 } ] } ],
  "metric": { "dcg": { "k": 10, "normalize": true } } }
```

## Gotchas
- Scores are per shard (IDF): tiny test indexes with many shards give odd rankings; test on realistic data or `search_type=dfs_query_then_fetch`.
- Boosts above ~10 swamp text relevance; keep them modest.
- Synonyms and analyzers often matter more than boosts.

## Verify
NDCG@10 on the judgement set improves and does not regress for the top queries.
