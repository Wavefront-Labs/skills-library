---
id: computing-software.search-and-information-retrieval.meilisearch.configure-prefix-search
name: configure-prefix-search
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [prefix-search, search-as-you-type, indexing-time, meilisearch]
level: practitioner
status: docs-checked
description: "Choose Meilisearch prefixSearch, indexingTime (default) or disabled, trading search-as-you-type against index size and indexing speed."
sources:
  - https://www.meilisearch.com/docs/capabilities/full_text_search/how_to/configure_prefix_search
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configure prefix search

Prefix search matches the beginning of the last word of a query, so `adv` finds "adventure". It powers search-as-you-type. The index setting `prefixSearch` has two modes:

| Mode | Effect |
|---|---|
| `indexingTime` | Default. Prefix structures are built while indexing: fast prefix queries, larger index, longer indexing. |
| `disabled` | Only whole-word matches. Smaller index and faster indexing, but users must type complete words. |

Get, update and reset operations exist on the settings endpoint; reset returns to `indexingTime`.

## Decide

Disable it for form-style search with a submit button, large datasets under performance pressure, or when partial matches add noise. Keep it for search-as-you-type, autocomplete and discovery.

## Caveats

- Changing the setting re-indexes all documents asynchronously; monitor the task.
- Prefix matching only applies to the last word of a multi-word query. `harry pot` matches "Harry Potter" because "harry" matches fully and "pot" is a prefix; earlier words must match completely or within typo tolerance.

## Checked

Method: 2026-11-09 docs-only read of the cited page in full. All claims match the page; unchanged except the shortened description.
