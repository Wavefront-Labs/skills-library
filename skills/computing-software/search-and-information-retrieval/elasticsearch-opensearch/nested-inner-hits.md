---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.nested-inner-hits
name: nested-inner-hits
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, nested-inner-hits]
level: practitioner
status: docs-checked
description: "Use inner_hits on nested, has_child and has_parent queries to return which child objects matched, with from, size, sort, name and _source options."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/retrieve-inner-hits
  - https://docs.opensearch.org/latest/query-dsl/joining/nested/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# inner_hits for nested and join

**Goal:** show which nested objects or child/parent documents caused a hit.
- Add `"inner_hits":{}` inside a `nested`, `has_child` or `has_parent` query. Each search hit then carries `inner_hits.<name>.hits.hits`.
- Options: `from`, `size` (by default the top three matching hits are returned), `sort` (default: by score) and `name`. The default `name` is the nested path for `nested`, the child type for `has_child`, and the parent type for `has_parent`. Set `name` when a request has several inner hits definitions.
- Per-document features in inner hits: highlighting, explain, search fields, source filtering, script fields, doc value fields, versions, sequence numbers and primary terms.
- Nested hits include `_nested` with the `field` and the `offset` of the object in the `_source` array. The offset can differ from the position in `inner_hits` because of sorting and scoring.
- By default the `_source` of an inner hit is relative to `_nested` (only the comment, not the whole document).
- Nested documents have no `_source` of their own: Elasticsearch parses the root document's source for each inner hit, which costs time when `size` and the inner `size` are high. To avoid it, set `"_source":false` and use `docvalue_fields`, for example `comments.text.keyword`.
- Multi-level nesting: address a deeper level with its dot-notated path (`comments.votes`); this indirect referencing is supported for nested inner hits only. The `_nested` metadata then nests too.
- OpenSearch documents the same `inner_hits` parameter on the nested query, with the same `_nested` offset and relative `_source` behaviour.
- Postings offsets (`index_options: offsets`) of nested string fields are not available in the main highlighting phase, so highlight nested fields through inner hits; the same applies to `docvalue_fields` and `stored_fields` on nested fields.

```
{"query":{"nested":{"path":"comments","query":{"match":{"comments.number":2}},"inner_hits":{}}}}
```

## Verify
- [ ] The inner hit `_nested.offset` points at the expected element of the array in `_source`.
- [ ] Setting `size` above 3 returns more than the default three inner hits when more match.

## Checked
2026-11-08. Confirmed against the Elasticsearch Retrieve inner hits page and the Elasticsearch nested field type page, and the OpenSearch nested query page: options and defaults, response structure, `_nested` offset, relative `_source`, source-extraction cost and the doc-values workaround, hierarchical paths, supported per-hit features.
Removed: `index.max_inner_result_window` and the error beyond it (not on the pages read), and the OpenSearch inner-hits section root (only the nested query page was read in full).
Method: documentation only; no commands were run.
