---
id: computing-software.search-and-information-retrieval.typesense.curation-set-management
name: curation-set-management
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [curation-set-api, link-curation-sets, curation-items, typesense]
level: practitioner
status: docs-checked
description: "Retrieve, list, delete and link Typesense curation sets, manage single items under /curation_sets/:name/items/:id, and the v30 curation_sets:* API key actions."
sources: ["https://typesense.org/docs/30.2/api/curation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing curation sets and items

## Sets

- `GET /curation_sets/:name` retrieve one.
- `GET /curation_sets` list all.
- `DELETE /curation_sets/:name` delete.

## Items

- `PUT /curation_sets/:name/items/:id` upsert one item.
- `GET /curation_sets/:name/items/:id` retrieve.
- `GET /curation_sets/:name/items` list.
- `DELETE /curation_sets/:name/items/:id` delete.

## Linking to a collection

At creation add `"curation_sets": ["clothing_curation", "tech_curation"]` to the collection body. For an existing one send `PATCH /collections/products` with `{"curation_sets": [...]}`.

## Item parameters

`rule.query` or `rule.filter_by` (one required), `rule.match`, `rule.tags`, `rule.synonyms`, `rule.stem`, `includes`, `excludes`, `metadata`, `filter_by`, `sort_by`, `replace_query`, `remove_matched_tokens` (default true), `filter_curated_hits` (default false), `effective_from_ts` and `effective_to_ts` (Unix timestamps for scheduled rules), `stop_processing` (default true) and `diversity`.

## Keys

The old `overrides:*` key actions return `401 Unauthorized` on the new routes; create keys with `curation_sets:*` actions (and delete the old ones, since there is no key update endpoint). `curation_sets:*` and `curation_sets/items:*` are different resource scopes: granting the first does not include the item actions (`curation_sets/items:list`, `get`, `upsert`, `delete`).

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Curation page (https://typesense.org/docs/30.2/api/curation.html) and its source markdown in typesense-website (placeholder rules, sort_by and filter_by examples), plus the API Keys page for curation_sets actions. Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
