---
id: computing-software.search-and-information-retrieval.typesense.union-search
name: union-search
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [union-search, remove-duplicates, grouped-union, typesense]
level: advanced
status: docs-checked
description: "Merge several Typesense multi_search queries into one ranked hit list with union true: pagination, sort_by uniformity, duplicate removal and group_by rules."
sources: ["https://typesense.org/docs/30.2/api/federated-multi-search.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Union search

Set `"union": true` in a `/multi_search` body to merge the results of every query into one ordered hit set instead of one result set per query. Example: two searches on `posts` with `q: "*"`, one filtering `user_name:stark_industry`, another `user_name:rogers_steve`, sent as `POST /multi_search?page=1&per_page=2`. The response has top-level `found`, `hits`, `out_of`, `page` and `union_request_params`.

Searches can target different collections, and need not share `query_by`, `include_fields` or `exclude_fields`.

## Differences from plain multi_search

- Pagination parameters inside individual searches (`page`, `per_page`, `offset`, `limit`, `limit_hits`) are ignored; only the global ones in the query string apply.
- Sorting needs the same type, count and order of sort fields in every search. Sorting one by `user_name:asc` (string) and another by `rating:asc` (float) errors.
- Duplicates are removed by default; set `remove_duplicates: false` to keep them.

## Grouping

Supported with `group_by` and `group_limit` inside searches, but the shape must be uniform: either all searches carry grouping params or none do.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Multi-Search page (https://typesense.org/docs/30.2/api/federated-multi-search.html) and its source markdown (response fields, limit_multi_searches, union rules). Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
