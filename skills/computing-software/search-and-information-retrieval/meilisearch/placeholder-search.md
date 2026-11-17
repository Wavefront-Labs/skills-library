---
id: computing-software.search-and-information-retrieval.meilisearch.placeholder-search
name: placeholder-search
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [placeholder-search, empty-query, browse-results, meilisearch]
level: practitioner
status: docs-checked
description: "Send an empty or missing q to Meilisearch to list documents by sort and custom ranking, combined with filters and facets for landing pages and category browsing."
sources: ["https://www.meilisearch.com/docs/capabilities/full_text_search/getting_started/placeholder_search"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Placeholder search in Meilisearch

A placeholder search is a search request where `q` is empty (`"q": ""`) or absent. Meilisearch skips text matching and returns documents instead of nothing, still honouring every other search parameter.

## Ordering

With no query terms, the text-based ranking rules `words`, `typo`, `proximity` and `exactness` have no effect. The order comes from the `sort` parameter and custom ranking rules, which therefore matter most. Without them you get the default order.

## Combinations

- Filter plus sort: `{"q": "", "filter": "genres = Action", "sort": ["rating:desc"]}` lists action movies by rating without any typing.
- Facets: `{"q": "", "facets": ["genres", "release_year"]}` adds a `facetDistribution` object with document counts per value, which drives category navigation.
- Pagination works as usual with `offset` and `limit`, or `page` and `hitsPerPage`.

## Typical uses

Landing pages, category browsing, default recommendations (sort by a custom ranking attribute like `popularity`), and showing facet counts before the user searches.

## Checked

Method: docs-checked 2026-11-09 against the Meilisearch documentation source for Placeholder search (capabilities/full_text_search/getting_started/placeholder_search.mdx), read in full.
