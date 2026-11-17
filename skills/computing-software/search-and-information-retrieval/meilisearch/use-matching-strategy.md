---
id: computing-software.search-and-information-retrieval.meilisearch.use-matching-strategy
name: use-matching-strategy
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [matching-strategy, last-all-frequency, query-terms, meilisearch]
level: practitioner
status: docs-checked
description: "Pick the Meilisearch matchingStrategy search parameter (last, all or frequency) to trade recall for precision on multi-word queries."
sources: ["https://www.meilisearch.com/docs/capabilities/full_text_search/how_to/use_matching_strategy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Use matchingStrategy

`matchingStrategy` is a search parameter deciding whether all query words are required or some may be dropped.

| Strategy | Drops terms | Best for | Results |
|---|---|---|---|
| `last` (default) | from the end of the query | general search, search-as-you-type | most |
| `all` | none, every term required | precise or technical queries, product catalogs | fewest |
| `frequency` | the most common terms first | natural-language queries | moderate |

## Behaviour

- `last`: for `batman dark knight`, first documents with all three words, then "batman" and "dark", then just "batman".
- `all`: only documents containing every word.
- `frequency`: counts how often each term occurs in the index and drops the most common first, so in `the dark knight rises` "the" goes before "rises". It helps when stop words are not configured.

## With phrases

A quoted phrase is always required whatever the strategy, which only applies to unquoted terms. For `"dark knight" batman returns`, `last` may drop "batman" then "returns", `all` requires everything, `frequency` may drop the more frequent of the two loose words.

Example request body: `{"q": "batman dark knight", "matchingStrategy": "all"}`.

## Checked

Method: docs-checked 2026-11-09 against the Meilisearch documentation source for Use matching strategy (capabilities/full_text_search/how_to/use_matching_strategy.mdx), read in full.
