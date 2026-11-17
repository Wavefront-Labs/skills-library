---
id: computing-software.search-and-information-retrieval.typesense.synonyms-v30-migration
name: synonyms-v30-migration
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [v30-migration, synonyms-index, snapshot-before-upgrade, typesense]
level: advanced
status: docs-checked
description: "Upgrade Typesense synonyms to v30: per-collection synonyms migrate to synonym sets named <collection>_synonyms_index; snapshot first and replace synonyms:* API key actions."
sources: ["https://typesense.org/docs/30.2/api/synonyms.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating synonyms to v30

On upgrade to v30 existing collection-specific synonyms are migrated automatically, and searches keep working. Self-hosters should take a snapshot before upgrading so the synonyms and overrides migrate.

## Where they go

Each collection's synonyms become a synonym set named after the collection with a `*_synonyms_index` postfix, e.g. `products_synonyms_index`.

## Differences

1. Endpoints: old `/collections/{collection}/synonyms/*`, new `/synonym_sets/*`.
2. Data: old direct synonym objects; new sets holding arrays of items.
3. Association: old per-collection; new via the collection's `synonym_sets` field.
4. Search: old always collection-bound; new sets can also be named at search time.

An old item `{"id": "coat-synonyms", "synonyms": ["blazer", "coat", "jacket"]}` becomes an entry inside `{"name": "products", "items": [...]}`.

## Action items

Client code must use the new API and client methods for reading and writing. API keys scoped to `synonyms:*` no longer work on the new routes; create keys with `synonym_sets:*` actions and delete the old ones. Benefit: sets are reusable across collections.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Synonym Sets page (https://typesense.org/docs/30.2/api/synonyms.html) and its source markdown, plus the API Keys page for synonym_sets actions. Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
