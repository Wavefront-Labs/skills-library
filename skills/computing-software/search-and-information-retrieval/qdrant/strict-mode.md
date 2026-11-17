---
id: computing-software.search-and-information-retrieval.qdrant.strict-mode
name: strict-mode
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [strict-mode, limits, query-limit, unindexed-filtering, config-strict]
level: advanced
status: docs-checked
description: "Protect a collection from expensive requests with strict mode limits on query size, timeouts and unindexed filtering."
sources:
  - "https://qdrant.tech/documentation/ops-configuration/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Strict mode rejects requests that could overload a deployment. Set it per collection in `strict_mode_config`, or defaults in the configuration.

```http
PATCH /collections/{collection_name}
{ "strict_mode_config": {
  "enabled": true,
  "max_query_limit": 100,
  "max_timeout": 30,
  "unindexed_filtering_retrieve": false,
  "unindexed_filtering_update": false,
  "search_max_hnsw_ef": 256,
  "search_allow_exact": false,
  "search_max_oversampling": 4.0
} }
```

Keys from the docs:

- `max_query_limit` bounds `limit`.
- `max_timeout` bounds the request timeout.
- `unindexed_filtering_retrieve` and `unindexed_filtering_update`, when false, refuse filters on fields without a payload index, in searches and in filtered updates such as delete by payload.
- `search_max_hnsw_ef` bounds `hnsw_ef`.
- `search_allow_exact` controls exact search.
- `search_max_oversampling` bounds quantization oversampling.

Deployment defaults for newly created collections go in the `strict_mode` section of the configuration file (all keys default to `null`, and `enabled` to `false`). With `unindexed_filtering_retrieve` or `unindexed_filtering_update` set to false, a filter on an unindexed field is rejected; on Qdrant Cloud these settings are applied to all collections by default.

## Checked

2026-11-03. Confirmed on the Qdrant configuration page (the `strict_mode` defaults block with every key listed) and the indexing page (unindexed filtering rejected, Qdrant Cloud default). Removed the unconfirmed claims about error messages, multi-tenant suitability and gradual rollout.

Method: documentation only; no commands were run.
