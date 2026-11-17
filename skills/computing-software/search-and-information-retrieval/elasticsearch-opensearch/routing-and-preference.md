---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.routing-and-preference
name: routing-and-preference
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, routing-and-preference]
level: advanced
status: docs-checked
description: "Use routing to confine searches to a shard and preference to give consistent results and spread load."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/search-shard-routing
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/mapping-routing-field
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom routing and search preference

**Goal:** target specific shards, keep repeated searches on the same shard copies.
- Index with `POST my-index/_doc?routing=tenant-42` and search with `GET my-index/_search?routing=tenant-42` so the search runs on the shard used to index the document; several comma-separated routing values are allowed.
- Forgetting the routing value can index a document on more than one shard; set `_routing.required: true` in the mapping to require a routing value for all CRUD operations.
- By default searches use adaptive replica selection (response time, previous search time, `search` thread-pool queue size); `cluster.routing.use_adaptive_replica_selection: false` switches to round-robin.
- `?preference=_local` restricts the search to shards on the local node (falling back to adaptive replica selection if the node has no copy). A custom `preference` string (it cannot start with `_`, for example a user name or session ID) routes to the same shards in the same order as long as the cluster state and selected shards do not change; repeated searches can then hit the same shard request cache.
- Skew: `index.routing_partition_size` (set at index creation) routes to a partition of shards; a larger partition spreads data more evenly at the cost of searching more shards.

## Verify
- [ ] Repeating a search with the same `preference` string returns hits in the same order while the cluster is stable.

## Scope
The Elasticsearch reference pages were checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch reference pages Search shard routing and the `_routing` field mapping. Confirmed: all statements above. Removed: "searches without routing hit every shard", "reduces jumping scores", "skewed keys create hot shards" and the `_search_shards` check (not stated on the pages), and the OpenSearch source root.

Method: documentation only; no commands were run.
