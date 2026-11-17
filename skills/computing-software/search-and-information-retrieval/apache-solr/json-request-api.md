---
id: computing-software.search-and-information-retrieval.apache-solr.json-request-api
name: json-request-api
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [json-request, json-request-api, json-query-dsl, json-params, bool-query, query-dsl]
level: practitioner
status: docs-checked
description: "Send Solr queries as JSON bodies: query, filter, fields, params and facet keys, the json. prefixed parameters, merge precedence, bool DSL and the lucene, edismax query forms."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/json-request-api.html
  - https://solr.apache.org/guide/solr/latest/query-guide/json-query-dsl.html
  - https://solr.apache.org/guide/solr/latest/query-guide/json-combined-query-dsl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# json-request-api

POST JSON to `/query`. Basic body: `{"query":"memory","filter":"inStock:true"}`. JSON can also go into `json=` or `json.<key>=` parameters, which override or supplement the body.

Merge precedence when a property appears in several places: traditional parameters (`q`, `rows`) win; then `json`-prefixed parameters; the body has lowest precedence. Multivalued properties such as `filter` and `fields` keep all values; single-valued ones take the highest-precedence value.

Query DSL: a query can be a string, or an object such as `{"lucene":{"df":"name","query":"iPod"}}`, `edismax`, or a `bool` object with `must`, `must_not`, `should` and `filter` arrays whose entries can be strings or nested parser objects.

Some features, such as most JSON Facet analytics, are only reachable through this API.

Combined Query (hybrid search, such as Reciprocal Rank Fusion) uses `solr.CombinedQuerySearchHandler` and a `CombinedQueryComponent`; `maxCombinerQueries` caps queries (default 5). It does not support grouping or cursors, and always runs distributed. In user-managed mode, shard URLs must be allow-listed or Solr returns 403.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide JSON Request API, JSON Query DSL and JSON Combined Query DSL pages: `json` and `json.<key>` parameters, the three-level precedence and multivalued merging, the bool and parser-object query forms, JSON-only facet analytics, `CombinedQuerySearchHandler`, `CombinedQueryComponent`, `maxCombinerQueries` default 5, no grouping or cursors, always distributed, and the 403 without an allow-listed shard URL. Nothing removed.

Method: documentation only; no commands were run.
