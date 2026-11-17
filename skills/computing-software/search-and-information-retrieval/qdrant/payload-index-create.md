---
id: computing-software.search-and-information-retrieval.qdrant.payload-index-create
name: payload-index-create
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [payload-index, create-index, keyword-index, field-schema, idx-create]
level: practitioner
status: docs-checked
description: "Create Qdrant payload indexes before ingesting data so filterable HNSW gets extra edges, rebuild if added later, and block unindexed filters."
sources:
  - https://qdrant.tech/documentation/manage-data/indexing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A payload index speeds up filtering on a field and helps the planner estimate filter cardinality.

```http
PUT /collections/{collection_name}/index
{ "field_name": "city", "field_schema": "keyword" }
```

Index types and what they serve:

- `keyword`: Match and Substring Match (optional prefix matching)
- `integer`: Match and Range
- `float`: Range
- `bool`: Match (as of v1.4.0)
- `geo`: Geo Bounding Box and Geo Radius
- `datetime`: Range (as of v1.8.0)
- `text`: full-text conditions
- `uuid`: like keyword, optimised for UUID values (as of v1.11.0)

Timing matters. The docs recommend creating payload indexes right after creating the collection, before ingesting data: the filterable HNSW index only gets the extra filter-aware edges when it is built after the payload indexes exist. If an index is created after data is ingested, rebuild the HNSW index to benefit. Rebuilding is resource-intensive and can take a long time, so avoid it when possible. To force it, make a small change to the HNSW config, for example bump `ef_construct` by 1 (read the current value from the collection info first), and do not revert the value afterwards.

Guidance:

- Index only the fields used in filters; indexes use extra memory and disk. If memory is tight, index the field that narrows results the most; more distinct values make an index more effective.
- Use a dot path to index a nested field.
- Queries on unindexed fields are slower and can hurt other queries. To block them, enable strict mode and set `unindexed_filtering_retrieve` to false: Qdrant then returns an error for such queries. Qdrant Cloud applies these settings to all collections by default.
- Extra HNSW edges can be turned off per field (as of v1.17.0) for payload fields only used with sparse vector search.

## Checked

2026-11-08. Confirmed against the Indexing page: create-index request, index types with version gates, create-before-ingest advice, rebuild procedure via `ef_construct`, strict-mode setting and Cloud default, selection advice. Page read by section (payload index, HNSW and rebuild parts); full-text and sparse sections skipped. Removed unconfirmed claims: `payload_m` behaviour and the advice to check collection info.
Method: documentation only; no commands were run.
