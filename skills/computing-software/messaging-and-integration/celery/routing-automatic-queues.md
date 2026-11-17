---
id: computing-software.messaging-and-integration.celery.routing-automatic-queues
name: routing-automatic-queues
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, routing, task-routes, queues, task-create-missing-queues, celery-routing-queues]
level: practitioner
status: docs-checked
description: "Route Celery tasks to named queues with task_routes and automatic queue creation, use glob or regex patterns, start workers with -Q, and rename the default queue."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/routing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: send some tasks to a dedicated queue and a dedicated worker with the least configuration.

## Automatic routing

The simplest approach uses `task_create_missing_queues` (on by default): a named queue not already in `task_queues` is created automatically. Say servers x and y run regular tasks and z only runs feed tasks:

```python
task_routes = {'feed.tasks.import_feed': {'queue': 'feeds'}}
```

Import-feed tasks go to `feeds`; everything else goes to the default queue, named `celery` for historical reasons.

Glob patterns and regular expressions match whole namespaces:

```python
app.conf.task_routes = {'feed.tasks.*': {'queue': 'feeds'}}
```

If pattern order matters, use the *items* format. `task_routes` can be a dict or a list of routers, so the setting is a tuple holding a list:

```python
task_routes = ([
    ('feed.tasks.*', {'queue': 'feeds'}),
    ('web.tasks.*', {'queue': 'web'}),
    (re.compile(r'(video|image)\.tasks\..*'), {'queue': 'media'}),
],)
```

## Workers

```console
user@z:/$ celery -A proj worker -Q feeds
user@z:/$ celery -A proj worker -Q feeds,celery
```

`-Q` takes any number of comma-separated queues, so z can also consume the default queue.

## Rename the default queue

```python
app.conf.task_default_queue = 'default'
```

## How the queue is declared

A queue named `video` is created with:

```python
{'exchange': 'video',
 'exchange_type': 'direct',
 'routing_key': 'video'}
```

Non-AMQP transports such as Redis and SQS don't support exchanges, so they need the exchange to have the same name as the queue; this design works for them too.

## Note

Alternate routing concepts like topic and fanout are not available on all transports; consult the transport comparison table.

## Checked

2026-11-07. Re-read the cited page(s) (routing) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. Code snippet and include files were not opened separately.

Changed: removed an unsupported 'kombu' attribution on the transport comparison table.

Method: documentation only; no commands were run.
