---
id: computing-software.search-and-information-retrieval.typesense.left-join-and-nested-joins
name: left-join-and-nested-joins
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [left-join, nested-joins, null-join-filter, typesense]
level: advanced
status: docs-checked
description: "Do left joins in Typesense with id:* || $coll(cond), exclude matches with a negated join, and chain nested joins with filters."
sources: ["https://typesense.org/docs/30.2/api/joins.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Left joins and nested joins

## Left join

Joins are inner by default. For a left join: `"filter_by": "id:* || $join_collection_name( <join_condition> )"`. `id:*` matches all documents of the searched collection, so a document is returned as is if no reference exists, and with the referenced data if it does.

## Anti-join (null filter)

Prefix the join with `!`: `"filter_by": "!$deny_list(user_id:=u11)"` returns items not on the deny list of user `u11`. Add `"exclude_fields": "$deny_list(*)"` to keep deny list data out of the response.

## Nested joins

Syntax `$A( $B(...))`. With `products`, `product_variants` (reference `products.id`), `inventory` (references `retailers.id` and `product_variants.id`) and `retailers` (geopoint `location`):

- All inventory: `"filter_by": "$product_variants( $inventory( $retailers(id:*)))"`, `"include_fields": "$product_variants(price, $inventory(qty, $retailers(title)))"`.
- Within a radius: `$retailers(location:(48.87538726829884, 2.296113163780903,1 km))` in place of `id:*`.
- Plus price: `$product_variants(price:<100 && $inventory( $retailers(location:(...))))`.

Sorting by a nested field: `"sort_by": "$JoinedCollectionName( $NestedJoinedCollectionName(field_name:desc))"`.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page JOINs (names, defaults, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
