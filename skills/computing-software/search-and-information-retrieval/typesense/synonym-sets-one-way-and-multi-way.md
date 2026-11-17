---
id: computing-software.search-and-information-retrieval.typesense.synonym-sets-one-way-and-multi-way
name: synonym-sets-one-way-and-multi-way
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [synonym-sets, one-way-synonym, multi-way-synonym, typesense]
level: practitioner
status: docs-checked
description: "Create Typesense v30 synonym sets with PUT /synonym_sets/:name using multi-way synonyms lists or one-way root mappings, plus locale and symbols_to_index options."
sources: ["https://typesense.org/docs/30.2/api/synonyms.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synonym sets: one-way and multi-way

`PUT /synonym_sets/:synonymSetName` creates or updates a set. Body: `{"items": [ ... ]}`.

## Multi-way

Every word is equivalent to the others: `{"id": "coat-synonyms", "synonyms": ["blazer", "coat", "jacket"]}` in set `clothing-synonyms`. A search for `coat` also returns documents containing `blazer` or `jacket`.

## One-way

Add a `root`: `{"id": "smart-phone-synonyms", "root": "smart phone", "synonyms": ["iphone", "android"]}` in `tech-synonyms`. Searching `smart phone` matches documents with `iphone` or `android` or both, but not the other direction.

## Item arguments

- `items.id` (required): unique id of the item.
- `items.synonyms` (required): array of equivalent words.
- `items.root`: root word for 1-way synonyms.
- `items.locale`: if set, the synonym applies only when the most weighted searched field has a matching locale; unset means global. Useful when a word means different things per language.
- `items.symbols_to_index`: special characters are dropped from synonyms by default; list the ones to keep as is.

The response echoes `{"name": ..., "items": [...]}`. After creating a set, link it to a collection (see the linking skill).

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Synonym Sets page (https://typesense.org/docs/30.2/api/synonyms.html) and its source markdown, plus the API Keys page for synonym_sets actions. Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
