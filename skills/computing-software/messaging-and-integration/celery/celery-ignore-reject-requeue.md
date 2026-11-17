---
id: computing-software.messaging-and-integration.celery.celery-ignore-reject-requeue
name: celery-ignore-reject-requeue
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, celery-task-options, ignore, reject, requeue, dead-letter-exchange, acks-late, semipredicates]
level: advanced
status: docs-checked
description: "Use the Celery Ignore and Reject exceptions to skip result storage, store results manually, dead-letter a message, or requeue it, and know the acks_late dependency."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/tasks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: control how the worker treats a task's final outcome by raising a semipredicate exception from `celery.exceptions`.

## Ignore
`raise Ignore()` makes the worker record no state for the task, but the message is still acknowledged. Use it for custom revoke-like behaviour or to store results yourself.
```python
from celery import states
from celery.exceptions import Ignore

@app.task(bind=True)
def get_tweets(self, user):
    timeline = twitter.get_timeline(user)
    if not self.request.called_directly:
        self.update_state(state=states.SUCCESS, meta=timeline)
    raise Ignore()
```
A custom revoke example checks `redis.ismember('tasks.revoked', self.request.id)` and raises `Ignore()`.

## Reject
`raise Reject(exc, requeue=False)` rejects the message with AMQP `basic_reject`. The broker-level reject only has effect when `Task.acks_late` is enabled. Rejecting equals acking, but brokers may add behaviour: RabbitMQ can route rejected messages to a Dead Letter Exchange configured on the queue.

Without requeue (`requeue=False`) the task never runs again: the result is stored as `FAILURE`, `task_failure` is sent, `AsyncResult.failed()` returns True and the reason is the result. That terminal result is recorded regardless of `acks_late`.

Dead-letter on out-of-memory:
```python
@app.task(bind=True, acks_late=True)
def render_scene(self, path):
    file = get_file(path)
    try:
        renderer.render_scene(file)
    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    except Exception as exc:
        raise self.retry(exc, countdown=10)
```

Requeue (`requeue=True`) only takes effect with `acks_late`; the message is redelivered and run again and no terminal result is stored. Be careful: it can easily cause an infinite message loop.
```python
@app.task(bind=True, acks_late=True)
def requeues(self):
    if not self.request.delivery_info['redelivered']:
        raise Reject('no reason', requeue=True)
    print('received two times')
```

## Retry
`Retry` is raised by `Task.retry()` to tell the worker the task is being retried (see the retry skill).

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/tasks.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
