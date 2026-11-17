---
id: computing-software.search-and-information-retrieval.meilisearch.design-primary-keys
name: design-primary-keys
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [primary-key, document-id, index-creation, meilisearch]
level: practitioner
status: docs-checked
description: "Choose and set a Meilisearch primary key: auto-detection of attributes ending in id, allowed types, stability, anti-patterns and how to change it."
sources:
  - https://www.meilisearch.com/docs/capabilities/indexing/how_to/design_primary_keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Design primary keys

Every document needs a unique primary key; it drives updates and deduplication.

## Selection

On a new index Meilisearch looks for one attribute ending in `id` (case-insensitive). Exactly one is used; none or several is an error, so set it explicitly when you have `id`, `product_id`, `user_id` together. Set it at creation (`POST /indexes` with `{"uid": "products", "primaryKey": "product_id"}`) or with `?primaryKey=product_id` on the documents call.

## Allowed values

Integers, or strings of a-z, A-Z, 0-9, hyphen and underscore (UUIDs fine). Floats, booleans and null are invalid.

## Good practice

- Reuse the source database ID, so PUT updates merge cleanly.
- Sequential integers are compact but need a central generator; UUIDs need no coordination but are long; composite strings like `category-123` must be unique across categories.

## Anti-patterns

- Non-unique values: the later document overwrites the earlier one.
- Mutable fields such as slug or URL: a changed value is treated as a new document. Keep a stable `id` and a separate `slug`.

## Changing it

Impossible in place. Export the data, delete the index, recreate it with the new `primaryKey`, re-import.

## Checked

Method: 2026-11-09 docs-only read of the cited page in full. All claims match the page; unchanged.
