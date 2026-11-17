---
id: computing-software.messaging-and-integration.celery.celery-task-request-and-logging
name: celery-task-request-and-logging
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, celery-task-request, task-request, task-logging, get-task-logger, argsrepr, sensitive-data, python]
level: practitioner
status: docs-checked
description: "Read the running task context via self.request, log with get_task_logger, redirect stdout, and hide secrets in logs with argsrepr and kwargsrepr."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/tasks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: inspect the current task's context, log properly, and keep secrets out of logs and events.

## Task request
`Task.request` holds state for the executing task (use a bound task: `@app.task(bind=True)`). Attributes include `id`, `group`, `chord`, `args`, `kwargs`, `origin`, `retries` (starts at 0), `is_eager`, `eta`, `expires`, `hostname`, `delivery_info` (exchange and routing key; keys depend on broker), `reply_to`, `correlation_id`, `called_directly`, `timelimit` (a `(hard, soft)` pair), `callbacks`, `errbacks`, `headers`, `root_id`, `parent_id`, `chain`, `properties`, `replaced_task_nesting`. New in 5.7: `time_limit` and `soft_time_limit`.
```python
@app.task(bind=True)
def dump_context(self, x, y):
    print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(self.request))
```

## Logging
Create one logger per module:
```python
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
```
It inherits from the `celery.task` logger so the task name and id appear in logs. Anything written with `print` to stdout/stderr is redirected to logging (disable via `worker_redirect_stdouts`). The worker will not update that redirection if you create a logger inside a task or task module; redirect manually with `self.app.log.redirect_stdouts_to_logger(logger, self.app.conf.worker_redirect_stdouts_level)` and restore `sys.stdout, sys.stderr` in `finally`.

If a Celery logger is silent, check it propagates: in an `after_setup_logger` signal handler set `logging.getLogger('celery.app.trace').propagate = True`. To disable Celery's logging configuration entirely, connect a no-op handler to the `setup_logging` signal.

## Hide sensitive arguments
With `task_protocol` 2+ (default since 4.0), override how args appear in logs and events:
```python
add.apply_async((2, 3), argsrepr='(<secret-x>, <secret-y>)')
charge.s(account, card='1234 5678 1234 5678').set(
    kwargsrepr=repr({'card': '**** **** **** 5678'})).delay()
```
Gotcha: the real values are still readable by anyone who can read the message from the broker; encrypt it or fetch secrets from a secure store inside the task.

## Checked

2026-11-07. Re-read the cited page(s) (tasks) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
