---
id: computing-software.messaging-and-integration.celery.celery-time-limits-and-late-ack
name: celery-time-limits-and-late-ack
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-limits-acks, celery, time-limit, soft-time-limit, acks-late, reject-on-worker-lost, retry-on-worker-lost, idempotent]
level: practitioner
status: docs-checked
description: "Configure Celery hard and soft time limits, late acknowledgment, and worker-lost handling with exact setting names and defaults."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
  - https://docs.celeryq.dev/en/stable/userguide/optimizing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Time limits, late acks and worker-lost handling

Goal: control what happens to a task message when a task is slow, fails, or its process dies.

## Time limits
- `task_time_limit` (default none): hard limit in seconds; the worker process is killed and replaced.
- `task_soft_time_limit` (default none): raises `SoftTimeLimitExceeded` in the task so it can clean up:

```python
from celery.exceptions import SoftTimeLimitExceeded

@app.task
def mytask():
    try:
        return do_work()
    except SoftTimeLimitExceeded:
        cleanup_in_a_hurry()
```

## Acknowledgment
- `task_acks_late` (default disabled): acknowledge after execution rather than right before. Tasks must then be idempotent, since a started task is retried after power failure or abrupt worker kill.
- `task_acks_on_failure` (5.7+, default `None`, falls back to `task_acks_on_failure_or_timeout`): when enabled, failed task messages are acknowledged; when disabled they are rejected without requeue.
- `task_acks_on_timeout` (5.7+, default `None`, same fallback): enabled acks timed-out tasks; disabled rejects and requeues them.
- `task_acks_on_failure_or_timeout` (deprecated 6.0, default enabled) acknowledges even on failure or timeout.
- All three only apply when `task_acks_late` is enabled.
- Exceptions are considered normal operation and are acknowledged; use `task.retry()` for them. Acks guard against failures Python cannot handle (power failure, fatal signal).

## Worker process lost
- Even with `task_acks_late`, the worker acknowledges tasks whose process exits abruptly or is signaled (KILL/INT).
- `task_reject_on_worker_lost` (default disabled): requeue instead. Warning: can cause message loops.
- `task_retry_on_worker_lost` (5.7+, default disabled): send the task again like `Task.retry()`: `max_retries` and `default_retry_delay` (180 s) apply, counting against the same `max_retries` as the task's own retries; when exhausted the task is marked failed. Takes precedence over `task_reject_on_worker_lost`; if sending fails, falls back to it. Also applies when `task_acks_late` is off. It covers only a pool child dying while the main worker survives; if the whole worker or container is OOM-killed it has no effect.
- `worker_lost_wait` (default 10.0 s): how long to wait for missing results before raising `WorkerLostError`.
- On RabbitMQ 4.0+, quorum queues drop or dead-letter a message after 20 redeliveries by default, so a task that keeps crashing its worker can vanish without a worker log.
- `worker_cancel_long_running_tasks_on_connection_loss` (5.1+, default disabled): cancel late-ack tasks on connection loss instead of having them run twice. Celery 6.0 will default it to `True`; leaving it off emits a warning.

## Checked

2026-11-07. Re-read the cited page(s) (configuration, optimizing) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
