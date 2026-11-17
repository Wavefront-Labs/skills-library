---
id: computing-software.search-and-information-retrieval.meilisearch.tasks-and-async-operations
name: tasks-and-async-operations
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [tasks, task-queue, auto-batching, meilisearch]
level: advanced
status: docs-checked
description: "Understand the Meilisearch task queue: statuses, summarized tasks, priority, auto-batching rules, cancelation, deletion and the 1M task cap."
sources: ["https://www.meilisearch.com/docs/capabilities/indexing/tasks_and_batches/async_operations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tasks and asynchronous operations

Index and document changes, settings updates, swaps, dumps, snapshots, and cancel/delete task calls are asynchronous: Meilisearch returns a summarized task (`taskUid`, `indexUid`, `status` always `enqueued`, `type`, `enqueuedAt`) and processes the queue one task at a time in order.

## Statuses

`enqueued`, `processing`, `succeeded`, `failed` (no database change), `canceled`. The last three are finished. A webhook can notify on completion. Global tasks (`dumpCreation`, `taskCancelation`, `taskDeletion`, `indexSwap`, `snapshotCreation`) have `indexUid: null` and need access to all indexes to view them on a protected instance.

## Priority

Always first, in this order: `taskCancelation`, `upgradeDatabase`, `taskDeletion`, `indexCompaction`, `export`, `snapshotCreation`, `dumpCreation`.

## Limits and safety

- A queue near 10GiB raises `no_space_left_on_device`; delete tasks to continue writing.
- Up to 1M tasks are stored; beyond that Meilisearch tries to drop the oldest 100K finished tasks.
- Stopping the instance mid-task is safe: `processing` tasks revert to `enqueued` on restart.

## Auto-batching

Consecutive tasks batch together if same index, same type and same content type. A different index, type, or a delete-by-filter closes the batch. Settings updates batch with each other but never with document additions. Inspect via `/batches`; batch uids are global across indexes.

## Cancel and delete

`POST /tasks/cancel` needs at least one filter (else `missing_task_filters`); only `enqueued` or `processing` tasks cancel, atomically; cancelation tasks are processed in reverse order so they can be canceled. Deletion works only on finished tasks (otherwise `deletedTasks` is 0). After deletion a task returns `task_not_found`.

## Checked

2026-11-03. Confirmed claim by claim against the Asynchronous operations page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
