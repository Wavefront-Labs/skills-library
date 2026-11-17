---
id: computing-software.search-and-information-retrieval.typesense.curation-dynamic-sorting
name: curation-dynamic-sorting
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [dynamic-sort, sort-by-placeholder, per-store-ranking, typesense]
level: advanced
status: docs-checked
description: "Sort results by a field chosen from the query with a Typesense curation rule such as sales.{store}:desc, triggered by query text or by a filter_by match."
sources: ["https://typesense.org/docs/30.2/api/curation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic sorting in curation

Example schema: `products` with `title` string, `store` string[], object fields `sales` and `inventory` each with `sales.store01`, `sales.store02` and `inventory.store01`, `inventory.store02` as int32, and `"enable_nested_fields": true`.

## Query-triggered

```json
{"id": "dynamic-sort",
 "rule": {"query": "{store}", "match": "exact"},
 "remove_matched_tokens": true,
 "sort_by": "sales.{store}:desc, inventory.{store}:desc"}
```

A search for `store01` sorts by that store's sales descending, then by its inventory descending. The placeholder `{store}` is substituted into the `sort_by`.

## Filter-triggered

Use `rule.filter_by` in place of the query: `"rule": {"filter_by": "store:={store}", "match": "exact"}` with the same `sort_by`. The same sorting applies when the search's filter matches the store.

`rule.filter_by` must equal the request's `filter_by` string exactly (backticks, spaces, brackets included) for the rule to trigger.

Upsert via `PUT /curation_sets/curate_products` with the item inside `items`.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Curation page (https://typesense.org/docs/30.2/api/curation.html) and its source markdown in typesense-website (placeholder rules, sort_by and filter_by examples), plus the API Keys page for curation_sets actions. Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
