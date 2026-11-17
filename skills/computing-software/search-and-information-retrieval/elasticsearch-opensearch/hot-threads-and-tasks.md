---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.hot-threads-and-tasks
name: hot-threads-and-tasks
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, hot-threads-and-tasks]
level: advanced
status: docs-checked
description: "Use hot_threads and the task management API to find and cancel CPU-heavy or long-running work."
sources:
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-hot-threads
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-tasks-list
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-tasks-cancel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hot threads and task management

**Goal:** see what a busy node is doing.
- `GET _nodes/hot_threads` (or `/_nodes/{node_id}/hot_threads`); needs cluster privilege `monitor` or `manage`. Parameters: `threads` (default 3), `interval` (default 500ms), `snapshots` (default 10), `type` (`cpu` default; also wait, block, gpu, mem), `ignore_idle_threads` (default true). Output is plain text; look for search, write, merge or GC activity.
- `GET _tasks?detailed=true&actions=*search*` lists running searches. `detailed` is more costly; `group_by` is nodes (default), parents or none; the Tasks API is beta and may change.
- Cancel: `POST _tasks/<node:id>/_cancel`, or `POST _tasks/_cancel?actions=...` with filters (`nodes`, `parent_task_id`); needs cluster `manage`.
- Failure mode: a cancelled task may keep running for a while, because it cannot always stop its current work safely at once; the `cancelled` flag only shows the cancellation was processed. Other tasks may need to finish first.
- If a cancellation is slow, use the task list with `detailed` and hot threads to see what else is running.

## Verify
- [ ] CPU drops after the offending task is cancelled and the culprit query is fixed.

## Checked
Date: 2026-11-08
Method: Read the Elasticsearch hot threads, list tasks and cancel task API references in full; OpenSearch was not checked.
