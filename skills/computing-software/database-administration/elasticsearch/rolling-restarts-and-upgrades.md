---
id: computing-software.database-administration.elasticsearch.rolling-restarts-and-upgrades
name: rolling-restarts-and-upgrades
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, rolling-upgrade-elasticsearch, rolling-restart, cluster-routing-allocation-enable, synced-flush, upgrade-assistant, node-shutdown-api, version-compatibility]
level: practitioner
status: docs-checked
description: "Restart or upgrade an Elasticsearch cluster node by node without downtime: allocation settings, node shutdown API, order of nodes, and checks between nodes."
sources:
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/upgrade/deployment-or-cluster/elasticsearch.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/upgrade/prepare-to-upgrade.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md
  - https://github.com/elastic/elasticsearch-specification/blob/main/specification/shutdown/put_node/ShutdownPutNodeRequest.ts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rolling restarts and upgrades

**Goal:** patch, reconfigure or upgrade every node with the cluster serving traffic throughout.

## Before an upgrade
- Supported path: rolling upgrades within a major, and from the last minor of the previous major to the next (the docs example is 8.19.x to the current 9.x). Check the upgrade docs for the exact path for your versions. Downgrades are not supported; a mixed-version cluster is only valid during the rolling upgrade.
- Use the Kibana Upgrade Assistant and fix critical deprecation items; verify plugin compatibility.
- Take a snapshot (the only way back if you cannot finish the upgrade).
- Cluster green.

## Per node
1. Stop shards from being reallocated while the node is down:
   ```json
   PUT _cluster/settings
   { "persistent": { "cluster.routing.allocation.enable": "primaries" } }
   ```
   (The node shutdown API is designed for indirect use by Elastic Cloud, ECE and ECK; direct use is not supported, so use the allocation setting for self-managed restarts.)
2. Optionally `POST _flush` to speed shard recovery.
3. Stop the node, upgrade the package/config, start it.
4. Wait for it to join: `GET _cat/nodes`.
5. Re-enable allocation: `"cluster.routing.allocation.enable": null`.
6. Wait for green (or yellow → green): `GET _cluster/health?wait_for_status=green&timeout=30m`, `GET _cat/recovery?active_only=true`.
7. Next node.

## Order
Upgrade one node at a time in this order: data tiers (`data_frozen`, `data_cold`, `data_warm`, `data_hot`; then other data nodes), then all remaining nodes that are neither master-eligible nor data, and the `master`/`voting_only` master-eligible nodes last. Upgrading a node out of order can cause errors such as `cannot allocate replica shard to a node with version [x] since this is older than the primary version [y]` until every node is upgraded.

## Gotchas
- Leaving `allocation.enable: primaries` set after finishing leaves replicas unassigned: always reset.
- Delayed allocation (`index.unassigned.node_left.delayed_timeout`, default 1m) is a backstop for unplanned restarts; extend it for slow restarts.
- Leave `cluster.initial_master_nodes` unset during a rolling upgrade.
- Upgrade every installed plugin (with `elasticsearch-plugin`) before starting the upgraded node; the upgrade docs link to the Kibana upgrade as the next step.
- During a full-cluster restart, the restart procedure also suggests stopping indexing and (for ML) enabling upgrade mode.

## Verify
After each node: health green, node version as expected in `_cat/nodes?h=name,version`.

## Checked

Checked 2026-10-25 against elastic/docs-content `main` (Stack 9.x docs) and the elasticsearch-specification. Confirmed: upgrade order by node role, out-of-order replica allocation error text, no downgrades and snapshot as the way back, unset `cluster.initial_master_nodes`, plugin upgrade, `cluster.routing.allocation.enable` primaries/null and flush steps, 1 minute default delayed timeout, node shutdown API direct use is unsupported. Removed the 7.15+ node shutdown recommendation, the `_migration/deprecations` call, the 7.17 and 8.18 path examples and the allocation delay example. The `wait_for_status` timeout value is an example.

Method: documentation only; no commands were run.
