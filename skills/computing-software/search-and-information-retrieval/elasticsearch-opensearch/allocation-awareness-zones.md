---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.allocation-awareness-zones
name: allocation-awareness-zones
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, allocation-awareness-zones, es-allocation]
level: advanced
status: docs-checked
description: "Spread copies across zones or racks with node attributes and cluster.routing.allocation.awareness settings."
sources:
  - https://www.elastic.co/docs/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/shard-allocation-awareness
  - https://docs.opensearch.org/latest/install-and-configure/configuring-opensearch/cluster-settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Allocation awareness and forced awareness

**Goal:** survive losing a zone.
- Node attribute in the node config file: `node.attr.zone: zone-a` (or `-Enode.attr.zone=zone-a` at startup).
- `PUT _cluster/settings {"persistent":{"cluster.routing.allocation.awareness.attributes":"zone"}}`. Several attributes can be given as a comma-separated list; each is considered separately.
- Forced awareness: `cluster.routing.allocation.awareness.force.zone.values: zone-a,zone-b`. Without it, if one location fails the shards spread across the remaining locations; with it, Elasticsearch prefers to leave replicas unassigned rather than overload the surviving nodes. List all possible attribute values.
- Failure mode: if the number of nodes per location is unbalanced and there are many replicas, replicas can be left unassigned.
- On Elastic Cloud Hosted and Enterprise you cannot set custom node attributes, so this applies to self-managed (and ECK) clusters.

## Verify
- [ ] `GET _cat/shards?v&h=index,shard,prirep,node` shows each primary and its replica on nodes in different zones (match node names to their `zone` attribute).

## Checked
Date: 2026-11-07
- Elasticsearch shard allocation awareness page, read in full: `node.attr.rack_id`, `-E` startup form, `PUT /_cluster/settings` persistent `cluster.routing.allocation.awareness.attributes`, comma-separated attributes, forced awareness `awareness.force.zone.values` example, unassigned replicas on unbalanced locations, Elastic Cloud limitation.
- OpenSearch cluster settings page: searched for the awareness rows, found `cluster.routing.allocation.awareness.attributes` and `cluster.routing.allocation.awareness.force.<attribute>.values` (both Dynamic, list). The page was searched, not read in full; the forced-awareness explanation above is from the Elasticsearch page.
- Removed: "Replicas must be enough for zones to hold a copy" (not stated on either page). Verify step reworded because `_cat/shards` shows node names, not zones.
Method: documentation only; no commands were run.
