---
id: computing-software.search-and-information-retrieval.apache-solr.export-handler
name: export-handler
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [export, export-handler, streaming-expressions, xport, bulk-export, result-export]
level: advanced
status: docs-checked
description: "Export entire Solr result sets with the /export handler: sort and fl required, docValues fields, includeStoredFields, batchSize and the link to streaming expressions."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/exporting-result-sets.html
  - https://solr.apache.org/guide/solr/latest/query-guide/streaming-expressions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# export-handler

`/export` streams a fully sorted result set of millions of records, sending records within milliseconds and continuing until the whole set is sorted. Uses: session analysis, distributed merge joins, time series roll-ups, aggregations on high-cardinality fields, fully distributed collapsing, sort-based stats.

Requirements:
- Every request needs `sort` and `fl`, or it errors. Filter queries are allowed.
- Sort fields must have `docValues="true"`. By default `fl` fields must too.
- `includeStoredFields=true` (default false) lets `fl` include stored-only fields, at a noticeable performance cost.
- `batchSize` (default 30000) sets internal buffer size: smaller uses less memory, larger can speed export, not linearly.

`/export` is an implicit handler whose properties are invariants, so query-time parameters cannot override them.

Streaming expressions are SolrCloud functions that emit tuples and compose search, transformation and analysis. Those designed for whole result sets rely on `/export`.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Exporting Result Sets and Streaming Expressions pages: sorting millions of records, the use cases, required `sort` and `fl`, docValues rules, `includeStoredFields` and its performance impact, `batchSize` default 30000, invariants, and streaming expressions emitting tuples with whole-result-set functions backed by `/export`. Removed the xport parser sentence and the docValues de-duplication note, which the pages do not state.

Method: documentation only; no commands were run.
