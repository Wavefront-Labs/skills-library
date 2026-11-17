---
id: computing-software.database-administration.elasticsearch.cross-cluster-search
name: cross-cluster-search
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, cross-cluster-search, remote-clusters, elasticsearch-lifecycle, ccs]
level: practitioner
status: docs-checked
description: "Search across Elasticsearch clusters with cross-cluster search: configure remote clusters (API key or cert based), query cluster:index patterns, and tune minimize_roundtrips."
sources:
  - https://github.com/elastic/docs-content/blob/main/explore-analyze/cross-cluster-search.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/remote-clusters/remote-clusters-api-key.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/remote-clusters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-cluster search (CCS)

**Goal:** one query over regional or per-team clusters without copying data.

## Connect a remote cluster (8.x)
API-key based security: the remote cluster exposes the remote cluster server port (default 9443); the local cluster stores a cross-cluster API key.
```json
# on the remote cluster
POST _security/cross_cluster/api_key
{ "name": "ccs-from-central", "access": { "search": [ { "names": ["logs-*"] } ] } }

# on the local cluster: add the key to the keystore, then
PUT _cluster/settings
{ "persistent": { "cluster.remote.eu.seeds": ["eu-es-1:9443"] } }
```
`bin/elasticsearch-keystore add cluster.remote.eu.credentials` (reload with `POST _nodes/reload_secure_settings`). Certificate-based (legacy) uses transport port 9300 and trust between clusters.

Check: `GET _remote/info` shows `connected: true`.

## Query
```json
GET logs-*,eu:logs-*,us:logs-*/_search
{ "query": { "range": { "@timestamp": { "gte": "now-15m" } } }, "aggs": { "by_cluster": { "terms": { "field": "_index" } } } }
```
Patterns like `*:logs-*` hit every remote. `skip_unavailable` defaults to `true`, so a down remote gives partial results if a remote is down; the response `_clusters` section reports status per cluster.

## Performance knobs
- `ccs_minimize_roundtrips`: synchronous searches default to `true` (each remote runs the whole search and returns its top hits, fewer WAN round trips); async searches default to `false`. Scroll and inner hits are better with `false`, and approximate kNN always uses `false`.
- Version compatibility: a local cluster can search remotes on the previous minor, any newer minor in the same major, and (from the last minor of a major) any minor of the next major; see the compatibility table in the CCS docs. Keeping clusters within one minor lets any cluster act as the local one.
- Kibana data views with `cluster:index` patterns work with CCS.

## Security
Local user role must allow the remote indices (`remote_indices` in role descriptors for API-key model); remote enforces the API key's access.

## Verify
Response `_clusters.successful` equals the number of targeted clusters; latency from the furthest region within budget.

## Checked

Checked 2026-10-25 against elastic/docs-content `main` (Stack 9.x). Confirmed: remote cluster port default 9443; `POST _security/cross_cluster/api_key` and `remote_indices` in role descriptors; `skip_unavailable` default true; `ccs_minimize_roundtrips` defaults (sync true, async false); version support rules. The 8.10 introduction version and the 8.15 default-change version were not confirmed and were removed.

Method: documentation only; no commands were run.
