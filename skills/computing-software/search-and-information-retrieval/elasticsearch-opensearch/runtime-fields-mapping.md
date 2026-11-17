---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.runtime-fields-mapping
name: runtime-fields-mapping
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, runtime-fields-mapping, es-runtime-fields]
level: advanced
status: docs-checked
description: "Define schema-on-read runtime fields in the Elasticsearch mapping with Painless emit and query them like normal fields."
sources:
  - https://www.elastic.co/docs/manage-data/data-store/mapping/runtime-fields
  - https://www.elastic.co/docs/manage-data/data-store/mapping/map-runtime-field
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime fields in the mapping (Elasticsearch)

**Goal:** add fields to existing documents without reindexing.
```
PUT my-index-000001
{"mappings":{"runtime":{"day_of_week":{"type":"keyword","script":{"source":"emit(doc['@timestamp'].value.dayOfWeekEnum.getDisplayName(TextStyle.FULL, Locale.ENGLISH))"}}},"properties":{"@timestamp":{"type":"date"}}}}
```
- A runtime field is evaluated at query time and is not indexed, so it adds nothing to index size; search speed decreases.
- The Painless script must call `emit` to return values. It can read mapped fields via `doc[...]` and `_source` via `params._source`.
- Allowed `type` values in the `runtime` section: boolean, composite, date, double, geo_point, ip, keyword, long, lookup. A `date` runtime field accepts `format` like the date field type.
- Without a `script`, Elasticsearch reads the same-named field from `_source` at query time; prefer `doc_values` when the field has them (faster than `_source`).
- `on_script_error`: `fail` (default) causes a shard failure reported in the response; `continue` silently ignores errors on that field.
- Update by adding a runtime field of the same name; remove with `PUT my-index-000001/_mapping {"runtime":{"day_of_week":null}}`. Changing or removing one while queries run can give inconsistent results, and Kibana visualisations using it can break.
- Index the fields you search and filter on often (for example a timestamp); Elasticsearch uses indexed fields first. Changing a runtime field to an indexed field needs no query changes.
- Queries on runtime fields count as expensive: with `search.allow_expensive_queries` set to false they are rejected.
- Use the `fields` parameter to retrieve values (they do not appear in `_source`); with `fields` the script runs only on top hits.
- `"dynamic": "runtime"` makes newly seen fields runtime fields.
- OpenSearch: not covered here; its equivalent feature page could not be read, so check its docs.

## Verify
- [ ] Search and aggregate on the new field works with no reindex.

## Checked
Checked 2026-11-08 against the Elasticsearch pages "Runtime fields" and "Map a runtime field" (type list, emit, no-script _source lookup, on_script_error, null removal, expensive-query rule, dynamic runtime). Only Elasticsearch was checked. Removed: the unconfirmed OpenSearch derived-fields equivalence and the Locale.ROOT example (page uses Locale.ENGLISH).
Method: documentation only; no commands were run.
