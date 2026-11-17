---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.ism-policy-states-transitions
name: ism-policy-states-transitions
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, ism-policy-states-transitions, os-ism]
level: practitioner
status: docs-checked
description: "Define OpenSearch ISM states, actions and transitions (hot, warm, delete) and attach the policy to indices with ism_template."
sources:
  - https://docs.opensearch.org/latest/im-plugin/ism/policies/
  - https://docs.opensearch.org/latest/im-plugin/ism/policies-operations/
  - https://docs.opensearch.org/latest/im-plugin/ism/api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Write an ISM policy

**Goal:** lifecycle automation in OpenSearch.
```
PUT _plugins/_ism/policies/logs
{"policy":{"description":"logs","default_state":"hot","states":[
 {"name":"hot","actions":[{"rollover":{"min_index_age":"7d"}}],"transitions":[{"state_name":"delete","conditions":{"min_index_age":"30d"}}]},
 {"name":"delete","actions":[{"delete":{}}],"transitions":[]}],
 "ism_template":[{"index_patterns":["logs-*"],"priority":100}]}}
```
- A policy has a required `default_state` and `states`, plus optional `description`, `ism_template` and `error_notification`. An index is in one state at a time.
- A state's actions run in order on entering the state; if one fails the rest are skipped. Optional per-action `timeout` and `retry` (`count`, `backoff` Exponential default, `delay` default 1 minute).
- Transitions are checked in order after the actions; the first that evaluates true wins, and one with no conditions is always true.
- Conditions: `min_index_age`, `min_rollover_age`, `min_state_age`, `min_doc_count`, `min_size` (primary shard storage), `no_alias`, `cron`.
- `ism_template` applies the policy automatically to new matching indexes; `priority` picks the winner when several match. Existing indexes need `POST _plugins/_ism/add/<index> {"policy_id":"logs"}`; that fails (in `failed_indices`) if the index already has a policy, so use the update managed index policy API then.
- Do not add a policy with `*` as the index: it matches system indexes such as `.opendistro-security`, and a delete action could remove roles and tenants. Use a prefix like `logs-*`.
- Supported actions include force merge, read only, read write, replica count, shrink, close, open, delete, rollover, notification, snapshot, index priority, allocation, rollup, stop replication, search only and convert index to remote.

## Verify
- [ ] `GET _plugins/_ism/explain/logs-000001` shows the policy and current state.

## Checked
Date: 2026-11-08
Method: Read the OpenSearch ISM policies page, supported-operations page and ISM API page (add policy) in the body chunks; the final few thousand characters of the policies page were not read. Elasticsearch was not checked.
