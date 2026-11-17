---
id: computing-software.search-and-information-retrieval.meilisearch.federated-search
name: federated-search
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [federated-search, multi-search, federation-weight, meilisearch]
level: practitioner
status: docs-checked
description: "Merge several index queries into one ranked list with /multi-search and the federation parameter: weight, page and hitsPerPage, and federation-level distinct."
sources: ["https://www.meilisearch.com/docs/capabilities/multi_search/getting_started/federated_search"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Federated search

`POST /multi-search` runs several queries in one request. Adding a `federation` object makes the response a single merged list of hits, each carrying `_federation` with `indexUid` and `queriesPosition`. Typical case: a CRM with `profiles`, `chats` and `tickets` indexes searched at once for a person.

## Weighting

Give a query `federationOptions` with a `weight` to boost its results; for example, weighting the profiles query higher puts profile documents first.

## Pagination

Default paging uses `offset` and `limit`. For exhaustive paging set `federation.page` and `federation.hitsPerPage`; the response then has `page`, `hitsPerPage`, `totalHits` and `totalPages` instead of offset, limit and estimatedTotalHits.

## Deduplicate across indexes

`federation.distinct` (for example `"client_name"`) keeps at most one hit per value across all queries. Each participating index must have that attribute in `filterableAttributes`. Differences from index-level distinct: it spans all queries including remotes, it overrides each index's distinct attribute, and setting `distinct` on both a query and the federation returns HTTP 400. With remote instances, facet distribution is best effort, not exact.

## Checked

2026-11-03. Confirmed claim by claim against the Federated search getting-started page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
