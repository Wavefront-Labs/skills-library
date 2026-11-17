---
id: computing-software.messaging-and-integration.celery.routing-message-priorities
name: routing-message-priorities
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, routing, priority, rabbitmq, redis, prefetch, celery-routing-priorities]
level: practitioner
status: docs-checked
description: "Configure Celery task priorities on RabbitMQ and Redis, including the opposite priority direction, x-max-priority, priority_steps, and the prefetch caveat."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/routing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make some tasks run ahead of others, knowing the number means opposite things on RabbitMQ and Redis.

## RabbitMQ (Celery 4.0+)

Higher number means higher priority: `priority=9` is generally delivered ahead of `priority=0`. This is broker ordering, not a strict guarantee about worker processing order. Enable per queue with `x-max-priority`:

```python
from kombu import Exchange, Queue

app.conf.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks',
          queue_arguments={'x-max-priority': 10}),
]
```

Defaults:

```python
app.conf.task_queue_max_priority = 10   # for all queues
app.conf.task_default_priority = 5      # for all tasks
```

## Redis

Priority 0 is the highest and 9 the lowest, the reverse of RabbitMQ. Redis has no notion of priorities itself, so read the page's note before relying on it. Turn it on with a transport option:

```python
app.conf.broker_transport_options = {
    'queue_order_strategy': 'priority',
}
```

Implementation: n lists per queue. Although there are 10 levels (0-9), they consolidate into 4 by default, so a queue named `celery` becomes 4 queues. The highest-priority one keeps the name; others append a separator (default `\x06\x16`) and the priority number:

```python
['celery', 'celery\x06\x163', 'celery\x06\x166', 'celery\x06\x169']
```

For more levels or a different separator set `priority_steps` and `sep`:

```python
app.conf.broker_transport_options = {
    'priority_steps': list(range(10)),
    'sep': ':',
    'queue_order_strategy': 'priority',
}
# ['celery', 'celery:1', ..., 'celery:9']
```

It will never be as good as broker-level priorities and may be approximate at best.

## Per-route and per-call priority

On Redis or RabbitMQ a route can set the queue default: `{'queue': 'video', 'routing_key': 'video.compress', 'priority': 10}`. `task.apply_async(priority=0)` overrides it.

## Prefetch caveat

Because of worker prefetching, tasks submitted together may run out of priority order at first. Disabling prefetching fixes that but can hurt small, fast tasks. In most cases simply reducing `worker_prefetch_multiplier` to 1 is easier and cleaner.

## Checked

2026-11-07. Re-read the cited page(s) (routing) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
