---
id: computing-software.search-and-information-retrieval.meilisearch.sort-search-results
name: sort-search-results
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [sortable-attributes, sort-parameter, sort-ranking-rule, meilisearch]
level: practitioner
status: docs-checked
description: "Let users sort Meilisearch results with sortableAttributes and the sort parameter (attr:asc or desc), including ranking rule placement and nested fields."
sources: ["https://www.meilisearch.com/docs/capabilities/filtering_sorting_faceting/how_to/sort_results"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sort search results

## Setup

1. Choose the fields and add them to the `sortableAttributes` index setting. Fields may hold numbers, strings, or arrays of those.
2. Optionally reorder `rankingRules`.

Gotchas: sorting is lexicographic by byte value, so `á` (225) sorts after `z` (122), and uppercase sorts as lowercase. If a field mixes types, numbers take precedence over strings, so sort only on homogeneous fields. A sortable attribute that no document has is accepted silently, so a typo only shows up as unsorted results.

## Query

`sort` takes `attribute:asc` or `attribute:desc`. POST body uses an array: `"sort": ["price:asc", "author:desc"]`. GET uses a comma-separated string: `sort="price:desc,author:asc"`. Earlier entries have priority; ties fall to the next. Nested fields use dot notation, such as `rating.users:desc`.

## Relevance versus sort

By default `sort` is the fifth rule, so closely matching documents come first and sort only breaks ties (relevant sorting). Moving `sort` higher gives exhaustive sorting that follows the user's order more strictly but is less relevant, appropriate when finding cheaper items matters more than the best textual match.

Sorting works well with placeholder search. It applies equally to all documents, so for always-on promotion use custom ranking rules instead.

## Checked

Method: docs-checked 2026-11-09 against the Meilisearch documentation source for Sort search results (meilisearch/documentation repo, capabilities/filtering_sorting_faceting/how_to/sort_results.mdx), read in full; code snippets are includes and were not read.
