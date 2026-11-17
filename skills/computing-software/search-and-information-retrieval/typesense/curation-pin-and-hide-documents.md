---
id: computing-software.search-and-information-retrieval.typesense.curation-pin-and-hide-documents
name: curation-pin-and-hide-documents
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [curation-sets, pin-documents, exclude-documents, typesense]
level: practitioner
status: docs-checked
description: "Pin documents to positions and hide others for a query with a Typesense v30 curation set: PUT /curation_sets/:name with rule.query, match exact or contains, includes and excludes."
sources: ["https://typesense.org/docs/30.2/api/curation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Curation: include and exclude documents

`PUT /curation_sets/curate_products` with:

```json
{"items": [{"id": "customize-apple",
  "rule": {"query": "apple", "match": "exact"},
  "includes": [{"id": "422", "position": 1}, {"id": "54", "position": 2}],
  "excludes": [{"id": "287"}]}]}
```

Documents 422 and 54 take positions 1 and 2 for the query `apple`; document 287 is removed. Use either `includes` or `excludes`, or both.

## match

`exact` applies only when the whole query equals `apple`. `contains` applies to every query containing the word. `rule.match` is required when `rule.query` is set.

## After creating

Link the set to a collection (see the linking skill). The response returns `{"name": "curate_products", "items": [...]}`.

## Ordering

Curation runs before synonyms, since a rule can replace the query; synonyms then work on the modified query.

## Pinned documents and filters

Set `filter_curated_hits: true` so a request `filter_by` also removes curated documents. Surviving pinned ones slide up: with QWE127, DEF456 and CVB333 pinned to 1, 2 and 3 and an in-stock filter, DEF456 (sold out) is dropped and CVB333 moves to position 2.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Curation page (https://typesense.org/docs/30.2/api/curation.html) and its source markdown in typesense-website (placeholder rules, sort_by and filter_by examples), plus the API Keys page for curation_sets actions. Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
