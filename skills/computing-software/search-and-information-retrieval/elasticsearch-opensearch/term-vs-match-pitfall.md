---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.term-vs-match-pitfall
name: term-vs-match-pitfall
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, term-vs-match-pitfall, es-term-level-queries]
level: practitioner
status: docs-checked
description: "Avoid the classic term-on-text mistake and choose term, terms, ids and exists for exact keyword data."
sources:
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-term-query
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-terms-query
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-exists-query
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-ids-query
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# term versus match on text fields

**Goal:** correct exact matching.
- `term` does not analyse its input and looks for the exact term. A `text` field is analysed at index time (the standard analyzer removes most punctuation, splits into tokens and lowercases them), so `{"term":{"title":"Quick"}}` on a `text` field can return poor or no results.
- Use `match` for `text` fields (it analyses the search term too); use `term` on keyword fields for exact values.
- `terms` matches any of a list of terms; the default maximum is 65,536 terms (`index.max_terms_count`). Terms lookup fetches the values from an existing document (its `_source` must be enabled; not usable across clusters with cross-cluster search).
- `exists` returns documents that contain an indexed value for the field; `ids` matches by `_id`.
- Failure mode: `exists` is false when the source value is `null` or `[]`, when the field is mapped with `index: false` and `doc_values: false`, when the value exceeds `ignore_above`, or when a malformed value was skipped via `ignore_malformed`. A custom `null_value` mapping, or an array like `[null, "foo"]`, counts as existing.

## Verify
- [ ] The same value matches via `match` on a text field and `term` on a keyword field.

## Scope
The Elasticsearch reference pages were checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch reference pages for the term, terms, exists and ids queries. Confirmed: all statements above. Removed: the `_analyze?field=` debug hint and the `.keyword` sub-field naming (not on the pages read), and the OpenSearch source root.

Method: documentation only; no commands were run.
