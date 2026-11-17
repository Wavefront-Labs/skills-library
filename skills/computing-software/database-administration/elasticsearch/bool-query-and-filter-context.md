---
id: computing-software.database-administration.elasticsearch.bool-query-and-filter-context
name: bool-query-and-filter-context
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, opensearch, query-dsl, bool-query, filter-context, query-context, must-should-filter, minimum-should-match, query-cache, term-vs-match]
level: practitioner
status: verified
description: "Build Elasticsearch bool queries that put non-scoring clauses in filter context for caching and speed, use should/minimum_should_match correctly, and avoid term-on-text bugs."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bool query and filter context

**Goal:** searches that score only what affects relevance and run the rest as
cached yes/no filters.

## Shape
```json
GET products/_search
{
  "query": {
    "bool": {
      "must":   [ { "match": { "title": "running shoes" } } ],
      "filter": [ { "term":  { "status": "active" } },
                  { "range": { "price": { "lte": 120 } } },
                  { "terms": { "brand.keyword": ["acme", "zoom"] } } ],
      "should": [ { "match_phrase": { "title": { "query": "trail running", "boost": 2 } } } ],
      "must_not": [ { "term": { "discontinued": true } } ]
    }
  }
}
```
| Clause | Scores? | Cached? | Meaning |
|---|---|---|---|
| must | yes | no | must match, contributes to score |
| filter | no | eligible (node query cache, segment-level, see Performance) | must match |
| should | yes | no | optional boost; see below |
| must_not | no | eligible (same cache rules) | exclude |

## should semantics
- With a `must` or `filter` present, `should` clauses are optional (boost only)
  unless `minimum_should_match` is set.
- With only `should` clauses, at least one must match (`minimum_should_match` defaults to 1).
- `"minimum_should_match": "2<75%"` style for "most of these terms".

## term vs match
`term` does not analyze the input; against a `text` field (lowercased, tokenized)
`{"term": {"title": "Running Shoes"}}` matches nothing. Use `term` on `keyword`
fields (`brand.keyword`), `match` on `text`.

## Performance
- Put everything that doesn't need relevance in `filter`: dates, statuses,
  tenant ids, permissions. Scoring is skipped and repeated filters can be cached.
- The query cache only caches segments with at least 10,000 documents and at least 3% of the shard's documents (`indices.queries.cache.all_segments` is `false` by default), so a small test index shows 0 in the `query_cache` stats however often a filter repeats.
- `constant_score` wraps a filter when you need a query with no scoring at all.
- Avoid leading wildcards and `script` queries in filters on large indices.

## Verify
`"profile": true` in the request shows per-clause time; `"explain": true` on a
hit shows which clauses scored. `GET _nodes/stats/indices/query_cache` `hit_count`
rises when filters are reused on segments big enough to be cached (a 5-document test index stays at 0).
