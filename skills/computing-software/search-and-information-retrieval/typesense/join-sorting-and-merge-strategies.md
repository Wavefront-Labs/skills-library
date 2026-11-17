---
id: computing-software.search-and-information-retrieval.typesense.join-sorting-and-merge-strategies
name: join-sorting-and-merge-strategies
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [join-sort, merge-strategy, related-docs-count, typesense]
level: advanced
status: docs-checked
description: "Control joined output in Typesense: sort_by on joined fields, nest, merge and nest_array strategies, related_docs_count, sort_by and limit."
sources: ["https://typesense.org/docs/30.2/api/joins.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sorting and shaping joined results

## Sort by a joined field

`"sort_by": "$JoinedCollectionName( field_name:desc )"`, or with eval: `"$JoinedCollectionName( _eval(field_name:foo):desc )"`. For one-to-many joins, write `"sort_by": "$product_prices(price_net:asc)"`: prices are sorted per product and the first (lowest) value positions the product; use `desc` for the highest. Without that syntax a many-to-one join errors with `Multiple references found to sort by on product_prices.price_net`. Nested join sort: `$A( $B(field:desc))`.

## Merge strategies in include_fields

Default `strategy: nest` returns joined fields as an object under the collection name. `"$authors(*, strategy: merge)"` merges them into the main document. `strategy: nest_array` always yields an array of objects even for a single match, avoiding the object-or-array ambiguity of one-to-many joins.

## Counts, sort and limit

`"$books(*, related_docs_count: foo_related_count)"` adds a field named `foo_related_count` with the number of related docs. `"$books(*, sort_by: id: desc)"` orders the joined docs and `"$books(*, limit:5)"` caps them at 5.

## Single document

`GET /collections/books/documents/1?include_fields=$authors(name)` includes referenced fields when fetching one document (escape the `$` in shells).

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page JOINs (names, defaults, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
