---
id: computing-software.database-administration.elasticsearch.term-level-queries-and-keyword-fields
name: term-level-queries-and-keyword-fields
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, query-dsl, term-query, range-query, keyword-field, multi-fields, wildcard-query]
level: practitioner
status: verified
description: "Use Elasticsearch term-level queries correctly: term/terms/range/exists/prefix on keyword vs text fields, why term on text fails, multi-fields, and expensive wildcard/regexp."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/term-level-queries.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/multi-fields.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Term-level queries and keyword vs text fields

## text vs keyword
- `text`: analyzed (lowercased, tokenized) for full-text search with `match`.
- `keyword`: stored as one exact token, used for filters, aggregations, sorting.
Dynamic mapping of a string creates both:
```json
"status": { "type": "text", "fields": { "keyword": { "type": "keyword", "ignore_above": 256 } } }
```

## The classic bug
```json
{ "query": { "term": { "status": "Shipped" } } }      // returns nothing
```
`status` (text) was indexed as token `shipped`; `term` does not analyze its input, so "Shipped"
never matches. Use the keyword sub-field:
```json
{ "query": { "term": { "status.keyword": "Shipped" } } }
```
Map identifiers, statuses, tags, emails as `keyword` explicitly in your index template.

## Term-level queries (exact, put them in filter context)
```json
{ "query": { "bool": { "filter": [
  { "term":   { "customer_id": "C-1001" } },
  { "terms":  { "status": ["open", "pending"] } },
  { "range":  { "created_at": { "gte": "now-7d/d", "lt": "now/d" } } },
  { "exists": { "field": "shipped_at" } },
  { "prefix": { "sku": "AB-" } },
  { "ids":    { "values": ["1", "2"] } }
] } } }
```
Filter context skips scoring and is cacheable. Date math (`now-7d/d`) rounding helps caching.
`range` works on numbers, dates, keywords (lexicographic) and IP fields.
`terms` with a lookup: `{ "terms": { "user_id": { "index": "groups", "id": "g1", "path": "members" } } }`.

## Expensive queries
`wildcard`, `regexp`, `fuzzy`, and `prefix` on high-cardinality keyword fields scan the term
dictionary. Leading wildcards (`*abc`) are the worst.
- `search.allow_expensive_queries: false` blocks them cluster-wide.
- Alternatives: the `wildcard` field type for log-like substring search, `index_prefixes` on
  text fields, n-gram analyzers, or `match_phrase_prefix` for autocomplete.

## Case-insensitive exact match
`"term": { "email": { "value": "a@b.com", "case_insensitive": true } }`, or a keyword
field with a lowercase **normalizer** in the mapping (better for aggregations).

## Verify
`GET index/_mapping/field/status*` shows the keyword field; the term query on `.keyword`
returns the expected hits; `_validate/query?explain` shows how a query is rewritten.
