---
id: computing-software.search-and-information-retrieval.typesense.join-one-to-many-and-many-to-many
name: join-one-to-many-and-many-to-many
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [one-to-many, many-to-many, join-filter, typesense]
level: advanced
status: docs-checked
description: "Model Typesense one-to-many and many-to-many relations with reference fields and filter joined collections using $collection(condition)."
sources: ["https://typesense.org/docs/30.2/api/joins.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# One-to-many and many-to-many

## One-to-many

`orders` references `customers` with `{"name": "customer_id", "type": "string", "reference": "customers.id"}`. Search `customers` and filter by their orders: `"filter_by": "$orders(customer_id:=customer_a)"` or `"$orders(total_price:<100)"`. By default all `orders` fields are included; restrict with `"include_fields": "$orders(total_price)"`.

Personalised pricing works the same: `customer_product_prices` holds `customer_id`, `custom_price` and a `product_id` reference to `products.product_id`; search `products` with `$customer_product_prices(customer_id:=customer_a && custom_price:<100)`.

## Many-to-many

Use a link collection: `documents`, `users`, and `user_doc_access` with `user_id` referencing `users.id` and `document_id` referencing `documents.id`. Documents accessible to a user: search `documents` with `$user_doc_access(user_id:=user_a)`. Users that can access a document: `"filter_by": "$user_doc_access(id: *)"` with `"include_fields": "$users(id) as user_identifier"`.

When the reference field is an array type, joined documents always come back as an array; for a singular reference they come as an array only when more than one is related. Force arrays with `strategy: nest_array` in `include_fields`.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page JOINs (names, defaults, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
