---
id: computing-software.search-and-information-retrieval.apache-solr.json-facet-terms
name: json-facet-terms
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [json-facets, json-facet, facet-domain, terms-facet, facet-stats, json-faceting]
level: advanced
status: docs-checked
description: "Build nested analytics with the Solr JSON Facet API: terms and range facets, limit and sort, overrequest and refine, numBuckets, allBuckets, prelim_sort and metric functions."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/json-facet-api.html
  - https://solr.apache.org/guide/solr/latest/query-guide/json-faceting-domain-changes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# json-facet-terms

Send facets in the JSON Request API body or `json.facet`. A bucketing facet looks like `"categories": {"type":"terms","field":"cat","limit":3}`; the response lists `buckets` with `val` and `count`. Facets nest, so metrics can be computed inside each bucket.

Types: `terms` and `range` produce many buckets; `query` and `heatmap` produce one.

Terms options: `limit`, `sort` (`count`, `index` or any metric), `overrequest`, `refine`, `overrefine` (extra buckets to refine in distributed search), `numBuckets`, `allBuckets`, `method` (`smart` default), and `prelim_sort` (approximate sort used to pick candidate buckets before refinement).

Metrics: `unique(manu_exact)`, `hll(author)`, `percentile(weight,50)` (t-digest), `relatedness(...)` for semantic knowledge graphs, plus the usual sum, avg, min, max.

Domain changes: a `domain` object can add a `filter`, or use `excludeTags` to ignore tagged `fq` filters, or switch to related documents. This is how multi-select facets work with JSON facets.

## Checked

2026-11-04. Confirmed against the JSON Facet API and Domain Changes pages: the `categories` terms example, facet types, terms options including `overrefine` and `prelim_sort`, metric functions including `relatedness`, domain `excludeTags`. Nothing removed.

Method: documentation only; no commands were run.
