---
id: computing-software.messaging-and-integration.celery.celery-task-states-and-results
name: celery-task-states-and-results
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, celery-task-states, result-backend, custom-states, update-state, pickleable-exceptions, rpc-backend, python]
level: practitioner
status: docs-checked
description: "Track Celery task states, pick a result backend, publish PROGRESS custom states with update_state, and write exceptions that survive pickling."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/tasks.html
  - https://docs.celeryq.dev/en/stable/userguide/calling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: observe task progress and results reliably.

## Built-in states
`PENDING` (waiting or unknown; any unknown task id is pending), `STARTED` (only if `track_started`; meta has `pid` and `hostname`), `SUCCESS` (`result` is the return value), `FAILURE` (`result` is the exception, plus `traceback`), `RETRY` (does not propagate), `REVOKED`. A new state replaces the old one. The client uses `PROPAGATE_STATES` to decide whether to re-raise and `READY_STATES` (a state can be cached if the task is ready).

## Result backends
Built-in: SQLAlchemy/Django ORM, Memcached, RabbitMQ/QPid (`rpc`), Redis, or your own. Warning: call `get()` or `forget()` on every `AsyncResult` you get back so resources are released.
- `rpc://` sends states as messages: a result can be retrieved only once and only by the client that sent the task, but it needs no polling. Messages are transient by default; set `result_persistent` for persistent ones.
- Database backends: polling is expensive, so raise polling intervals of `result.get()`. MySQL defaults to `REPEATABLE-READ`, which will not see other transactions' changes; `READ-COMMITTED` is recommended.

## Custom states and progress
```python
@app.task(bind=True)
def upload_files(self, filenames):
    for i, file in enumerate(filenames):
        if not self.request.called_directly:
            self.update_state(state='PROGRESS',
                meta={'current': i, 'total': len(filenames)})
```
Watch every state change from the caller with `result.get(on_message=callback, propagate=False)`; each message is a dict with `task_id`, `result`, `children`, `status`, `traceback`.

Set `result_extended = True` to store extra task metadata in the backend.

## Pickleable exceptions
With pickle as serializer, exceptions must keep original arguments in `.args`. Call `Exception.__init__(self, status_code)` in a custom `__init__`; omitting it is BAD. Keyword arguments are not preserved, so pass them positionally:
```python
class HttpError(Exception):
    def __init__(self, status_code, headers=None, body=None):
        self.status_code = status_code
        self.headers = headers
        self.body = body
        super(HttpError, self).__init__(status_code, headers, body)
```

## Checked

2026-11-07. Re-read the cited page(s) (tasks, calling) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Changed: reworded the READY_STATES sentence to what the page states.

Method: documentation only; no commands were run.
