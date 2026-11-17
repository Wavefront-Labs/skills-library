---
id: computing-software.search-and-information-retrieval.typesense.synonym-set-items-api
name: synonym-set-items-api
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [synonym-set-items, retrieve-synonym-set, delete-synonym-set, typesense]
level: practitioner
status: docs-checked
description: "Manage Typesense synonym sets and items: GET and DELETE sets, list all sets, and PUT, GET, list and DELETE single items under /synonym_sets/:name/items/:id."
sources: ["https://typesense.org/docs/30.2/api/synonyms.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synonym set and item endpoints

## Whole sets

- Retrieve: `GET /synonym_sets/:synonymSetName` returns `{"name": ..., "items": [...]}`.
- List: `GET /synonym_sets` returns an array of those objects.
- Delete: `DELETE /synonym_sets/:synonymSetName` returns `{"name": "clothing-synonyms"}`.

## Items

Change one item without resending the set:

- Upsert: `PUT /synonym_sets/:synonymSetName/items/:id`.
- Retrieve: `GET /synonym_sets/:synonymSetName/items/:id`.
- List: `GET /synonym_sets/:name/items`.
- Delete: `DELETE /synonym_sets/:synonymSetName/items/:id`.

## Keys

API keys need `synonym_sets:*` actions (`synonym_sets:list`, `get`, `create`, `delete`); item operations use the separate `synonym_sets/items:*` scope (`list`, `get`, `upsert`, `delete`). The old `synonyms:*` actions give `401 Unauthorized` on the new routes; there is no key update endpoint, so create new keys and delete the old ones.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Synonym Sets page (https://typesense.org/docs/30.2/api/synonyms.html) and its source markdown, plus the API Keys page for synonym_sets actions. Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
