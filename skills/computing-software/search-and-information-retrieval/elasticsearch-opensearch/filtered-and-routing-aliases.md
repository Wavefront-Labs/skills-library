---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.filtered-and-routing-aliases
name: filtered-and-routing-aliases
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, filtered-and-routing-aliases]
level: advanced
status: docs-checked
description: "Create aliases with a filter or routing value to expose a subset of an index, such as per-tenant views."
sources:
  - https://www.elastic.co/docs/manage-data/data-store/aliases
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filtered and routing aliases

**Goal:** cheap logical views.
- `{"add":{"index":"orders","alias":"orders-acme","filter":{"term":{"tenant":"acme"}},"routing":"acme"}}`.
- The `filter` is Query DSL and limits the documents the alias can access in searches.
- Filters apply only to Query DSL searches, not to retrieving a document by ID, so an alias filter is not a security boundary on its own; combine with document-level security for real isolation.
- `routing` sends the alias's requests to a specific shard, which can let searches use the shard request cache. `index_routing` and `search_routing` override `routing` for indexing and searching respectively.
- Data stream aliases do not support routing options.
- Writes through an alias that points to several targets are rejected unless one has `is_write_index: true`; an alias to a single index writes to it automatically (not so for data stream aliases).

## Verify
- [ ] Search via the alias returns only the tenant's documents.

## Checked
Date: 2026-11-08
Method: Read the Elasticsearch aliases page in full; OpenSearch was not checked.
