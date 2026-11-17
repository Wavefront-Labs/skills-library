---
id: computing-software.messaging-and-integration.celery.celery-task-limits-and-acks
name: celery-task-limits-and-acks
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, celery-task-options, rate-limit, time-limit, acks-late, throws, track-started, ignore-result, python]
level: practitioner
status: docs-checked
description: "Tune Celery per-task options: rate_limit, hard and soft time limits, acks_late and worker-lost behaviour, throws, track_started, ignore_result and store_errors_even_if_ignored."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/tasks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: set task attributes through the decorator (any keyword becomes an attribute of the task class).

## Acknowledgement
Default: the message is acked just before execution so a started task is never rerun. `acks_late=True` acks after the task returns (global default `task_acks_late`); the task may then run multiple times if the worker crashes, so it must be idempotent. Even with `acks_late`, the message is acked if the child process is killed (task calls `sys.exit` or gets a signal), deliberately. To redeliver in those cases enable `task_reject_on_worker_lost`.

## Rate limit
`rate_limit=None` (default `task_default_rate_limit`) means off; a number is tasks per second; strings take `"/s"`, `"/m"`, `"/h"`. `"100/m"` enforces at least 600ms between starts on one worker. It is per worker instance, not global; for a global limit restrict the task to a given queue. With `countdown` or `eta` the task starts at the later of ETA and the next rate-limit slot. Warning: a rate-limited waiting task still counts against prefetch, so a burst can stop the worker fetching any message (even unlimited tasks); route rate-limited tasks to dedicated workers.

## Time limits
`time_limit` (hard) and `soft_time_limit` in seconds; unset uses the worker default. A soft limit raises `SoftTimeLimitExceeded` in the child; if it propagates, `on_failure`, errbacks and the `task_failure` signal run; if the task catches it and exits normally they do not. A hard limit kills the child, and since 5.7 the parent process invokes `on_failure`, errbacks and `task_failure`. Prefer manual I/O timeouts (for example `requests.get(URL, timeout=(5.0, 30.0))`); a task that blocks forever can stop the worker doing other work.

## Other options
- `throws=(KeyError, HttpNotFound)`: expected errors are stored as failures but logged at INFO without traceback; others log at ERROR with traceback.
- `track_started=True`: report a STARTED state (pid and hostname in `result.info`); default False; global `task_track_started`.
- `ignore_result=True`: store no state, so `AsyncResult` cannot report ready or the value.
- `store_errors_even_if_ignored=True`: store errors anyway. Since 5.7 the worker falls back to `Task.ignore_result` when the request has no override.
- `max_retries` (default 3), `default_retry_delay`, `serializer`, `compression`, `backend`.

## Checked

2026-11-07. Re-read the cited page(s) (tasks) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
