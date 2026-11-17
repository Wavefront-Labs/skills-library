---
id: computing-software.search-and-information-retrieval.meilisearch.facet-search
name: facet-search
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [facet-search, facet-query, exhaustive-facet-count, meilisearch]
level: practitioner
status: docs-checked
description: "Use the Meilisearch /facet-search endpoint for type-ahead over facet values, with its string-only and first-term-only limits and exhaustiveFacetCount."
sources: ["https://www.meilisearch.com/docs/capabilities/filtering_sorting_faceting/how_to/facet_search"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Facet search

Facet search searches within the values of one facet, powering auto-complete on filter menus whose facet has thousands of values (brands, authors).

## Setup and request

The attribute must be in `filterableAttributes`. Facet search is on by default; the index setting `facetSearch` can disable it to speed up indexing. Send `POST /indexes/<index>/facet-search` with the facet name and the typed text in `facetQuery`. The response has `facetHits`, an array of `{value, count}`, plus `facetQuery`. You can narrow with `q`, `filter` and `matchingStrategy`.

## Limitations

- String values only. Numbers are stored as float64, which makes prefix matching on their text unreliable; convert numeric facets to strings (`"rating": "4.5"`) before indexing.
- Only the first term of `facetQuery` is used; later words are dropped. For an `author` value "Jane Austen", `Jane` matches, `Austen` does not (not the start of the value), and `Jane Aus` behaves like `Jane`. For multi-word matching run a normal search with `q` and read `facetDistribution`.

## Counts

Counts are estimates by default. Set `exhaustiveFacetCount` to `true` for exact counts, which is slower; use it when accuracy matters, such as storefront category counts.

## Checked

2026-11-03. Confirmed claim by claim against the Facet search page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
