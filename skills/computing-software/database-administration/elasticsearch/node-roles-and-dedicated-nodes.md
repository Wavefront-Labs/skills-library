---
id: computing-software.database-administration.elasticsearch.node-roles-and-dedicated-nodes
name: node-roles-and-dedicated-nodes
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, opensearch, elasticsearch-setup, node-roles, dedicated-master, data-tiers, coordinating-only-node, ingest-role, data-hot, data-content]
level: advanced
status: docs-checked
description: "Assign Elasticsearch node.roles (master, data tiers, ingest, ml, coordinating-only) so masters stay stable, tiers match hardware, and heavy searches don't topple data nodes."
sources:
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/configuration-reference/node-settings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node roles

**Goal:** each node does the job its hardware suits, and losing or overloading one
role does not take out the others.

## Roles (`node.roles` in elasticsearch.yml)
| Role | Does | Hardware |
|---|---|---|
| `master` | Cluster state, elections, shard allocation | Dedicated masters on larger clusters; HA needs at least 3 master-eligible nodes |
| `voting_only` (+ master) | Votes, never becomes master | Tiny tie-breaker |
| `data_content` | Non-time-series indices | Balanced |
| `data_hot` / `data_warm` / `data_cold` / `data_frozen` | Time-series tiers for ILM | Fast SSD → dense/cheap → object-store cache |
| `data` | Generic data node (all data roles) | |
| `ingest` | Ingest pipelines | CPU |
| `ml`, `transform`, `remote_cluster_client` | Feature-specific | |
| *(empty list)* `node.roles: [ ]` | **Coordinating only**: routes requests, merges results | CPU + RAM, no data |
Unset `node.roles` = the default roles (`master`, `data`, `data_content`, `data_hot`, `data_warm`, `data_cold`, `data_frozen`, `ingest`, `ml`, `remote_cluster_client`, `transform`; not `voting_only`). That suits small clusters; once a cluster has more than a handful of nodes use dedicated master-eligible nodes. If you set `node.roles`, list every role the cluster needs (at least `master` and `data_content` plus `data_hot`, or `data`).

## Example layout (~20 nodes, logs)
```yaml
# masters x3
node.roles: [ master ]
# hot x6
node.roles: [ data_hot, data_content, ingest ]
# warm x6
node.roles: [ data_warm ]
# coordinating x2 (Kibana and heavy aggregation traffic point here)
node.roles: [ ]
```

## Changing roles on an existing node
Removing the data role from a node that holds shard data can stop it starting. Drain it first with an allocation filter:
```json
PUT _cluster/settings
{ "persistent": { "cluster.routing.allocation.exclude._name": "es-d7" } }
```
wait until `GET _cat/allocation?v` shows 0 shards on it, then change roles; `elasticsearch-node repurpose` can delete leftover data that prevents startup. When repurposing to neither `data` nor `master`, starting a new node with an empty data path is simplest. Removing the master role from a voting node: use voting exclusions first.

## Gotchas
- Every node also acts as a coordinating node; too many coordinating-only nodes add load because the master waits for cluster state acknowledgements from them.
- Cross-cluster search and replication need `remote_cluster_client`; Fleet, the security app and transforms need `transform`.

## Verify
```bash
curl -s 'localhost:9200/_cat/nodes?v&h=name,node.role,heap.percent,cpu,master'
```
The roles shown per node match your plan (a `-` means coordinating only).

## Checked

Checked 2026-10-25 against elastic/docs-content and elastic/elasticsearch `main` docs (Stack 9.x). Confirmed: role names, default roles when `node.roles` is unset, `voting_only` requires `master`, empty `node.roles` makes a coordinating-only node, HA needs three master-eligible nodes (two not voting-only), repurposing guidance and `elasticsearch-node repurpose`, required roles for CCS/CCR and transforms. Removed the unconfirmed startup error text, load balancer, `_tier_preference` and watermark notes, and the `_cat/nodes` role-letter list. The OpenSearch comparison line was not checked against OpenSearch documentation (outside this lane) and was removed.

Method: documentation only; no commands were run.
