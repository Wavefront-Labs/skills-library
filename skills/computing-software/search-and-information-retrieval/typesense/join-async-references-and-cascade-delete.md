---
id: computing-software.search-and-information-retrieval.typesense.join-async-references-and-cascade-delete
name: join-async-references-and-cascade-delete
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [async-reference, cascade-delete, reference-aliases, typesense]
level: advanced
status: docs-checked
description: "Index Typesense documents before their references exist with async_reference; object references, aliases in references and cascade_delete."
sources: ["https://typesense.org/docs/30.2/api/joins.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async references, object references, aliases, cascade

## async_reference

Set `"reference": "products.product_id"`, `"optional": true`, `"async_reference": true` on a field to index a document even when the referenced one does not exist yet; otherwise you get `Reference document having '...' not found in the collection '...'.` References resolve automatically when the referenced documents arrive, which helps with indexing in a different order from dependencies.

## References inside objects

For an `object` field `order`, declare `{"name": "order.product_id", "type": "string", "reference": "products.id"}`. For an `object[]` field `orders`, the reference field must be an array: `{"name": "orders.product_id", "type": "string[]", "reference": "products.id"}`.

## Aliases

An alias can be used in a reference definition. But documents store internal sequential IDs of the referenced documents, assigned in indexing order. If you switch any collection of the join group through an alias update, reindex all the related collections together so the IDs stay in sync.

## Cascade delete

By default a document is cascade deleted when all of its referenced documents get deleted. Declare `cascade_delete: false` on the reference field to change that; this requires `async_reference: true` too.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page JOINs (names, defaults, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
