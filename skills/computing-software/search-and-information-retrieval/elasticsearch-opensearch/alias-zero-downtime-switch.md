---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.alias-zero-downtime-switch
name: alias-zero-downtime-switch
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, alias-zero-downtime-switch, es-aliases]
level: practitioner
status: docs-checked
description: "Point clients at an alias and atomically swap the index behind it using the _aliases actions API."
sources:
  - https://www.elastic.co/docs/manage-data/data-store/aliases
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-update-aliases
  - https://docs.opensearch.org/latest/im-plugin/index-alias/
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-aliases
  - https://docs.opensearch.org/latest/api-reference/cat/cat-aliases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zero-downtime reindex with an alias

**Goal:** change index structure without client changes.
```
POST _aliases
{"actions":[{"remove":{"index":"products-v1","alias":"products"}},{"add":{"index":"products-v2","alias":"products"}}]}
```
- All actions in one request are applied atomically: the alias has no downtime and never points to both indices at once (Elasticsearch aliases page); OpenSearch likewise states alias changes are atomic.
- Applications read and write `products`; versioned indices stay behind it.
- Check: `GET _alias/products`, `GET _cat/aliases?v`.
- Rollback is the reverse swap.
- Failure mode: an alias pointing to several indices rejects writes unless one index has `is_write_index: true`.
- If one action in a multi-action request fails, Elasticsearch can return HTTP 200 with `errors: true` and per-action `action_results`; set `must_exist` to `true` on `remove` so the whole list fails together.

## Verify
- [ ] Queries against the alias return results from the new index only.

## Checked
Date: 2026-11-07
- Elasticsearch aliases page, read in full: atomic multiple actions, remove-then-add swap example, `GET _alias/logs`, `is_write_index` and the rejects-writes rule, `must_exist` and `action_results`.
- Elasticsearch update-aliases API page, read in full: `POST /_aliases`, `must_exist` default false, `errors` and `action_results` response fields.
- OpenSearch alias guide: read the atomic-change statement, the combined remove-and-add example, the write-index rejection text and the `GET /_alias/<name>` and `GET /_cat/aliases?v` rows (searched and read those sections, not every line).
- Both cat aliases pages: `GET _cat/aliases` and the `v` parameter (searched, not read in full).
- Removed: nothing factual; added the `errors`/`must_exist` note. The OpenSearch alias API reference page returned an empty stub and was not read.
Method: documentation only; no commands were run.
