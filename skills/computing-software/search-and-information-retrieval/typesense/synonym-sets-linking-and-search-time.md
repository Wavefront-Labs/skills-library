---
id: computing-software.search-and-information-retrieval.typesense.synonym-sets-linking-and-search-time
name: synonym-sets-linking-and-search-time
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [synonym-sets-link, search-time-synonyms, collection-patch, typesense]
level: practitioner
status: docs-checked
description: "Attach Typesense synonym sets to a collection at creation or via PATCH, and add more sets per query with the synonym_sets search parameter; precedence with overrides."
sources: ["https://typesense.org/docs/30.2/api/synonyms.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linking synonym sets and using them in search

## Link at creation

Add `"synonym_sets": ["clothing-synonyms", "tech-synonyms"]` to the `POST /collections` body next to `name` and `fields`.

## Link to an existing collection

`PATCH /collections/products` with `{"synonym_sets": ["clothing-synonyms", "tech-synonyms"]}`.

## Per-query sets

A search looks for synonyms in the sets given by the `synonym_sets` search parameter and in the sets linked to the collection. If `products` is linked to `clothing-synonyms`, then `GET /collections/products/documents/search?q=controller&query_by=name&synonym_sets=tech-synonyms,electronics-synonyms` uses all three.

## Ordering with curation

Overrides are handled first, because rules may replace the query; synonym sets then work on the modified query.

## When synonyms do not fire

- Phrase search with double quotes: `"Site Reliability"` will not return `Infrastructure` even as a multi-way synonym.
- `filter_by`: synonyms only apply to tokens in `q`. A synonym `abc <> xyz` with `filter_by: title:=abc` matches only `title=abc`, since filters behave like a SQL `WHERE`.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Synonym Sets page (https://typesense.org/docs/30.2/api/synonyms.html) and its source markdown, plus the API Keys page for synonym_sets actions. Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
