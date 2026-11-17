---
id: computing-software.search-and-information-retrieval.meilisearch.filter-tasks
name: filter-tasks
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [filter-tasks, task-filters, batches-route, meilisearch]
level: practitioner
status: docs-checked
description: "Filter the Meilisearch tasks list by uids, statuses, types, indexUids, canceledBy and RFC 3339 date bounds, combine with &, and paginate with limit, from, reverse."
sources: ["https://www.meilisearch.com/docs/capabilities/indexing/tasks_and_batches/filter_tasks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filtering tasks

`GET /tasks` returns all undeleted tasks; narrow with query parameters. Each accepts comma-separated values; different filters combine with logical AND using `&`. OR across different filters is not supported.

## Parameters

- `uids`, `batchUids`, `statuses` (enqueued, processing, succeeded, failed, canceled), `types` (such as `documentAdditionOrUpdate`, `indexDeletion`), `indexUids` (case-sensitive), `canceledBy`.
- Date filters with RFC 3339 values: `beforeEnqueuedAt`, `afterEnqueuedAt`, `beforeStartedAt`, `afterStartedAt`, `beforeFinishedAt`, `afterFinishedAt`.
- Paging: `limit` (default 20), `from` (uid of the first task returned, default the latest), `reverse` (true gives oldest first, default false).

Example: tasks of index `movies` with type `documentAdditionOrUpdate` or `documentDeletion` and status `processing`.

`/batches` filters the same way, but parameters like `uids` target the tasks inside batches, not the batches.

## Checked

2026-11-03. Confirmed claim by claim against the Filter tasks page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: an unsupported claim about strict date comparison.

Method: documentation only; no commands were run.
