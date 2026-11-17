---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.rolling-upgrade-procedure
name: rolling-upgrade-procedure
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, rolling-upgrade-procedure, es-upgrades]
level: advanced
status: docs-checked
description: "Rolling upgrade of a self-managed Elasticsearch cluster: node order by role and tier, allocation, flush, upgrade, wait for green."
sources:
  - https://www.elastic.co/docs/deploy-manage/upgrade/deployment-or-cluster/elasticsearch
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rolling upgrade (Elasticsearch, self-managed)

**Goal:** upgrade one node at a time without interrupting service.

## Before you start
- Plan the upgrade and take the preparation steps, including a snapshot, per Elastic's plan and prepare guides.
- Downgrading is not supported. After one node runs the target version the cluster may make changes you cannot roll
  back, so only start if you can finish every node. If you must stop mid-upgrade, rebuild an empty cluster of the older
  version and restore from the snapshot.
- Running more than two versions in one cluster is not supported, and a mixed-version cluster is valid only during the
  upgrade. Release candidate builds are not a supported source. Only upgrade from a version released earlier than the
  target.

## Node order (one node at a time)
1. Data nodes first, tier by tier: `data_frozen`, `data_cold`, `data_warm`, `data_hot`, then other data nodes such as
   `data_content`.
2. Then nodes that are neither master-eligible nor data (ml, ingest, dedicated coordinating, transform,
   remote_cluster_client), in any order.
3. Master-eligible (`master` and `voting_only`) nodes last.
A node with several roles belongs to the first applicable group. Shard allocation errors such as "cannot allocate replica
shard to a node with version ... older than the primary version" are expected until more nodes are upgraded.

## Per node
1. Optional: stop replica allocation so the cluster does not race the one-minute
   `index.unassigned.node_left.delayed_timeout`:
```
PUT _cluster/settings
{ "persistent": { "cluster.routing.allocation.enable": "primaries" } }
```
2. Optional: pause non-essential indexing and `POST /_flush` (recovery is faster). Optionally put ML in upgrade mode
   (`POST _ml/set_upgrade_mode?enabled=true`).
3. Stop the node (for example `sudo systemctl stop elasticsearch.service`).
4. Upgrade the package. With a zip or tarball, extract to a new directory and point `ES_PATH_CONF`, `path.data` and
   `path.logs` at your external directories.
5. Merge config changes. Leave `cluster.initial_master_nodes` unset; set `discovery.seed_hosts` or
   `discovery.seed_providers`; carry JVM and logging overrides over. Upgrade all plugins with `elasticsearch-plugin`.
6. Start the node and confirm it joined (`GET _cat/nodes`).
7. Re-enable allocation:
```
PUT _cluster/settings
{ "persistent": { "cluster.routing.allocation.enable": null } }
```
8. Wait for `status: green` from `GET _cluster/health` before the next node. Watch recovery with
   `GET _cat/recovery?v=true&expand_wildcards=all&active_only=true`. If you set ML upgrade mode, turn it off with
   `enabled=false`.

## Verify
- [ ] `GET _cat/nodes?v=true&h=name,ip,role,master,version,uptime&s=uptime` shows every node on the target version and
      `GET _cluster/health` reports green.

## Checked

2026-11-08. Confirmed against Elastic's self-managed "Upgrade Elasticsearch" page (current docs). Corrected the draft's
order: it said to upgrade non-master-eligible nodes first, but the docs upgrade data nodes first by tier, then the
remaining non-master nodes, then master-eligible nodes last. Removed as unconfirmed: the OpenSearch procedure (its
rolling-upgrade page returned an empty stub and the OpenSearch source was dropped; the steps here are Elasticsearch only),
the `wait_for_status=green` health parameter, and the claim that skipping major versions is the failure mode.
Method: documentation only; no commands were run.
