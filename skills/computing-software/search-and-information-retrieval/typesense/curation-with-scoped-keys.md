---
id: computing-software.search-and-information-retrieval.typesense.curation-with-scoped-keys
name: curation-with-scoped-keys
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [curation-scoped-key, rule-filter-by, filter-curated-hits, typesense]
level: sme
status: docs-checked
description: "Make Typesense curation rules fire for scoped search keys: rule.filter_by must equal the combined (request) && (key) filter string; embed filter_curated_hits in the key."
sources: ["https://typesense.org/docs/30.2/api/curation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Curation with scoped API keys

A scoped key may embed a `filter_by`. When a request also has its own filter, Typesense combines them as `(request_filter) && (scoped_api_key_filter)`, with parentheses and spaces around `&&`.

Example: key embeds `{"filter_by":"country: AU"}`, the request sends `filter_by=title:hold`, so the final string is `(title:hold) && (country: AU)`. A curation rule triggered by filter must have `rule.filter_by` exactly equal to that string.

## Curated hits and embedded filters

Documents added by `includes` or by the `pinned_hits` search parameter are not filtered by the key's embedded `filter_by`. This is the same default as for the request's own filter, controlled by `filter_curated_hits`.

To return only curated hits that match, embed the flag in the key: `{"filter_by": "company_id:124", "filter_curated_hits": true}`. Embedded parameters cannot be overridden by the search request, so curated hits always pass through the combined filter, and the request's own `filter_by` also applies to them.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Curation page (https://typesense.org/docs/30.2/api/curation.html) and its source markdown in typesense-website (placeholder rules, sort_by and filter_by examples), plus the API Keys page for curation_sets actions. Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
