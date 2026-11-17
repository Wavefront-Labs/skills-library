---
id: computing-software.search-and-information-retrieval.apache-solr.collection-create-api
name: collection-create-api
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [collections-api, create-collection, numshards, replicationfactor, reload-collection]
level: practitioner
status: docs-checked
description: "Create and manage SolrCloud collections with the Collections API: CREATE parameters, numShards, replicationFactor, replica types, createNodeSet, MODIFYCOLLECTION, RELOAD, DELETE."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/collection-management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# collection-create-api

`/admin/collections?action=CREATE&name=<name>&collection.configName=<configset>&numShards=1` (v2: `POST /api/collections`).

CREATE parameters:
- `router.name`: `compositeId` (default; needs `numShards`) or `implicit` (name `shards`; `router.field` picks the shard).
- `replicationFactor` (default 1, NRT replicas), or explicit `nrtReplicas`, `tlogReplicas`, `pullReplicas`. A PULL replica cannot be leader and should not be the only type.
- `createNodeSet` (v2 `nodeSet`; value `EMPTY` defers replica creation), `createNodeSet.shuffle`.
- `collection.configName` (v2 `config`), `property.name=value` (expert), `waitForFinalState`, `async`.

Other actions: `RELOAD` (apply config changes), `MODIFYCOLLECTION` (change attributes; raising `replicationFactor` only permits more ADDREPLICA calls, it adds none), `LIST`, `DELETE` (v2: `DELETE /api/collections/<name>`).

Add `async=<id>` to long actions, then poll request status.

## Checked

2026-11-04. Confirmed against the Collection Management page: CREATE parameters, router names, replica types, `createNodeSet` and `EMPTY`, v2 `DELETE /api/collections/<name>`, `async`. Removed a generic closing sentence.

Method: documentation only; no commands were run.
