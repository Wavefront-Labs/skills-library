---
id: computing-software.messaging-and-integration.celery.celery-worker-queues-and-inspect
name: celery-worker-queues-and-inspect
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-worker-queues, celery, queues, add-consumer, inspect, ping, remote-control, active-queues]
level: practitioner
status: docs-checked
description: "Choose worker queues with -Q, add or cancel consumers at runtime, and inspect registered, active, scheduled and reserved tasks, stats and ping."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/workers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control worker queues and inspect workers at runtime

Goal: change which queues a worker consumes and see what it is doing.

By default a worker consumes all queues in `task_queues` (falling back to the queue named `celery`). At start choose queues: `celery -A proj worker -l INFO -Q foo,bar,baz`. A name not in `task_queues` is auto-created depending on `task_create_missing_queues`.

At runtime (add_consumer is idempotent):

```console
$ celery -A proj control add_consumer foo
$ celery -A proj control add_consumer foo -d celery@worker1.local
$ celery -A proj control cancel_consumer foo
```

```pycon
>>> app.control.add_consumer('foo', reply=True)
>>> app.control.add_consumer(queue='baz', exchange='ex', exchange_type='topic',
...     routing_key='media.*', options={'queue_durable': False, 'exchange_durable': False},
...     reply=True, destination=['w1@example.com', 'w2@example.com'])
>>> app.control.cancel_consumer('foo', reply=True)
```

List queues: `celery -A proj inspect active_queues [-d celery@worker1.local]` or `app.control.inspect().active_queues()`.

Inspect API (built on remote control; pass node names to limit):

```pycon
>>> i = app.control.inspect()                       # all nodes
>>> i = app.control.inspect(['worker1.example.com'])
>>> i.registered(); i.active(); i.scheduled(); i.reserved()
```

- `registered()` lists task names per worker.
- `active()` entries have name, id, args, kwargs.
- `scheduled()` returns ETA/countdown tasks (eta, priority, request), not periodic tasks.
- `reserved()` are received but not yet executing.
- `celery -A proj inspect stats` (or `Inspect.stats()`) gives statistics.

Other commands: `app.control.broadcast('shutdown')` (optionally `destination=`) gracefully stops workers; `app.control.ping(timeout=0.5)` returns `[{'worker1.example.com': 'pong'}, ...]` and accepts `destination`; `enable_events()` / `disable_events()` toggle event sending for `celery events`.

Gotcha: remote control only works with the RabbitMQ (amqp) and Redis brokers.

## Checked

2026-11-07. Re-read the cited page(s) (workers) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
