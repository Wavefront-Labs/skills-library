---
id: computing-software.database-administration.elasticsearch.runtime-fields
name: runtime-fields
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, runtime-fields, painless, schema-on-read, elasticsearch-query-dsl, mappings]
level: practitioner
status: verified
description: "Add Elasticsearch runtime fields in the mapping or at query time to compute or fix values without reindexing, and know when to promote them to indexed fields."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/runtime.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/runtime-search-request.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime fields

**Goal:** query, aggregate and sort on a value that was not indexed (or was indexed wrongly) without reindexing, accepting slower queries.

## In a search request
```json
GET logs-*/_search
{ "runtime_mappings": {
    "duration_s": { "type": "double",
      "script": { "source": "if (doc['duration_ms'].size() != 0) emit(doc['duration_ms'].value / 1000.0)" } } },
  "query": { "range": { "duration_s": { "gte": 2 } } },
  "aggs": { "p95": { "percentiles": { "field": "duration_s", "percents": [95] } } },
  "fields": ["duration_s"] }
```

## In the mapping (available to every query and Kibana)
```json
PUT logs-app/_mapping
{ "runtime": { "client_ip": { "type": "ip",
    "script": { "source": "String m = params._source.message; int i = m.indexOf('ip='); if (i >= 0) emit(m.substring(i + 3, m.indexOf(' ', i)));" } } } }
```
Reading `params._source` is much slower than `doc[...]` (doc values); prefer doc values when the input field is indexed.

## Shadowing a bad field
A runtime field with the same name as an indexed field overrides it at query time: fix a mis-parsed field immediately, then fix the ingest pipeline and reindex at leisure.

## Cost model
- Computed per matching document per query: fine for filtered dashboards, slow for full scans over billions of docs.
- Async search (`_async_search`) helps long queries.
- Types accepted in the mapping on 9.5 (all created): `boolean`, `composite` (needs `fields`), `date`, `double`, `geo_point`, `ip`, `keyword`, `long`, `lookup` (needs `target_index`, `input_field`, `target_field`, `fetch_fields`).

## Promote when hot
If a runtime field is used constantly, move it to an indexed field: remove from `runtime`, add to `properties`, populate via ingest pipeline for new data and `_update_by_query` or reindex for old data.

## Verify
Compare a few documents' runtime values with `fields` output; profile (`"profile": true`) to see time spent in the script.
