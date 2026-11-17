---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.red-yellow-triage-runbook
name: red-yellow-triage-runbook
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, red-yellow-triage-runbook]
level: advanced
status: docs-checked
description: "Follow an ordered runbook for red or yellow clusters: nodes, disk, settings, allocation, then recovery."
sources:
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-allocation-explain
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-allocation
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-recovery
  - https://www.elastic.co/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings
  - https://docs.opensearch.org/latest/api-reference/cluster-api/cluster-allocation/
  - https://docs.opensearch.org/latest/api-reference/cat/cat-recovery/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Red and yellow cluster triage

**Goal:** a repeatable checklist. Status meanings (cluster health API): green means all shards are assigned; yellow means all primaries are assigned but one or more replicas are not; red means one or more primary shards are unassigned and some data is unavailable (this can occur briefly during startup).
- 1) `GET _cluster/health` for the status and unassigned counts, then `GET _cat/nodes` to see whether a node left. 2) `GET _cat/allocation` for shards and disk space per data node.
- 3) `GET _cluster/settings` and check `cluster.routing.allocation.enable`. Its values are `all` (default), `primaries`, `new_primaries` and `none`. It affects only future allocations and does not re-allocate or un-allocate shards already placed; a restarted node holding an unassigned primary copy with a matching allocation id recovers it immediately.
- 4) `GET _cluster/allocation/explain` (optionally with `index`, `shard`, `primary` and `current_node`) explains why a shard is unassigned or stays where it is. OpenSearch's version also accepts `include_yes_decisions` and `include_disk_info`.
- 5) `GET _cat/recovery?active_only=true&v` lists ongoing shard recoveries.
- If allocation was disabled for a restart, set `cluster.routing.allocation.enable` back to `all` through the cluster settings API once the node is back.

## Verify
- [ ] Health returns green and `_cat/recovery?active_only=true` has nothing active.

## Checked

2026-11-08. Confirmed against the Elasticsearch cluster health, allocation explain, cat allocation, cat recovery and cluster-level shard allocation settings pages, and the OpenSearch cluster allocation explain and cat recovery pages. Removed the `indices.recovery.max_bytes_per_sec` tuning advice, the null reset form of the setting, and the warning about force-allocating primaries, which none of those pages state.
Method: documentation only; no commands were run.
