---
id: computing-software.database-administration.elasticsearch.nested-and-join-queries
name: nested-and-join-queries
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, nested-query, has-child, has-parent, join-field, elasticsearch-query-dsl]
level: practitioner
status: verified
description: "Query arrays of objects correctly with nested fields and nested queries, and parent-child relations with join fields (has_child, has_parent), with costs and limits."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/nested.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-nested-query.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/parent-join.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested and join queries

## The object-array problem
With default `object` mapping, `{"comments":[{"author":"ann","stars":5},{"author":"bob","stars":1}]}` is flattened: a query for author=ann AND stars=1 matches. Use `nested` when per-object correlation matters.

## Nested
```json
PUT blog { "mappings": { "properties": { "comments": { "type": "nested",
  "properties": { "author": { "type": "keyword" }, "stars": { "type": "integer" } } } } } }

GET blog/_search
{ "query": { "nested": { "path": "comments", "score_mode": "max",
    "query": { "bool": { "filter": [ { "term": { "comments.author": "ann" } }, { "range": { "comments.stars": { "gte": 4 } } } ] } },
    "inner_hits": { "size": 3 } } } }
```
- Each nested object is a hidden Lucene document: 100 comments = 101 docs. Updates re-index the whole parent.
- Limits: `index.mapping.nested_fields.limit` (100 on 9.5), `index.mapping.nested_parents.limit` (50), `index.mapping.nested_objects.limit` (10000 per doc); read the defaults with `GET <index>/_settings?include_defaults=true`.
- Aggregate with `nested` + `reverse_nested` aggregations; sort with `nested` sort options.

## Join (parent-child)
```json
PUT qa { "mappings": { "properties": { "rel": { "type": "join", "relations": { "question": "answer" } } } } }
PUT qa/_doc/1 { "title": "How to reindex?", "rel": "question" }
PUT qa/_doc/2?routing=1 { "body": "Use the reindex API", "rel": { "name": "answer", "parent": "1" } }

GET qa/_search { "query": { "has_child": { "type": "answer", "query": { "match": { "body": "reindex" } }, "score_mode": "max" } } }
GET qa/_search { "query": { "has_parent": { "parent_type": "question", "query": { "match": { "title": "reindex" } } } } }
```
- Children must be routed to the parent's shard (`routing=<parent id>`).
- Children update independently (good for frequently changing child data); the join field builds global ordinals eagerly on refresh, which can add significant refresh time, and join queries cost more than nested ones.

## Which one
| Need | Choose |
|---|---|
| Small arrays, read-heavy | nested |
| Many children, frequent child updates | join |
| No per-object correlation | plain object (or flatten) |
| Data rarely changes | denormalise into the parent |

## Verify
Test the cross-object false positive: the ann/stars=1 query must return 0 hits with nested mapping.
