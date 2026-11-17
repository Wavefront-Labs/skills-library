---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.replica-count-and-availability
name: replica-count-and-availability
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, replica-count-and-availability]
level: practitioner
status: docs-checked
description: "Set number_of_replicas and auto_expand_replicas to survive node loss, and know the risks of zero replicas."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/index-settings/index-modules
  - https://docs.opensearch.org/latest/api-reference/index-apis/update-settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replica count and availability

**Goal:** survive node loss.
- `PUT my-index/_settings {"index":{"number_of_replicas":1}}`: `index.number_of_replicas` is a dynamic setting, default 1 in Elasticsearch. The Elasticsearch page warns that 0 may cause temporary availability loss during node restarts, or permanent data loss on data corruption.
- OpenSearch: `PUT /{index}/_settings` updates dynamic settings at any time on an open index; `index.number_of_shards` cannot be changed after creation. The page's bulk-indexing example sets `refresh_interval` to `-1` and re-enables it afterwards, and another example sets `number_of_replicas` to 0 for several indexes. Setting a value to `null` resets it to the default. If any setting in the request cannot be updated, the whole request is rejected.
- `index.auto_expand_replicas` (Elasticsearch, default false): a dash-delimited range such as `0-5`, or `0-all`, based on the number of data nodes. Auto-expansion respects only allocation filtering rules, so other rules (such as total shards per node) can leave replicas unassigned and health yellow. With upper bound `all`, shard allocation awareness and `cluster.routing.allocation.same_shard.host` are ignored for the index.
- Failure mode: setting replicas to 0 for a bulk load and forgetting to restore it (an inference from the 0-replica warning).
- Not on the pages read: that a replica is never on its primary's node, the single-node yellow state, and the indexing-cost trade-off. Treat as background, not checked here.

## Verify
- [ ] `GET _cluster/health` shows no unassigned replicas after the change (green).

## Checked
Checked 2026-11-08 against the Elasticsearch "Index modules" page and the OpenSearch "Update Index Settings API" page. Removed: the primary/replica co-location rule, the single-node yellow claim, the read-capacity versus indexing-cost claim, and the `_cluster/health` color expectation as a documented fact.
Method: documentation only; no commands were run.
