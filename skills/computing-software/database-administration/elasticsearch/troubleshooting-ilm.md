---
id: computing-software.database-administration.elasticsearch.troubleshooting-ilm
name: troubleshooting-ilm
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, ilm, ilm-explain, rollover, ilm-retry, index-lifecycle, data-tiers]
level: practitioner
status: docs-checked
description: "Find why Elasticsearch ILM is stuck: _ilm/explain step and error info, common rollover alias and allocation failures, retrying a failed step, and moving an index manually."
sources:
  - https://github.com/elastic/docs-content/blob/main/troubleshoot/elasticsearch/index-lifecycle-management-errors.md
  - https://github.com/elastic/docs-content/blob/main/troubleshoot/elasticsearch/start-ilm.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/configuration-reference/index-lifecycle-management-settings.md
  - https://github.com/elastic/elasticsearch-specification/blob/main/specification/indices/shrink/IndicesShrinkRequest.ts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting ILM

## Where is each index?
```
GET logs-app-*/_ilm/explain?only_errors=true
GET .ds-logs-app-orders-*/_ilm/explain
GET _ilm/status                      # RUNNING / STOPPING / STOPPED
```
Fields: `phase`, `action`, `step`, `failed_step`, `step_info` (the error), `age`,
`is_auto_retryable_error`, `failed_step_retry_count`.

## Common failures
| step_info / symptom | Cause | Fix |
|---|---|---|
| `index.lifecycle.rollover_alias [x] does not point to index [y]` | classic (non-data-stream) rollover alias missing or not write index | add alias with `is_write_index: true` to the current index |
| `setting [index.lifecycle.rollover_alias] for index [y] is empty or not defined` | the rollover action needs the alias setting on non-data-stream indices | set `index.lifecycle.rollover_alias` (or use a data stream, which manages rollover itself) |
| stuck in `check-rollover-ready` forever | conditions never met (low volume), or policy has rollover but index is not managed by an alias | adjust `max_age`/`max_primary_shard_size`; `min_*` conditions too strict |
| stuck in `allocate`/`migrate` step `check-allocation` | no nodes in the target tier (`data_warm`), allocation filters, disk watermarks | add tier nodes or fix the filters, and use `GET _cluster/allocation/explain` |
| `shrink` stuck | shrink needs a copy of every shard on one node with enough disk | ensure capacity, or remove shrink from policy |
| `searchable_snapshot` failure | repository missing or unreachable | verify the repository (`POST _snapshot/repo/_verify`) |
| ILM `STOPPED` | someone ran `_ilm/stop` (e.g. during maintenance) | `POST _ilm/start` |

## Retry
After fixing the cause:
```
POST logs-app-2026.10.01-000005/_ilm/retry
```
Erring indices are retried automatically on each ILM polling interval (`indices.lifecycle.poll_interval`, dynamic, default `10m`; `failed_step_retry_count` increments), and you can run the retry API on demand. If ILM cannot resolve the error, execution halts until the underlying issue is fixed.

## Move an index manually
```
POST _ilm/move/my-index-000005
{ "current_step": { "phase": "hot", "action": "rollover", "name": "check-rollover-ready" },
  "next_step":    { "phase": "warm" } }
```
Use sparingly: skipping steps can leave an index unrolled or misplaced.

## Policy changes
## Verify
`_ilm/explain?only_errors=true` returns no indices; `_cat/indices?v&h=index,creation.date.string,docs.count,store.size&s=index`
shows regular rollovers and old indices deleted on schedule.

## Checked

Checked 2026-10-25 against elastic/docs-content, elastic/elasticsearch and the elasticsearch-specification `main` (Stack 9.x). Confirmed: `_ilm/explain?only_errors=true`, `step_info`, `failed_step`, `is_auto_retryable_error` and `failed_step_retry_count` fields, `_ilm/retry`, `indices.lifecycle.poll_interval` default 10m, the `rollover_alias` error messages, `hot/rollover/check-rollover-ready`, ILM stopped state (`operation_mode`), shrink needing a copy of every shard on one node. Removed the unconfirmed claim about policy edits applying at the next phase and the data-stream rollover_alias error row. The `_ilm/move` request body and the `_cat/indices` Verify call were not re-read.

Method: documentation only; no commands were run.
