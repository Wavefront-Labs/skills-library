---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.ilm-policy-phases
name: ilm-policy-phases
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, ilm-policy-phases, es-ilm]
level: practitioner
status: docs-checked
description: "Define hot, warm, cold, frozen and delete phases with actions such as rollover, shrink, forcemerge and delete."
sources:
  - https://www.elastic.co/docs/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy
  - https://www.elastic.co/docs/manage-data/lifecycle/index-lifecycle-management/index-lifecycle
  - https://www.elastic.co/docs/manage-data/lifecycle/index-lifecycle-management/rollover
  - https://www.elastic.co/docs/reference/elasticsearch/index-lifecycle-actions/ilm-rollover
  - https://www.elastic.co/docs/reference/elasticsearch/index-lifecycle-actions/ilm-forcemerge
  - https://www.elastic.co/docs/reference/elasticsearch/configuration-reference/index-lifecycle-management-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Write an ILM policy with phases

**Goal:** automated retention.
```
PUT _ilm/policy/logs
{"policy":{"phases":{"hot":{"actions":{"rollover":{"max_age":"7d","max_primary_shard_size":"50gb"}}},"warm":{"min_age":"7d","actions":{"forcemerge":{"max_num_segments":1}}},"delete":{"min_age":"90d","actions":{"delete":{}}}}}}
```
- Attach a policy through the `index.lifecycle.name` index setting (for example in an index template). When ILM manages rollover on an alias, also set `index.lifecycle.rollover_alias`; it is not needed with data streams.
- Action phases: `rollover` is allowed only in `hot`; `forcemerge` in `hot` and `warm`; `delete` only in `delete`. `rollover` accepts `max_age`, `max_docs` and `max_primary_shard_size` (and others); `forcemerge` takes `max_num_segments`.
- After a rollover, `min_age` is measured from the rollover time, not index creation.
- ILM runs periodically: `indices.lifecycle.poll_interval` controls how often it checks (default `10m`), and an action can take several runs to finish, so changes are not instant.
- A `min_age` change in an updated policy does not affect indices that are already executing that phase.

## Verify
- [ ] `GET logs-*/_ilm/explain` shows the expected phase and action.

## Scope
The Elasticsearch documentation was checked; OpenSearch (ISM) was not.

## Checked

Checked 2026-11-02 against the Elasticsearch docs: Configure a lifecycle policy, Index lifecycle, Rollover, Policy updates, ILM rollover and forcemerge action references, and the ILM settings reference. Confirmed: all statements above. Removed: the OpenSearch source root.

Method: documentation only; no commands were run.
