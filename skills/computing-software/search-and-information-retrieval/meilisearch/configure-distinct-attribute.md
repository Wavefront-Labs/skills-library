---
id: computing-software.search-and-information-retrieval.meilisearch.configure-distinct-attribute
name: configure-distinct-attribute
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [distinct-attribute, deduplicate-results, product-variants, meilisearch]
level: practitioner
status: docs-checked
description: "Deduplicate Meilisearch results with the distinctAttribute index setting or the distinct search parameter, for example one hit per product_id."
sources: ["https://www.meilisearch.com/docs/capabilities/full_text_search/how_to/configure_distinct_attribute"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configure a distinct attribute

A distinct attribute forces Meilisearch to return only one document per unique value of a field. The typical case is variants of one product, such as three colours of the same jacket sharing `product_id` "123456": set `distinctAttribute` to `product_id` and a search for `lee leather jacket` returns just one of them.

## Two ways

1. Index setting `distinctAttribute`: applies by default to all searches and facet retrievals of the index. Only one field is allowed; setting several returns an error.
2. Search parameter `distinct`: chosen per query and takes precedence over the setting. The field must first be in `filterableAttributes`.

## Which document wins

Among documents sharing the value, Meilisearch returns the highest ranked after applying the ranking rules; on a tie it returns the first by `internal_id`.

## Cost

Updating `distinctAttribute` re-indexes all documents. For a new index, set settings first and add documents afterwards to use less RAM than changing settings on loaded data.

## Checked

2026-11-03. Confirmed claim by claim against the Configure a distinct attribute page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
