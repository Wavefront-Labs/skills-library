---
id: computing-software.messaging-and-integration.celery.celery-task-class-handlers
name: celery-task-class-handlers
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, celery-task-handlers, custom-task-class, on-failure, on-success, before-start, after-return, custom-request]
level: advanced
status: docs-checked
description: "Write Celery custom task base classes, lifecycle handlers (before_start, on_success, on_retry, on_failure, after_return), cached resources, and custom Request classes."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/tasks.html
  - https://docs.celeryq.dev/en/stable/userguide/application.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: share behaviour across tasks with a `celery.Task` subclass.

## Instantiation
A task is not instantiated per request; it is a global instance in the registry, so `__init__` runs once per process and state persists. Use that to cache resources:
```python
class DatabaseTask(Task):
    _db = None
    @property
    def db(self):
        if self._db is None:
            self._db = Database.connect()
        return self._db

@app.task(base=DatabaseTask, bind=True)
def process_rows(self):
    for row in self.db.table.all(): process_row(row)
```
App-wide: `Celery('tasks', task_cls='your.module.path:DatabaseTask')` (string path or class; default `'celery.app.task:Task'`). Or set `app.Task = MyBaseTask`.

## Handlers (all run synchronously in the worker process)
Order: `before_start` (blocks; `run()` waits) -> `run()` -> result stored -> `on_success` / `on_retry` / `on_failure` -> `after_return`.
- `before_start(self, task_id, args, kwargs)` (5.2)
- `on_success(self, retval, task_id, args, kwargs)`
- `on_retry(self, exc, task_id, args, kwargs, einfo)` runs after state is RETRY, before the retry is scheduled
- `on_failure(self, exc, task_id, args, kwargs, einfo)`
- `after_return(self, status, retval, task_id, args, kwargs, einfo)` runs on terminal states only, not RETRY, REJECTED or IGNORED; use the `task_postrun` signal for every attempt.

Return values are ignored. The result backend is updated before `on_success`/`on_failure`, so clients can see SUCCESS or FAILURE while the handler runs. If `on_success` raises, it is logged at ERROR and the task stays SUCCESS (no errbacks, no `task_failure`); eagerly, it propagates to the caller. `after_return` raising is logged and the recorded outcome stands.

## Overriding __call__
If you override `__call__` call `self.run(*args, **kwargs)`, not `super().__call__`.

## Custom Request
Set `Request = MyRequest` (class or FQN) on the task class; inherit from `celery.worker.request.Request`. With the prefork pool, `on_timeout(self, soft, timeout)` and `on_failure(self, exc_info, send_failed_event=True, return_ok=False)` run in the main worker process, e.g. to log hard timeouts when `not soft`.

## Checked

2026-11-07. Re-read the cited page(s) (tasks, application) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
