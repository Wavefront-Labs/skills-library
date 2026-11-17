---
id: computing-software.search-and-information-retrieval.apache-solr.distributed-search-tolerance
name: distributed-search-tolerance
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [distributed-requests, distributed-search, shards-tolerant, shards-preference, partial-results, singlepass]
level: advanced
status: docs-checked
description: "Control SolrCloud distributed queries: shards.tolerant, requireZkConnected, partialResults, shards.info, distrib.singlePass, shards, and shards.preference."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/solrcloud-distributed-requests.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# distributed-search-tolerance

`shards.tolerant` (default false): if a shard cannot answer, the request fails. With `true`, partial results may be returned and the response header sets `partialResults`. With `requireZkConnected`, the request fails if the serving node cannot reach ZooKeeper, avoiding stale or wrong results; it also fails when queried shards are unavailable, like false. Add `shards.info` for per-shard detail.

`distrib.singlePass=true` fetches all requested stored fields in the first phase. It can be slower when large or many fields are requested.

`shards=shard1,shard2` (or replica URLs) restricts the query. It is required for user-managed clusters but optional in SolrCloud, where `_route_` is the usual way.

`shards.preference=property:value` orders replicas within each shard. Properties:
- `replica.type`: preferred types.
- `replica.location`: `local`, a `host`, or a URL prefix `http://hostname:port`. The benefit of `local` shrinks as more shards lack a local replica; `host` may then work better.

Without SolrJ, `shards.preference` is not supported for single-shard collections.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Distributed Requests page: `shards.tolerant` (default false, true, requireZkConnected), `partialResults`, `shards.info`, `distrib.singlePass` trade-off, `shards` requirement in user-managed clusters, `shards.preference` with `replica.type` and `replica.location` (local, host, URL prefix), and the SolrJ single-shard limit. Removed `replica.leader`, which the page does not list.

Method: documentation only; no commands were run.
