---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.dynamic-mapping-control
name: dynamic-mapping-control
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, dynamic-mapping-control]
level: practitioner
status: docs-checked
description: "Set dynamic to true, false, strict or runtime and use dynamic_templates so unexpected fields do not explode the mapping."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dynamic
  - https://www.elastic.co/docs/manage-data/data-store/mapping/dynamic-templates
  - https://www.elastic.co/docs/reference/elasticsearch/index-settings/mapping-limit
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control dynamic mapping behaviour

**Goal:** stop uncontrolled field creation (mapping explosion) while still accepting wanted fields.
- `dynamic` values: `true` (default) adds new fields; `runtime` adds them as runtime fields (not indexed, loaded from `_source` at query time); `false` ignores new fields (not indexed or searchable, not added to the mapping, still in `_source` of returned hits on non-columnar indices); `strict` throws an exception and rejects the document. Inner objects inherit the parent's setting unless they set their own.
- Template for strings:
```
PUT my-index
{"mappings":{"dynamic_templates":[{"strings_as_keyword":{"match_mapping_type":"string","mapping":{"type":"keyword","ignore_above":256}}}]}}
```
- `index.mapping.total_fields.limit` (default 1000) counts fields, object mappings, field aliases and mapped runtime fields. With `dynamic` true or runtime, index requests that would exceed it fail with `Limit of total fields [X] has been exceeded`, unless `index.mapping.total_fields.ignore_dynamic_beyond_limit` is true (the extra fields then go to `_ignored`). If you raise the limit, Elastic also recommends raising `indices.query.bool.max_clause_count`; for large arbitrary key sets consider the `flattened` type.
- Failure mode: strict mode rejects documents with a new field, which breaks ingest if a producer adds one.
- Failure mode: raising the field limit hides a bad data model (keys used as field names).

## Verify
- [ ] Index a document with an unknown field and confirm the behaviour matches your `dynamic` setting.
- [ ] `GET my-index/_mapping` shows the template-applied type.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.
- Cited pages are Elasticsearch; OpenSearch was not checked here.

## Checked
2026-11-08. Read the Elasticsearch `dynamic` parameter page, the dynamic templates page (partly, via targeted search; the template body follows its documented shape but was not run) and the mapping limit settings page. Confirmed `dynamic` values, inheritance, the field limit default, what counts toward it and the error text. Removed the `strict_dynamic_mapping_exception` name (not on the pages read).
Method: documentation only; no commands were run.
