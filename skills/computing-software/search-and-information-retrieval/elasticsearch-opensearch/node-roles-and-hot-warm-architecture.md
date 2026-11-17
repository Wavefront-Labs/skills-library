---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.node-roles-and-hot-warm-architecture
name: node-roles-and-hot-warm-architecture
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, node-roles-and-hot-warm-architecture]
level: advanced
status: docs-checked
description: "Assign dedicated master, data tier, ingest and coordinating-only roles in Elasticsearch and OpenSearch with node.roles, and plan a tiered topology."
sources:
  - https://www.elastic.co/docs/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_tuning-your-cluster/creating-a-cluster.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node roles and hot-warm-cold architecture

**Goal:** a topology that matches workloads. Set roles in `elasticsearch.yml` / `opensearch.yml` with `node.roles`.

## Elasticsearch
- If `node.roles` is set, the node gets only the roles listed, so list every role the cluster needs. Without it a node gets all of: master, data, data_content, data_hot, data_warm, data_cold, data_frozen, ingest, ml, remote_cluster_client, transform.
- Every cluster needs `master`, and `data_content` plus `data_hot` (or `data`).
- Dedicated master-eligible: `node.roles: [ master ]`. HA needs at least three master-eligible nodes, at least two not voting-only; then an election survives one failure. `voting_only` can be added only to nodes that also have `master`.
- Data tiers: `data_content`, `data_hot`, `data_warm`, `data_cold`, `data_frozen`; a node can belong to several tiers.
- Coordinating-only node: `node.roles: [ ]`. Every node coordinates requests anyway; this is not a role you can switch off. Too many coordinating-only nodes add load because the master must wait for cluster-state acknowledgements from every node, so weigh the benefit.
- With heavy ingest load, use dedicated ingest nodes, not ingest on master or data nodes.
- `remote_cluster_client` is needed for cross-cluster search and replication; `transform` for transforms.

## OpenSearch
- The former master node is called cluster manager. Node types in the docs: cluster manager, cluster-manager-eligible, data, ingest, coordinating, dynamic (ML), warm, search.
- By default a node is cluster-manager-eligible, data, ingest and coordinating.
- Docs examples: `node.roles: [ cluster_manager ]`, `[ data, ingest ]`, and `[]` for a dedicated coordinating node.
- Production guidance in the docs: three dedicated cluster manager nodes in three zones; keep data nodes balanced across zones (multiples of the zone count).

## Verify
- [ ] After start, each node holds exactly the roles in its config (check the node info or your monitoring), and a cluster manager/master is elected after stopping one master-eligible node.

## Checked
2026-11-08. Confirmed from the Elastic node roles page and the OpenSearch cluster creation page: Elasticsearch default roles, requirement list, master/voting_only/HA rule, tier role names, coordinating-only via empty list and its overhead, ingest advice; OpenSearch node types, defaults, example role lists, zone guidance. Removed: the `_cat/nodes` check and `warm` role string (neither page states them), and generic notes.
Method: documentation only; no commands were run.
