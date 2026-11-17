---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.ism-explain-retry-failed
name: ism-explain-retry-failed
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, ism-explain-retry-failed]
level: advanced
status: docs-checked
description: "Use the OpenSearch ISM explain API, retry and change_policy to recover indices stuck in failed actions."
sources:
  - https://docs.opensearch.org/latest/im-plugin/ism/api/
  - https://docs.opensearch.org/latest/im-plugin/ism/settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debug and retry failed ISM actions

**Goal:** unblock lifecycle runs.
- `GET _plugins/_ism/explain/<index>` (patterns allowed) returns `policy_id`, `enabled`, and `state`, `action`, `step`, `retry_info` and `info.message` objects. A failed action shows `"failed": true` in `action` and `"step_status": "failed"` in `step`; `info.message` describes the problem.
- Since 2.12, `POST _plugins/_ism/explain/<index>` takes a `filter` (`policy_id`, `state`, `action_type`, `failed`) to list only matching indexes; `show_policy=true` adds the applied policy.
- Right after attaching a policy, `total_managed_indices` is 0 and the fields are null until ISM creates the managed index job on its next sweep.
- Retry after fixing the cause: `POST _plugins/_ism/retry/<index>`. Optional body `{"state":"hot"}` restarts in that state instead of where it failed; wildcards retry many. An index that is not failed comes back in `failed_indices` with "This index is not in failed state."
- Switch policies: `POST _plugins/_ism/change_policy/<index> {"policy_id":"new","state":"...","include":[{"state":"..."}]}`. It is asynchronous: minor changes (like a new `min_index_age`) apply on the next run, changes to the current state's actions or structure apply at the end of that state. `updated_indices` counts recorded changes, not indexes already moved.
- Job interval is `plugins.index_state_management.job_interval`, in minutes, default 5; ISM settings are dynamic.
- The rollover alias setting requirement was not checked.

## Verify
- [ ] Explain shows `"failed": false` and the next action.

## Checked
Date: 2026-11-08
Method: Read the OpenSearch ISM API page (explain, retry, change policy sections) and ISM settings page; the rollover action page was not found to cover the alias setting, so that was not verified. Elasticsearch was not checked.
