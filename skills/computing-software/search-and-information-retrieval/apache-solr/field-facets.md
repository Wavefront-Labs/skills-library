---
id: computing-software.search-and-information-retrieval.apache-solr.field-facets
name: field-facets
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [field-faceting, facet-field, facet-parameters, facet-query, facet-method, facet-mincount]
level: practitioner
status: docs-checked
description: "Run Solr field and query facets: facet.field, facet.query, facet.limit, facet.mincount, facet.sort, facet.method (enum, fc, fcs), facet.missing, overrequest and tag exclusion."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/faceting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# field-facets

Enable with `facet=true`. Common parameters:
- `facet.field`: terms of a field with counts. `facet.query`: counts for arbitrary queries.
- `facet.sort`: `count` (default when limit is above 0) or `index`.
- `facet.limit`, `facet.offset`, `facet.mincount`, `facet.missing`, `facet.prefix`, `facet.contains`, `facet.matches`, `facet.excludeTerms`.
- `facet.threads` for parallel field faceting.
- Per-field override: `f.fieldname.facet.limit`.

`facet.method` (default `fc`):
- `enum`: one filter per term, best for multivalued fields with few distinct values; size `filterCache` to hold them.
- `fc`: iterate matching docs and tally terms; good for many unique values and few values per document.
- `fcs`: per-segment, single-valued string fields; control threads with the `threads` local param; helps with rapid index changes.
An incompatible request is switched automatically (see `requestedMethod`).

Distributed accuracy: each shard is asked for `10 + 1.5 * facet.limit` terms by default; tune with `facet.overrequest.count` and `facet.overrequest.ratio`.

Tag a filter `{!tag=x}` and exclude it with `{!ex=x}` for multi-select facets.

## Checked

2026-11-04. Confirmed against the Faceting page: facet parameters, `facet.method` descriptions, `requestedMethod`, `10 + (1.5 * facet.limit)` over-request with `facet.overrequest.count` and `.ratio`, tag and exclude local params. Nothing removed.

Method: documentation only; no commands were run.
