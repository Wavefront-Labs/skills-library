---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.nested-query
name: nested-query
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, nested-query]
level: practitioner
status: docs-checked
description: "Query arrays of objects with the nested query: path, score_mode, multi-level nesting, ignore_unmapped and the must_not trap."
sources:
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-nested-query
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/nested
  - https://docs.opensearch.org/latest/query-dsl/joining/nested/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested query

**Goal:** correct matching on arrays of objects.
```
{"query":{"nested":{"path":"obj1","query":{"bool":{"must":[{"match":{"obj1.name":"blue"}},{"range":{"obj1.count":{"gt":5}}}]}},"score_mode":"avg"}}}
```
- The field must be mapped `"type":"nested"`. The query searches nested objects as if they were separate documents and returns the root parent document when an object matches. Use dot notation with the full path (`obj1.name`).
- `path` and `query` are required. `score_mode` (default `avg`): `avg`, `max`, `min`, `sum`, `none` (parent scored 0). Elasticsearch notes nested `knn` queries only support `max`.
- `ignore_unmapped` (default `false`): when `true` an unmapped path returns no documents instead of an error; useful across indices where some lack the field.
- Multi-level nesting: write one nested query per level, for example `path: driver` containing `path: driver.vehicle`. All conditions in the inner `bool` must then match the same inner object. With `object` instead of `nested`, the values are flattened and conditions can match across objects.
- A `script` query inside a nested query sees only the nested document's doc values, not the parent or root.
- `must_not` trap: if any nested object matches the inner query, the parent is returned even when other objects in it do not. A `must_not` inside the nested query on `author: nik9000` still returns a document having both `kimchy` and `nik9000`. To exclude parents that have any such object, put `must_not` outside, around the `nested` query.
- Add `inner_hits` to see which nested objects matched (see the nested-inner-hits skill).
- Nested documents are reachable only through the nested query, the `nested` and `reverse_nested` aggregations, nested sorting and nested inner hits.

## Verify
- [ ] A document whose two comments are (ana, 2 stars) and (bob, 5 stars) does not match author ana with stars at least 4.
- [ ] The outer `must_not` form excludes a document that has one matching comment among several.

## Checked
2026-11-08. Confirmed against the Elasticsearch nested query and nested field type pages and the OpenSearch nested query page: parameters and defaults, score_mode values, multi-level example, ignore_unmapped, script-query scope, must_not behaviour, access paths for nested documents.
Removed: the claim that querying a nested field without `nested` returns no hits (the docs say nested documents are only accessible within nested scope; the cross-match behaviour is for object fields) and unconfirmed-cluster boilerplate.
Method: documentation only; no commands were run.
