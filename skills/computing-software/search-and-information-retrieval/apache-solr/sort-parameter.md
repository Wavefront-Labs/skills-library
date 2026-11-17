---
id: computing-software.search-and-information-retrieval.apache-solr.sort-parameter
name: sort-parameter
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [sorting, sort-parameter, sort-fields, function-sort, sortabletext, tie-breaker]
level: intro
status: docs-checked
description: "Sort Solr results with the sort parameter: score desc default, multiple criteria, function sorts, sortable field requirements, multivalued fields and the unstable tie-breaker."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/common-query-parameters.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sort-parameter

`sort` defaults to `score desc`. Examples: `price asc`, `inStock desc, price asc`, `div(popularity,price) desc`.

Sortable inputs:
- Document score and function results.
- Single-valued primitive fields with `docValues="true"` (or `indexed="true"`, in which case structures are built on the fly).
- Single-valued `SortableTextField`, which sorts on the original input regardless of analysis.
- Single-valued `TextField` whose analyzer yields one term, such as with `KeywordTokenizer`; a docValues-like structure is built at runtime.
- Multivalued primitive fields with docValues: ascending uses the minimum value, descending the maximum. `categories asc` equals `field(categories,min) asc`.

To sort on text you also tokenize for search, `copyField` it into a second field and sort on the copy.

Later criteria apply only when earlier ones tie. If everything ties, Solr falls back to the Lucene document ID, which changes with segment merges and updates, so ordering can shift; add a unique field as the last criterion for stability.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Common Query Parameters page (sort Parameter section): default `score desc`, the example sorts, the sortable field types, min/max for multivalued fields, the copyField note, multiple criteria and the Lucene document ID tie-breaker. Nothing removed.

Method: documentation only; no commands were run.
