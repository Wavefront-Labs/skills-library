---
id: computing-software.database-administration.elasticsearch.cross-cluster-replication
name: cross-cluster-replication
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, ilm, snapshot, cross-cluster-replication, ccr, follower-index, auto-follow, remote-cluster, disaster-recovery, leader-index]
level: advanced
status: docs-checked
description: "Replicate Elasticsearch indices to a second cluster with CCR: remote cluster connection, follower and auto-follow patterns, monitoring lag, and promoting followers for DR."
sources:
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/tools/cross-cluster-replication.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/tools/cross-cluster-replication/ccr-getting-started-prerequisites.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/tools/cross-cluster-replication/ccr-getting-started-auto-follow.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/remote-clusters/remote-clusters-api-key.md
  - https://github.com/elastic/elasticsearch-specification/blob/main/specification/ccr/unfollow/UnfollowIndexRequest.ts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-cluster replication

**Goal:** a DR or regional read cluster that follows production indices with
seconds of lag, and a tested promotion procedure.

CCR needs a licence that supports it, the same licence type on both clusters (a 30-day trial works). OpenSearch has its own
cross-cluster replication plugin with different APIs.

## 1. Connect the follower cluster to the leader
On the **follower** cluster:
```json
PUT _cluster/settings
{ "persistent": { "cluster": { "remote": { "prod": {
    "mode": "proxy", "proxy_address": "prod-es.example.com:9443" } } } } }
```
(`sniff` mode with `seeds` when nodes are directly reachable.) API-key based
remote cluster security connects to the remote cluster port, default 9443; certificate-based trust uses the transport port.
Use an address that includes that port.
Check: `GET _remote/info` shows `connected: true`.

## 2. Follow indices
```json
PUT /orders-follower/_ccr/follow
{ "remote_cluster": "prod", "leader_index": "orders" }

PUT _ccr/auto_follow/logs
{ "remote_cluster": "prod", "leader_index_patterns": ["logs-*"],
  "follow_index_pattern": "{{leader_index}}" }
```
Followers are read-only. Leader indices need soft deletes (default since 7.0).
Auto-follow only applies to indices created on the remote cluster **after** the pattern exists;
follow existing ones explicitly.

## Monitor
```json
GET /orders-follower/_ccr/stats      // leader vs follower global checkpoint = lag in operations
GET _ccr/stats                        // auto-follow failures
```
Alert on growing checkpoint difference and `read_exceptions`.

## Promote for DR
```json
POST /orders-follower/_ccr/pause_follow
POST /orders-follower/_close
POST /orders-follower/_ccr/unfollow
POST /orders-follower/_open
```
Now writable; point writers at it (aliases help). Failing back requires setting up
following in the other direction and re-syncing: there is no automatic reverse.

## Gotchas
- The leader keeps operation history using soft deletes and a retention lease (`index.soft_deletes.retention_lease.period` is the maximum time to retain it); if the follower is paused or disconnected longer than that, the lease expires and the follower must be re-created.
- Mappings and settings changes replicate. ILM and SLM policy definitions do not: CCR copies the `index.lifecycle.name` setting but you must define the policy on the follower cluster.
- Deleting a leader index does not delete the follower.
- Searchable snapshot indices are not fully replicated; configure snapshot repositories on the follower cluster instead.

## Verify
`_ccr/stats` shows lag near zero under load; a DR drill promotes a follower and
an app writes to it successfully.

## Checked

Checked 2026-10-25 against elastic/docs-content `main` (Stack 9.x) and the elasticsearch-specification. Confirmed: same licence type needed on both clusters; remote cluster port default 9443 for API-key security; soft deletes required and on by default since 7.0; retention lease behaviour; auto-follow only for indices created after the pattern; ILM policies are not replicated (only the `index.lifecycle.name` setting); the unfollow API requires the follower to be paused and closed first. The exact `_ccr/stats` field names were not checked and the alert advice is generic guidance.

Method: documentation only; no commands were run.
