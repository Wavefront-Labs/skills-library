---
id: computing-software.search-and-information-retrieval.typesense.curation-v30-migration
name: curation-v30-migration
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [overrides-migration, curations-index, v30-upgrade, typesense]
level: advanced
status: docs-checked
description: "Upgrade Typesense overrides to v30 curation sets, which are named <collection>_curations_index; snapshot before upgrading and replace overrides:* key actions."
sources: ["https://typesense.org/docs/30.2/api/curation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating overrides to curation sets

In v30 the per-collection overrides are migrated automatically to curation sets and searches continue to work, but client code must use the new API. Self-hosters should snapshot before upgrading so the Synonyms and Overrides are migrated.

## Where rules end up

Each collection's override rules go into a curation set named like the collection with a `*_curations_index` postfix, e.g. `products_curations_index`.

## Differences

1. Endpoints: `/collections/{collection}/overrides/*` becomes `/curation_sets/*`.
2. Data: direct override objects become items inside a curation set.
3. Association: via the collection's `curation_sets` field.
4. Search: sets can be named dynamically in search parameters as well as through the collection link.

## Keys

Keys granted `overrides:*` give `401 Unauthorized` against the new endpoints. Create new keys with `curation_sets:*`, then delete the old ones, as keys have no update endpoint.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Curation page (https://typesense.org/docs/30.2/api/curation.html) and its source markdown in typesense-website (placeholder rules, sort_by and filter_by examples), plus the API Keys page for curation_sets actions. Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
