---
id: computing-software.messaging-and-integration.celery.routing-custom-routers-broadcast
name: routing-custom-routers-broadcast
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, routing, routers, broadcast, task-routes, kombu, celery-routing-routers]
level: practitioner
status: docs-checked
description: "Write Celery router functions for task_routes, understand destination precedence and queue expansion, and fan tasks out to every worker with Broadcast queues."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/routing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide routing dynamically with a router, and broadcast a task to all workers.

## Destination precedence

A task's destination is decided by, in order:

1. Routing arguments to `Task.apply_async`.
2. Routing attributes defined on the Task itself.
3. Routers in `task_routes`.

Best practice is not to hard-code these, but leave them to configuration via routers; sensible defaults can still be task attributes.

## Router function

Signature: `(name, args, kwargs, options, task=None, **kw)`.

```python
def route_task(name, args, kwargs, options, task=None, **kw):
    if name == 'myapp.tasks.compress_video':
        return {'exchange': 'video',
                'exchange_type': 'topic',
                'routing_key': 'video.compress'}
```

If you return the `queue` key it expands using that queue's definition in `task_queues`: `{'queue': 'video', 'routing_key': 'video.compress'}` becomes `{'queue': 'video', 'exchange': 'video', 'exchange_type': 'topic', 'routing_key': 'video.compress'}`.

Install routers in `task_routes`, as objects or by dotted name:

```python
task_routes = (route_task,)
task_routes = ('myapp.routers.route_task',)
```

A plain dict is equivalent for simple name-to-route mappings:

```python
task_routes = {
    'myapp.tasks.compress_video': {
        'queue': 'video',
        'routing_key': 'video.compress',
    },
}
```

Routers are traversed in order and the first returning a true value wins; a sequence can mix functions and dicts. A route may also carry a default `'priority'` (Redis or RabbitMQ), overridden by `task.apply_async(priority=0)`.

## Broadcast

`Broadcast` delivers a copy of each task to every worker consuming the queue:

```python
from kombu.common import Broadcast

app.conf.task_queues = (Broadcast('broadcast_tasks'),)
app.conf.task_routes = {
    'tasks.reload_cache': {
        'queue': 'broadcast_tasks',
        'exchange': 'broadcast_tasks'
    }
}
```

With beat, use `'options': {'exchange': 'broadcast_tasks'}` in the `beat_schedule` entry, e.g. `crontab(minute=0, hour='*/3')`.

Gotcha: Celery doesn't define what happens when two tasks share a task_id, so with broadcast the state history may not be preserved. The page suggests setting `task.ignore_result` in this case.

## Checked

2026-11-07. Re-read the cited page(s) (routing) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
