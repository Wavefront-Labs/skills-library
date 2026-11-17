---
id: computing-software.search-and-information-retrieval.apache-solr.filter-queries-caching
name: filter-queries-caching
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [filter-queries, filter-query, filter-cache-fq, post-filter, cache-false, cost-local-param]
level: practitioner
status: docs-checked
description: "Use Solr fq filter queries well: independent caching, cache=false and cost for expensive filters, post filters at cost 100 or more, and filter() clauses."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/common-query-parameters.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# filter-queries-caching

Each `fq` is cached independently in the filter cache and does not affect scoring. Rule of thumb from the guide: put clauses that are often used together in one `fq` with mandatory (`+`) clauses; use separate `fq` parameters for clauses that are mostly independent.

`filter(condition)` inside an `fq` caches clauses individually, which also allows a union of cached filters.

Local params on a filter:
- `cache=false` skips the filter cache, for queries unlikely to repeat, for example `fq={!geofilt cache=false}`.
- `cost` orders non-cached filters; cheaper ones run first. Default cost is 0.
- Post filter: a non-cached filter with `cost>=100` whose query implements `PostFilter` runs after the main results match. `{!frange}` defaults to cost 100 because it works best as a post filter. Multiple post filters are ordered by cost.

Make sure a filter cache is configured and sized for your `fq` volume (see the caches page).

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Common Query Parameters page (fq section and cache Local Parameter): independent caching, the single fq versus separate fq rule, `filter(condition)`, `cache=false`, `cost`, post filters at `cost>=100` with `PostFilter`, default cost 0 and `{!frange}` default 100. The statement that fq does not affect scoring is the page's own wording (restrict documents without influencing score).

Method: documentation only; no commands were run.
