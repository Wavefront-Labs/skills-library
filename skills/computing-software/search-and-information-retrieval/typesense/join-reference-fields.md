---
id: computing-software.search-and-information-retrieval.typesense.join-reference-fields
name: join-reference-fields
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [joins, reference-field, include-fields, typesense]
level: practitioner
status: docs-checked
description: "Link Typesense collections with a reference property, fetch related fields via include_fields $collection(fields), and reverse joins with id:*."
sources: ["https://typesense.org/docs/30.2/api/joins.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reference fields and basic joins

You cannot add a reference field to an existing collection via alter. Declare it at creation: `{"name": "books", "fields": [{"name": "title", "type": "string"}, {"name": "author_id", "type": "string", "reference": "authors.id"}]}`.

## Fetch related fields

`"include_fields": "$authors(first_name,last_name)"` adds an `authors` object to each hit; `$authors(*)` includes all fields.

## Reverse direction

When you search `authors` and want their books (the reference field lives in `books`), use `filter_by` to join: `"filter_by": "$books(id: *)"` with `"include_fields": "$books(*)"`. `id:*` is a special filter matching every document of that collection.

## Types

`int32`, `int64` and `string` give a one-to-one reference. Array types (`int32[]`, `int64[]`, `string[]`) allow one document to relate to zero or more others.

## Security

A reference makes the referenced collection reachable through joins. A search key limited to the referencing collection can read the referenced fields via a joined query, still without searching that collection directly.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page JOINs (names, defaults, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
