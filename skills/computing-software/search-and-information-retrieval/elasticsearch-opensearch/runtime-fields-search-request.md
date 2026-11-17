---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.runtime-fields-search-request
name: runtime-fields-search-request
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, runtime-fields-search-request]
level: advanced
status: docs-checked
description: "Define runtime_mappings per Elasticsearch search request to compute ad hoc fields, shadow mapped fields and aggregate on them."
sources:
  - https://www.elastic.co/docs/manage-data/data-store/mapping/define-runtime-fields-in-search-request
  - https://www.elastic.co/docs/manage-data/data-store/mapping/runtime-fields
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime fields in a search request (Elasticsearch)

**Goal:** one-off computed fields that exist only for the request.
```
GET my-index-000001/_search
{"runtime_mappings":{"duration":{"type":"long","script":{"source":"emit(doc['measures.end'].value - doc['measures.start'].value);"}}},
 "aggs":{"duration_stats":{"stats":{"field":"duration"}}}}
```
- `runtime_mappings` uses the same format as the `runtime` section of the index mapping; copy the definition across.
- The field exists only within that request, but you can search, sort and aggregate on it.
- Runtime fields take precedence over mapped fields of the same name, so you can shadow a field to fix a mapping mistake (for example map text `measures.start` as `long` to run `avg`) without changing the data. The page shows this with `PUT <index>/_mapping {"runtime":{...}}`; the same shadowing works in `runtime_mappings`.
- A runtime field can return values computed from other runtime fields.
- Runtime fields do not appear in `_source`; use `fields` on `_search` to retrieve their values.
- Queries against runtime fields are expensive and are rejected when `search.allow_expensive_queries` is false. The page recommends async search to offset the cost.
- Failure mode: assuming the field is stored; it exists only for the request.
- OpenSearch: not covered; its equivalent page could not be read.

## Verify
- [ ] The aggregation or `fields` section of the response contains the computed values.

## Checked
Checked 2026-11-08 against the Elasticsearch pages "Define runtime fields in a search request" and "Runtime fields" (same format as mapping, precedence over mapped fields, aggregations on request-only fields, `fields` retrieval, expensive-query rule, async search). Only Elasticsearch was checked. Removed: the `params.rate` example script (not shown on the pages) and the OpenSearch references.
Method: documentation only; no commands were run.
