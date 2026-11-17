---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.ilm-data-tiers-and-searchable-snapshots
name: ilm-data-tiers-and-searchable-snapshots
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, ilm-data-tiers-and-searchable-snapshots]
level: advanced
status: docs-checked
description: "Move indices across tiers with migrate actions and use searchable_snapshot in cold or frozen phases."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/index-lifecycle-actions/ilm-migrate
  - https://www.elastic.co/docs/reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ILM with data tiers and searchable snapshots

**Goal:** cheaper storage for old data.
- `migrate` moves the index to the data tier of the current phase by setting `index.routing.allocation.include._tier_preference`; ILM injects it automatically in the warm and cold phases (`enabled` defaults to `true`). It is not allowed in the hot or frozen phase. If the target tier has no nodes it falls back: warm uses `data_warm,data_hot`, cold uses `data_cold,data_warm,data_hot`.
- `searchable_snapshot` (phases hot, cold, frozen) takes a snapshot in the repository named by the required `snapshot_repository` and mounts it as a searchable snapshot; it requires data tiers. In the frozen phase it mounts a partially mounted index prefixed `partial-`. If the cold phase defines `searchable_snapshot`, `migrate` is not injected there.
- Do not put `searchable_snapshot` in both the hot and cold phases; indices may then fail to migrate to the cold tier.
- Licence level for searchable snapshots: see the Elastic subscriptions page.

## Verify
- [ ] `GET _cat/shards/my-index?v&h=index,node` shows nodes of the intended tier.

## Scope
The Elasticsearch documentation was checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch ILM migrate and searchable snapshot action references. Confirmed: all statements above. Corrected: the earlier claim that a missing target tier leaves the index on the previous tier is refined to the documented fallback order. Removed: the unconfirmed licence-tier statement and the OpenSearch source root.

Method: documentation only; no commands were run.
