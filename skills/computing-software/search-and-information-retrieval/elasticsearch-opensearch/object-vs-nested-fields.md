---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.object-vs-nested-fields
name: object-vs-nested-fields
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, object-vs-nested-fields]
level: practitioner
status: docs-checked
description: "Choose object, nested or flattened for arrays of objects: cross-object false matches, nested limits and when flattened avoids mapping explosion."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/nested
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/flattened
  - https://docs.opensearch.org/latest/query-dsl/joining/nested/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object, nested and flattened fields

**Goal:** keep array-of-object matches correct without paying for nested where it is not needed.
- Default `object` arrays are flattened internally: `user:[{first:John,last:Smith},{first:Alice,last:White}]` becomes `user.first:[alice,john]` and `user.last:[smith,white]`, so a query for Alice AND Smith wrongly matches.
- `"type":"nested"` indexes each object in the array as a separate hidden document, so a `nested` query for Alice AND Smith does not match but Alice AND White does. A document with 100 nested objects creates 101 Lucene documents.
- Elasticsearch says nested documents and queries are typically expensive. For a large, arbitrary set of keys use `flattened`, which maps a whole object as one field and indexes the leaf values as keywords (no analysis, no numeric or date handling; range queries and sorting compare as strings, highlighting is unsupported). Do not use `flattened` for all document content.
- Elasticsearch limits (settings): `index.mapping.nested_fields.limit` (default 100 distinct nested mappings per index), `index.mapping.nested_parents.limit` (default 50 nested fields that are parents of other nested fields) and `index.mapping.nested_objects.limit` (default 10000 nested JSON objects per document across all nested types). Flattened has `depth_limit` (default 20).
- Nested parameters: `dynamic`, `properties`, `include_in_parent`, `include_in_root` (both default `false`).
- If a parent object has `subobject` set to `false`, nested mappings below it are flattened and nested functionality is disabled.
- Nested fields have incomplete Kibana support: visible and searchable in Discover but not usable in Lens visualizations.
- OpenSearch: nested mapping and nested queries work the same way (its docs show that mapping `contacts` as `object` instead of `nested` would match both example documents). `flat_object` was not readable in this review; check the OpenSearch field-types page before relying on it.

## Verify
- [ ] The same two-condition `bool` query returns no hit on a `nested` mapping but a hit on a plain `object` mapping.

## Checked
2026-11-08. Confirmed against the Elasticsearch nested field type and flattened field type pages and the OpenSearch nested query page: flattening of object arrays, nested hidden documents, Lucene document count, limits and defaults, flattened behaviour, nested parameters, Kibana warning.
Removed: the claim that updating one nested child reindexes the whole parent, the three-way table equating `flat_object` with `flattened` (OpenSearch field type page returned no content), and unconfirmed-cluster boilerplate.
Method: documentation only; no commands were run.
