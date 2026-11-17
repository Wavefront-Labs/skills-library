---
id: computing-software.database-administration.elasticsearch.task-management-api
name: task-management-api
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, task-management-api, tasks, cancel-task, elasticsearch-operations, long-running-queries]
level: practitioner
status: verified
description: "List, inspect and cancel long-running Elasticsearch tasks (searches, reindex, update_by_query, force merge) with the _tasks API, and run big jobs as async tasks."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tasks.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html#docs-reindex-task-api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task management API

## Find what is running
```bash
GET _tasks?detailed=true&actions=*search*&group_by=parents
GET _cat/tasks?v&detailed&s=running_time:desc&h=action,task_id,running_time,node,description
```
`detailed` shows the request description (index pattern and query excerpt for searches). `running_time_in_nanos` locates the long-running ones.

## Cancel
```bash
POST _tasks/oTUltX4IQMOUUVeiohTt8A:12345/_cancel
POST _tasks/_cancel?actions=*search*&nodes=data-hot-3
```
Search tasks check for cancellation periodically and stop; child tasks on other nodes are cancelled with the parent. Some tasks are not cancellable (`cancellable: false`). Cancelling `_reindex` leaves already-copied documents in the destination.

## Long jobs as tasks
```bash
POST _reindex?wait_for_completion=false&slices=auto&requests_per_second=2000
{ "source": { "index": "old" }, "dest": { "index": "new" } }
# returns {"task": "node:id"}
GET _tasks/<node:id>                          # status: total, created, updated, batches
POST _reindex/<node:id>/_rethrottle?requests_per_second=-1   # unthrottle
```
Completed task results are stored in the `.tasks` index. `DELETE .tasks/_doc/<node:id>` is refused on 9.5 even for `superuser` (403, `.tasks` is a restricted index), so do not build cleanup around it.

## Protecting the cluster from runaway searches
- `search.default_search_timeout` cluster setting (partial results after timeout).
- `X-Opaque-Id` header from applications: appears under `headers` in `GET _tasks?detailed=true` output (confirmed), so you can tell which service sent the request before cancelling.
- `search.max_buckets`, circuit breakers and `indices.query.bool.max_clause_count` limit damage.

## Verify
After cancelling a throttled reindex, `GET _tasks/<id>` returned `completed: true` with `"canceled": "by user request"` in the response and only the already-copied documents (10) in the destination; node CPU and search thread pool queue return to baseline.
