---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.cross-cluster-replication
name: cross-cluster-replication
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, cross-cluster-replication]
level: advanced
status: docs-checked
description: "Replicate indices to a follower cluster for DR using follower indices or auto-follow patterns."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-overview.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-auto-follow.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-put-follow.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-put-auto-follow-pattern.html
  - https://docs.opensearch.org/latest/tuning-your-cluster/replication-plugin/index/
  - https://docs.opensearch.org/latest/tuning-your-cluster/replication-plugin/api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-cluster replication

**Goal:** a standby copy.
- ES: `PUT /follower-idx/_ccr/follow` with body `{"remote_cluster":"east","leader_index":"leader-idx"}` (both required); auto-follow `PUT /_ccr/auto_follow/{name}`, so each new index matching the pattern on the remote cluster gets a follower. Auto-follow does not match closed indices or searchable snapshots, and indices with a read or write block should be avoided.
- The model is active-passive: write to the leader, followers pull changes and reject writes; their mappings and aliases cannot be changed manually, so change the leader. The remote cluster must be configured first.
- Leader indices need soft deletes (default on indices created on or after 7.0.0); older indices must be reindexed into a new index.
- OpenSearch (replication plugin): `PUT /_plugins/_replication/{follower-index}/_start`, `_pause`, `_resume`, `_stop` (POST) and `GET .../_status`; the follower pulls from the leader, supports wildcard patterns and works with the Security plugin.
- Elasticsearch CCR is a subscription feature: check Elastic's subscriptions page for the tier that includes it.
- Failure mode: retained history (soft deletes, kept up to configurable limits) too short for the outage you need to survive.

## Verify
- [ ] Follower doc count tracks the leader within the expected lag.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.

## Checked
2026-11-08. Read the Elasticsearch CCR overview, auto-follow, Create follower and Create auto-follow pattern pages and the OpenSearch replication plugin overview and API pages. Confirmed endpoints, required fields, read-only followers and soft deletes. Removed "until promoted/unfollowed" and the "retention leases" wording (not on the pages read), and left the subscription tier as a pointer because the tier column on the subscriptions page could not be read as text.
Method: documentation only; no commands were run.
