---
id: computing-software.messaging-and-integration.celery.routing-manual-queues-exchanges
name: routing-manual-queues-exchanges
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, routing, task-queues, kombu, exchange, routing-key, topic, celery-routing-queues]
level: practitioner
status: docs-checked
description: "Define Celery task_queues with kombu Queue and Exchange, set default exchange and routing key, bind multiple keys to one queue, and send to a queue per call."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/routing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: take full control of queues, exchanges and routing keys instead of relying on automatic queues.

## Topic setup

```python
from kombu import Queue

app.conf.task_default_queue = 'default'
app.conf.task_queues = (
    Queue('default',    routing_key='task.#'),
    Queue('feed_tasks', routing_key='feed.#'),
)
app.conf.task_default_exchange = 'tasks'
app.conf.task_default_exchange_type = 'topic'
app.conf.task_default_routing_key = 'task.default'
```

`task_queues` is a list of kombu `Queue` instances. If a queue sets no exchange or exchange type, they come from `task_default_exchange` and `task_default_exchange_type`.

Route a task:

```python
task_routes = {
    'feeds.tasks.import_feed': {
        'queue': 'feed_tasks',
        'routing_key': 'feed.import',
    },
}
```

Or override per call with `apply_async` (or `send_task`):

```python
import_feed.apply_async(args=['http://cnn.com/rss'],
                        queue='feed_tasks',
                        routing_key='feed.import')
```

## Workers

```console
user@z:/$ celery -A proj worker -Q feed_tasks --hostname=z@%h
user@x:/$ celery -A proj worker -Q default --hostname=x@%h
user@z:/$ celery -A proj worker -Q feed_tasks,default --hostname=z@%h
```

The last form lets the feed worker also take regular tasks when busy.

## Custom exchange for one queue

```python
from kombu import Exchange, Queue

app.conf.task_queues = (
    Queue('feed_tasks',    routing_key='feed.#'),
    Queue('regular_tasks', routing_key='task.#'),
    Queue('image_tasks',   exchange=Exchange('mediatasks', type='direct'),
                           routing_key='image.compress'),
)
```

## Default queue, exchange, routing key

`task_default_queue` routes tasks with no explicit route. The default exchange, exchange type and routing key are the default routing values for tasks and the defaults for entries in `task_queues`:

```python
default_exchange = Exchange('default', type='direct')
media_exchange = Exchange('media', type='direct')
app.conf.task_queues = (
    Queue('default', default_exchange, routing_key='default'),
    Queue('videos', media_exchange, routing_key='media.video'),
    Queue('images', media_exchange, routing_key='media.image'),
)
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'default'
app.conf.task_default_routing_key = 'default'
```

## Multiple bindings on one queue

```python
from kombu import Exchange, Queue, binding
media_exchange = Exchange('media', type='direct')
CELERY_QUEUES = (
    Queue('media', [
        binding(media_exchange, routing_key='media.video'),
        binding(media_exchange, routing_key='media.image'),
    ]),
)
```

Celery auto-creates the entities for queues in `task_queues` unless the queue's `auto_declare` is False.

## Checked

2026-11-07. Re-read the cited page(s) (routing) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
