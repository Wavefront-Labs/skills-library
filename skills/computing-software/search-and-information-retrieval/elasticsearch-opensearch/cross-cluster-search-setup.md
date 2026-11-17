---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.cross-cluster-search-setup
name: cross-cluster-search-setup
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, cross-cluster-search-setup, es-cross-cluster]
level: advanced
status: docs-checked
description: "Register remote clusters and query them with cluster:index syntax, with skip_unavailable and security."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cross-cluster-search.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-remote-info.html
  - https://docs.opensearch.org/latest/search-plugins/cross-cluster-search/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-cluster search

**Goal:** search several clusters from one.
- `PUT _cluster/settings {"persistent":{"cluster":{"remote":{"east":{"seeds":["<host>:9300"],"skip_unavailable":true}}}}}` (the OpenSearch CCS page uses the same `cluster.remote` form with `seeds` on port 9300; its page does not cover `skip_unavailable`).
- Query with `cluster:index` names, mixing local and remote: `GET east:logs-*,logs-*/_search`.
- Status: `GET _remote/info` (needs the `monitor` cluster privilege). `connected` only says whether a connection is currently open, not whether the remote is down; Elasticsearch does not reconnect by itself, and a cross-cluster search triggers a reconnect.
- OpenSearch: users need READ or SEARCH permission on the remote indexes, and their permissions are evaluated on the remote cluster, by default combining roles propagated from the coordinating cluster with the remote cluster's own role mappings; `ccs_minimize_roundtrips=false` needs an additional index permission.
- Elasticsearch `skip_unavailable` defaults to `true`: a failing cluster is skipped and the rest return partial results. With `false`, the search fails if that cluster is unavailable, disconnects, or fails on all shards.
- Failure mode: `skip_unavailable:false` makes the whole search fail when one cluster is down.

## Verify
- [ ] `_remote/info` shows `connected: true` and the response includes a `_clusters` section summarising each cluster's search.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.

## Checked
2026-11-08. Read the Elasticsearch cross-cluster search page, the Get remote cluster information page and the OpenSearch cross-cluster search page: `seeds`, `cluster.remote`, `cluster:index` names, `skip_unavailable` default and behaviour, `_clusters` section, `connected` caveat, OpenSearch permission model. Added the default and the `connected` caveat.
Method: documentation only; no commands were run.
