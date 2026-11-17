---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.cluster-health-api-status
name: cluster-health-api-status
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, cluster-health-api-status, es-cluster-health]
level: practitioner
status: docs-checked
description: "Interpret green, yellow and red status with _cluster/health, _cat/shards and _cat/indices to find the affected indices."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-health.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-shards.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-nodes.html
  - https://docs.opensearch.org/latest/api-reference/cluster-api/cluster-health/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Read cluster health and cat APIs

**Goal:** quickly localise the problem.
- `GET _cluster/health?level=indices` adds per-index health (OpenSearch documents `level` values `cluster`, `indices`, `shards` and `awareness_attributes`); `wait_for_status=yellow&timeout=30s` waits until the cluster reaches that status or better, for scripts.
- Red: one or more primary shards unassigned, so some data is unavailable (can happen briefly at startup). Yellow: all primaries assigned, one or more replicas unassigned. Green: all shards assigned. Index status is the worst of its shards; cluster status the worst of its indices.
- `GET _cat/shards?v&h=index,shard,prirep,state,unassigned.reason&s=state`. `unassigned.reason` is the reason for the last state change, not why the shard is unassigned now; use the cluster allocation explain API for that.
- `GET _cat/nodes?v&h=name,node.role,heap.percent,cpu,load_1m,disk.used_percent` (`role` is an alias of `node.role`).
- Failure mode: treating yellow on a single-node cluster as a fault; a primary and its replica are never allocated to the same node, so replicas stay unassigned.

## Verify
- [ ] The list of non-STARTED shards is empty after the fix.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.

## Checked
2026-11-08. Read the Elasticsearch cluster health, cat shards, cat nodes and shard allocation settings pages and the OpenSearch cluster health page: status definitions, `level`, `wait_for_status`, cat column names, the `unassigned.reason` caveat and the same-node rule. Added the `unassigned.reason` caveat and `node.role` column name.
Method: documentation only; no commands were run.
