---
id: computing-software.messaging-and-integration.celery.signals-task-handlers
name: signals-task-handlers
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, signals, task-prerun, task-failure, after-task-publish, handlers, celery-signals-task]
level: practitioner
status: docs-checked
description: "Connect Celery signal handlers for task publish, prerun, postrun, retry, success, failure, revoked and unknown events, with senders and provided arguments."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/signals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: hook into the task lifecycle with decoupled handlers.

## Connecting

```python
from celery.signals import after_task_publish

@after_task_publish.connect
def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
    info = headers if 'task' in headers else body   # headers for protocol v2
    print('after_task_publish for task id {info[id]}'.format(info=info))

@after_task_publish.connect(sender='proj.tasks.add')   # filter by sender
def handler(sender=None, headers=None, body=None, **kwargs): ...
```

Signals share the django.core.dispatch implementation. Always accept `**kwargs` so new Celery versions can add arguments without breaking you.

## Signals, senders and arguments

Publishing side (runs in the sending process; sender is the task name):
- `before_task_publish` (3.1+): `body`, `exchange`, `routing_key`, `headers` (modifiable), `properties` (modifiable), `declare` (modifiable), `retry_policy` (modifiable, any `kombu.Connection.ensure` argument).
- `after_task_publish`: `headers`, `body`, `exchange`, `routing_key`.

Execution (sender is the task object):
- `task_prerun`: `task_id`, `task`, `args`, `kwargs`.
- `task_postrun`: same plus `retval` and `state`.
- `task_retry`: `request`, `reason`, `einfo`. Only `request` is guaranteed; `reason` and `einfo` may be None or missing (e.g. cancelled then retried).
- `task_success`: `result`, and `runtime` (5.7+), seconds from start of tracing until the result is stored and callbacks dispatched (the "succeeded in Xs" log value).
- `task_failure`: `task_id`, `exception`, `args`, `kwargs`, `traceback`, `einfo`.
- `task_internal_error`: `task_id`, `args`, `kwargs`, `request` (the original request dictionary, since `task.request` may not be ready), `exception`, `traceback`, `einfo`.

Consumer side (sender is the Consumer or task):
- `task_received`: `request` is a `Request` instance, not `task.request`; with prefork it is sent in the parent process.
- `task_revoked`: `request` (a `Context`, same prefork caveat), `terminated`, `signum` (None with terminated True means TERM), `expired`.
- `task_unknown`: `name`, `id`, `message`, `exc` when a message names an unregistered task.
- `task_rejected`: `message`, `exc` for an unknown type of message on a task queue.

`task_sent` is deprecated; use `after_task_publish`.

## Checked

2026-11-07. Re-read the cited page(s) (signals) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. Code snippet and include files were not opened separately.

Changed: removed a module path for Request that the page does not give.

Method: documentation only; no commands were run.
