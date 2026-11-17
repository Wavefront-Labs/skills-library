---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.allocation-explain-unassigned
name: allocation-explain-unassigned
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, allocation-explain-unassigned]
level: advanced
status: docs-checked
description: "Use the allocation explain API to see why a shard is unassigned and which decider blocks it."
sources:
  - https://docs.opensearch.org/latest/api-reference/cluster-api/cluster-allocation/
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-allocation-explain
  - https://docs.opensearch.org/latest/api-reference/cluster-api/cluster-reroute/
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-reroute
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Explain unassigned shards

**Goal:** exact cause, not guessing.
- `GET _cluster/allocation/explain` with no body explains the first unassigned shard (OpenSearch page); target one with `{"index":"my-index","shard":0,"primary":false}`. `POST` is also accepted.
- Read `unassigned_info.reason` and each node's `deciders` (for example `disk_threshold`, `same_shard`, `filter`, `awareness`, `max_retry`).
- Optional query parameters: `include_yes_decisions` and `include_disk_info` (both default false).
- After the maximum number of failed allocation attempts, retry with `POST _cluster/reroute?retry_failed=true`.
- Failure mode: a primary with no valid copy cannot be fixed by reroute alone. Restore from a snapshot, or as a last resort use the reroute commands `allocate_stale_primary` or `allocate_empty_primary`, which require `accept_data_loss: true` and can lose data.

## Verify
- [ ] The shard that was unassigned now reports `current_state` `started` in the explain response, or no unassigned shards remain.

## Checked
Date: 2026-11-07
- OpenSearch cluster allocation explain page, read in full: GET/POST endpoints, first unassigned shard with no body, request body fields, `include_yes_decisions` and `include_disk_info` defaults, `unassigned_info.reason`, the decider list (`same_shard`, `disk_threshold`, `filter`, `awareness`, `max_retry`).
- Elasticsearch allocation explain API page, read in full: body and query parameters, `unassigned_info.reason` values, `node_allocation_decisions[].deciders`, the `max_retry` example that says to call `POST /_cluster/reroute?retry_failed`.
- Elasticsearch reroute API page: searched for `retry_failed`, `allocate_stale_primary`, `allocate_empty_primary` and `accept_data_loss` (data-loss wording confirmed); OpenSearch reroute page searched for the same (`retry_failed=true` example, `accept_data_loss` must be true). Neither read end to end.
- Removed: the "no shards to explain" Verify string (not on either page); Verify rewritten to use `current_state`.
Method: documentation only; no commands were run.
