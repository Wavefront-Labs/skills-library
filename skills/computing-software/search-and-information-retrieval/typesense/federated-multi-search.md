---
id: computing-software.search-and-information-retrieval.typesense.federated-multi-search
name: federated-multi-search
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [federated-search, multi-search, limit-multi-searches, typesense]
level: practitioner
status: docs-checked
description: "Batch several Typesense searches in one POST /multi_search call with common parameters, ordered per-search results, limit_multi_searches and per-search API keys."
sources: ["https://typesense.org/docs/30.2/api/federated-multi-search.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Federated multi-search

The multi-search API batches searches in one HTTP request to avoid per-request latency. Federated mode returns a separate result set per search, ideal when a UI needs distinct results from several sources, such as `products` and `brands` queried in parallel.

## Request

`POST /multi_search` with `{"searches": [{"collection": "products", "q": "shoe", "filter_by": "price:=[50..120]"}, {"collection": "brands", "q": "Nike"}]}`. Parameters shared by all searches can go in the query string, e.g. `?query_by=name`; client libraries take them as a second argument (`commonSearchParams`).

## Response

A `results` array, guaranteed to be in the same order as the `searches` you sent. Each entry has its own `found`, `hits`, `out_of`, `page`, `request_params` and `search_time_ms`.

## Extra parameters

Each individual search accepts any normal search parameter. Multi-search adds:

- `limit_multi_searches`: maximum number of search requests per call; default `50` (e.g. `20`). Best embedded in a scoped API key so it applies automatically and cannot be changed at search time.
- `x-typesense-api-key`: embed a separate search key per search, useful to apply different embedded filters per collection via scoped keys.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Multi-Search page (https://typesense.org/docs/30.2/api/federated-multi-search.html) and its source markdown (response fields, limit_multi_searches, union rules). Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
