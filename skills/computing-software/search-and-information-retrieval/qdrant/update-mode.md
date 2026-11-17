---
id: computing-software.search-and-information-retrieval.qdrant.update-mode
name: update-mode
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [update-mode, insert-only, update-only, upsert, pts-updatemode]
level: practitioner
status: docs-checked
description: "Restrict writes with update_mode: upsert, insert_only or update_only."
sources:
  - "https://qdrant.tech/documentation/manage-data/points/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

An upsert request normally inserts new points and overwrites existing ones. The `update_mode` parameter narrows that.

```http
PUT /collections/{collection_name}/points
{
  "points": [ { "id": 1, "vector": [0.9, 0.1] } ],
  "update_mode": "insert_only"
}
```

Values from the docs:

- `upsert` is the default: insert or overwrite.
- `insert_only` inserts a point only if it does not exist; if a point with that id exists, the operation is ignored.
- `update_only` modifies points that already exist and skips new ids.

The docs say `insert_only` is especially useful when migrating from one embedding model to another, where regular updates conflict with background re-embedding tasks. `update_only` is useful with conditional updates: without an explicit `update_mode`, a conditional update on a non-existent point inserts it even if the condition is not met, which is rarely intended.

## Checked

2026-11-03. Confirmed on the Qdrant points page: `upsert` default, `insert_only`, `update_only` semantics, the embedding-migration and conditional-update use cases. Removed the unconfirmed idempotence and retry claims.

Method: documentation only; no commands were run.
