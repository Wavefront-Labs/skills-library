---
id: computing-software.database-administration.elasticsearch.voting-config-exclusions-and-removing-master-nodes
name: voting-config-exclusions-and-removing-master-nodes
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, elasticsearch-setup, voting-config-exclusions, master-eligible, cluster-coordination, quorum]
level: advanced
status: docs-checked
description: "Remove or replace Elasticsearch master-eligible nodes without losing quorum using voting configuration exclusions, and check the current voting configuration."
sources:
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/distributed-architecture/discovery-cluster-formation/modules-discovery-voting.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/distributed-architecture/discovery-cluster-formation/modules-discovery-bootstrap-cluster.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/configuration-reference/discovery-cluster-formation-settings.md
  - https://github.com/elastic/elasticsearch-specification/blob/main/specification/cluster/post_voting_config_exclusions/ClusterPostVotingConfigExclusionsRequest.ts
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/command-line-tools/node-tool.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Voting config exclusions and removing master nodes

Elasticsearch keeps a **voting configuration**: the set of master-eligible nodes whose
votes count. Elections and cluster state updates need a majority of it. With `cluster.auto_shrink_voting_configuration` at its default (`true`) and at least three master-eligible nodes, the cluster adjusts the
configuration automatically as nodes leave, as long as all but one master-eligible node stay healthy.

## Removing master-eligible nodes safely
Removing fewer than half of the master-eligible nodes at a time (with more than three) is handled
automatically. Stopping **half or more** of the voting configuration at once (e.g. 2 of 3, or going below three nodes) can leave a voting configuration whose majority is gone: the cluster stops.

Use exclusions first:
```
POST /_cluster/voting_config_exclusions?node_names=master-old-1,master-old-2&timeout=2m
```
Use `node_names` or `node_ids` (not both). The call waits until the cluster has reconfigured its voting configuration to exclude the nodes (or the `timeout` expires). Then shut those nodes down. Afterwards, clear the list:
```
DELETE /_cluster/voting_config_exclusions?wait_for_removal=true
```
The number of exclusions is limited by `cluster.max_voting_config_exclusions` (dynamic, default 10). `wait_for_removal` on the DELETE defaults to `true`: it waits for all excluded nodes to be removed from the cluster before clearing the list.

## Inspect the current configuration
```
GET /_cluster/state?filter_path=metadata.cluster_coordination
GET /_cat/nodes?v&h=name,node.role,master
```
`last_committed_config` lists node IDs that currently vote; `voting_config_exclusions` lists exclusions.

## Replacing all masters (rolling)
1. Add the new master-eligible nodes (with `discovery.seed_hosts` pointing at the existing
   cluster; do **not** set `cluster.initial_master_nodes` on nodes joining an existing cluster).
2. Wait until they have joined (`_cat/nodes`).
3. Exclude the old masters via the API, wait.
4. Stop the old masters; clear exclusions.
5. Update `discovery.seed_hosts` on all nodes for future restarts.

## Gotchas
- `cluster.initial_master_nodes` is only for the very first bootstrap; leaving it on nodes and
  restarting them against a fresh data path can form a second, separate cluster.
- Two master-eligible nodes cannot tolerate the loss of either one; HA needs at least three master-eligible nodes, at least two of them not voting-only.
- If quorum is already lost and cannot be restored, `elasticsearch-node unsafe-bootstrap` /
  `detach-cluster` exist as last resorts with data-loss risk (see the `elasticsearch-node` docs).

## Verify
After the change, `GET _cluster/health` is green/yellow as before, `_cat/nodes` shows an
elected master among the new nodes, and `cluster_coordination.voting_config_exclusions` is empty.

## Checked

Checked 2026-10-25 against elastic/docs-content, elastic/elasticsearch and the elasticsearch-specification `main` (Stack 9.x). Confirmed: voting exclusions POST by `node_names` or `node_ids` with `timeout`, DELETE with `wait_for_removal` default true, `cluster.max_voting_config_exclusions` default 10, auto-shrink rules, HA needs three master-eligible nodes, `cluster.initial_master_nodes` guidance, `unsafe-bootstrap`/`detach-cluster`. Removed the unconfirmed "7.0+" and "odd size" claims. The `_cluster/state` filter_path and the `last_committed_config` field name in Inspect were not re-read, and `timeout=2m` is an example value.

Method: documentation only; no commands were run.
