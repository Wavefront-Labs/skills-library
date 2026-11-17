---
id: computing-software.database-administration.elasticsearch.discovery-and-cluster-formation
name: discovery-and-cluster-formation
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, opensearch, elasticsearch-yml, elasticsearch-setup, discovery-seed-hosts, cluster-initial-master-nodes, master-eligible, voting-configuration, cluster-bootstrap, split-brain]
level: advanced
status: docs-checked
description: "Form an Elasticsearch 7+/8 cluster correctly: discovery.seed_hosts, one-time cluster.initial_master_nodes bootstrap, three master-eligible nodes, and voting exclusions."
sources:
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/distributed-architecture/discovery-cluster-formation/modules-discovery-bootstrap-cluster.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/distributed-architecture/discovery-cluster-formation/modules-discovery-voting.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/distributed-architecture/discovery-cluster-formation/modules-discovery-quorums.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/command-line-tools/node-tool.md
  - https://github.com/elastic/elasticsearch-specification/blob/main/specification/cluster/post_voting_config_exclusions/ClusterPostVotingConfigExclusionsRequest.ts
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Discovery and cluster formation

**Goal:** nodes find each other, exactly one cluster forms, and master elections
survive losing a node.

## elasticsearch.yml essentials
```yaml
cluster.name: prod-logs
node.name: es-m1
node.roles: [ master ]                       # dedicated master on larger clusters
network.host: 10.0.1.11
discovery.seed_hosts: [ "10.0.1.11", "10.0.1.12", "10.0.1.13" ]   # or DNS names
cluster.initial_master_nodes: [ "es-m1", "es-m2", "es-m3" ]       # node.name values, FIRST START ONLY
```
- `discovery.seed_hosts`: where to look for master-eligible nodes, on every node.
- `cluster.initial_master_nodes`: used **only** when bootstrapping a brand-new
  cluster. Remove it from config after the cluster forms. Leaving it, or setting
  it on nodes joining an existing cluster, can bootstrap a second, separate
  cluster with the same name (data loss risk when nodes later meet).
Since 7.0 there is no `minimum_master_nodes`; the cluster manages a voting
configuration automatically (quorum = majority of voting masters).

## Master-eligible count
High availability needs at least **3** master-eligible nodes, at least two of which are not voting-only; with three the cluster tolerates losing one. Two master-eligible nodes cannot tolerate losing one (no majority). Dedicated masters (`node.roles: [master]`) keep elections stable under data-node load. A
`voting_only` node can be the third master-eligible node but cannot be elected master.

## Removing master nodes safely
You must not stop half or more of the nodes in the voting configuration at the same time. By default the voting configuration shrinks automatically when you remove fewer than half of the master-eligible nodes (with more than three), so use voting exclusions to remove half or more at once or to go below three. Exclude
them from voting first:
```bash
curl -X POST "localhost:9200/_cluster/voting_config_exclusions?node_names=es-m3"
# shut down es-m3, then clear when done:
curl -X DELETE "localhost:9200/_cluster/voting_config_exclusions"
```

## Troubleshooting
- Log `master not discovered yet, this node has not previously joined a bootstrapped (v7+) cluster`
  → initial_master_nodes missing or its entries don't exactly match `node.name` (an FQDN versus bare hostname mismatch is a common cause).
- If you meant to join an existing cluster but a node bootstrapped itself, clusters never merge: wipe that node's data, set `discovery.seed_hosts` and make sure `cluster.initial_master_nodes` is unset.
- `elasticsearch-node unsafe-bootstrap` forces a node to form a brand-new cluster from its local metadata; it is a last resort and can lose data.

## Verify
```bash
curl -s "localhost:9200/_cat/nodes?v&h=name,node.role,master"
curl -s localhost:9200/_cluster/state?filter_path=metadata.cluster_coordination.last_committed_config
```
One master marked `*`, and the voting config lists your master-eligible nodes.

## Checked

Checked 2026-10-25 against elastic/docs-content and elastic/elasticsearch `main` (Stack 9.x docs). Confirmed: `cluster.initial_master_nodes` only for first bootstrap and must match `node.name` exactly; remove it after formation; log message wording; at least three master-eligible nodes (two not voting-only) for HA; do not stop half or more of the voting nodes; voting exclusions API (by node names or ids, shrink rules); `elasticsearch-node unsafe-bootstrap` description. Removed the unconfirmed "5 for very large clusters", "10 data nodes" and second log message claims. The `_cluster/state` filter_path in Verify was not checked.

Method: documentation only; no commands were run.
