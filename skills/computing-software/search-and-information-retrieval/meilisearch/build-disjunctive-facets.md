---
id: computing-software.search-and-information-retrieval.meilisearch.build-disjunctive-facets
name: build-disjunctive-facets
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [disjunctive-facets, faceted-navigation, multi-search-facets, meilisearch]
level: advanced
status: docs-checked
description: "Build ecommerce-style disjunctive facets in Meilisearch client-side using multi-search with limit 0 per-group queries and merged facetDistribution."
sources: ["https://www.meilisearch.com/docs/capabilities/filtering_sorting_faceting/advanced/disjunctive_facets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build disjunctive facets

In ordinary (conjunctive) facets, selecting "Red" collapses the colour counts so "Blue" drops to 0. Disjunctive facets keep the other values in the selected group visible with unfiltered counts, while other groups update normally.

Meilisearch has no built-in mode; you implement it with multi-search (`POST /multi-search` with a `queries` array).

## Query plan

1. One main query with all active filters applied. It returns the hits and `facetDistribution` for groups that have no active selection.
2. One extra query per group that has active selections, with that group's filter removed, `facets` set to just that group, and `limit: 0` since only counts are needed.

Example with `color = Red` and `brand = Nike` selected: main query filters both and asks for `["size"]`; the colour query filters `brand = Nike` and asks for `["color"]`; the brand query filters `color = Red` and asks for `["brand"]`.

## Implementation notes

- Track active filters grouped by facet, for instance `{color: ["Red"], brand: ["Nike"], size: []}`.
- Build each filter string by ORing values within a group in parentheses and ANDing groups.
- Take hits and `estimatedTotalHits` from the first result, and merge the other results' `facetDistribution` objects by assignment; each group appears in exactly one query, so there are no conflicts.

Cost: one extra query per active group, but multi-search runs in one HTTP request, queries execute concurrently, and `limit: 0` skips ranking and document retrieval. With 10+ groups, only add queries for groups the user actually filtered.

## Checked

Method: docs-checked 2026-11-09 against the Build disjunctive facets page (raw mdx of github.com/meilisearch/documentation, read in full). All claims confirmed.
