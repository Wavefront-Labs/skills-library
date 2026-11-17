---
id: computing-software.search-and-information-retrieval.meilisearch.configure-searchable-attributes
name: configure-searchable-attributes
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [searchable-attributes, attributes-to-search-on, attribute-ranking, meilisearch]
level: practitioner
status: docs-checked
description: "Set Meilisearch searchableAttributes to choose and order searched fields, with reindexing caveats and the attributesToSearchOn override."
sources:
  - https://www.meilisearch.com/docs/capabilities/full_text_search/how_to/configure_searchable_attributes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configure searchable attributes

By default `searchableAttributes` is `["*"]`: every field is searched, in order of appearance. Narrowing it helps relevancy, because a match in an earlier-listed field outranks one in a later field, and performance, because fewer fields are scanned.

Example for a movies index: list `title`, then `overview`, then `genres`; leave out `id` and `release_date`, which are useless for text.

## Operations

Use the index settings endpoints to get, update or reset `searchableAttributes`. Reset restores `["*"]`.

## Warnings from the docs

- Updating triggers re-indexing of all documents, an asynchronous task you follow through the tasks API.
- After a manual update, new attributes appearing in later documents are not added automatically. Add them yourself or reset the setting.
- Known issue: a manual update changes the displayed field order in JSON responses; do not depend on field order.

## Per-query restriction

`attributesToSearchOn` in the search body (for example `["title"]`) limits one request to a subset of the configured searchable attributes. Documents matching only in other fields are silently excluded, with no error, so results can be narrower than expected.

## Checked

Method: 2026-11-09 docs-only read of the cited page in full. All claims match the page; unchanged except the shortened description.
