---
id: computing-software.search-and-information-retrieval.typesense.curation-diversify-results
name: curation-diversify-results
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [mmr-diversity, diversity-lambda, similarity-metric, typesense]
level: sme
status: docs-checked
description: "Diversify the top 250 Typesense hits with Maximum Marginal Relevance via a curation diversity block: jaccard, equality and vector_distance metrics, weights and diversity_lambda."
sources: ["https://typesense.org/docs/30.2/api/curation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diversifying results with MMR

A curation item can carry a `diversity` object. Typesense re-ranks the top 250 hits with Maximum Marginal Relevance: pick the next document that balances relevance to the query against its maximum similarity to documents already selected.

## Example

```json
{"id": "override_id",
 "rule": {"tags": ["screen_pattern_rule"]},
 "diversity": {"similarity_metric": [
   {"field": "tags", "method": "jaccard", "weight": 0.7},
   {"field": "app_id", "method": "equality", "weight": 0.3}]}}
```

Relevance to the query is computed for every document. `similarity_metric` defines how similar two documents are; weights combine the fields.

## Methods

- `equality`: exact match of field value(s), 1 if the same, otherwise 0; works for single and array fields.
- `jaccard`: Jaccard index of the values; array fields only.
- `vector_distance`: similarity via the vector field.

The field must be `facet: true` for an array type, otherwise `sort: true`.

## Lambda

Send `diversity_lambda` with the search: `{"q": "*", "curation_tags": "screen_pattern_rule", "diversity_lambda": 0.75}`. At 1 there is no diversity; at 0 maximum diversity. Default `0.5`.

Rules can alternatively fire on query or filter matches instead of tags.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Curation page (https://typesense.org/docs/30.2/api/curation.html) and its source markdown in typesense-website (placeholder rules, sort_by and filter_by examples), plus the API Keys page for curation_sets actions. Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
