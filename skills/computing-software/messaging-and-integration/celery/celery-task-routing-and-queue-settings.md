---
id: computing-software.messaging-and-integration.celery.celery-task-routing-and-queue-settings
name: celery-task-routing-and-queue-settings
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-routing, celery, task-routes, task-queues, quorum-queues, priority, worker-direct, transient-queue, delivery-mode]
level: practitioner
status: docs-checked
description: "Configure Celery task_queues, task_routes, default queue settings, quorum queues, priorities, worker-direct and transient queues."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
  - https://docs.celeryq.dev/en/stable/userguide/optimizing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Routing and queue settings

Goal: send tasks to the right queues with the exact settings and defaults.

## task_queues and task_routes
- `task_queues` (default `None`): list of `kombu.Queue` the worker consumes. Default is queue/exchange/binding key `celery`, direct exchange. `-Q` overrides it; `-X` excludes queues by name.
- `task_routes` (default `None`): a router or list of routers, consulted in order; the first not returning `None` wins. A router can be a function `(name, args, kwargs, options, task=None, **kwargs)`, a string path, a dict (becomes `MapRoute`) or a list of `(pattern, route)` tuples. Patterns can be globs or `re.compile(...)`:

```python
task_routes = {
    'mytasks.add': 'cpu-bound',
    'feed.tasks.*': 'feeds',
    'video.encode': {'queue': 'video', 'exchange': 'media',
                     'routing_key': 'media.video.encode'},
}
```
A string result is a queue name in `task_queues`; a dict is a custom route. Explicit `apply_async` options win over the router, and values in `task_routes` win over `task_queues` when merged.

## Defaults
- `task_default_queue` `"celery"` (must be in `task_queues`; auto-created if unset), `task_default_exchange` (uses queue name), `task_default_exchange_type` `"direct"`, `task_default_routing_key` (uses queue name).
- `task_default_delivery_mode` `"persistent"` (or `transient`).
- `task_create_missing_queues` (enabled). 5.6+: `task_create_missing_queue_type` (`"classic"` or `"quorum"`) and `task_create_missing_queue_exchange_type` (`None`, or `direct`/`topic`/`fanout`). These apply only to implicitly created queues, not those defined in `task_queues`.
- `task_default_queue_type` (5.5+, `"classic"` or `"quorum"`, RabbitMQ only). Quorum queues require confirm publish: `broker_transport_options = {"confirm_publish": True}`. With `worker_detect_quorum_queues` (default enabled) the worker detects quorum queues and disables global QoS.

## Priorities and direct queues
`task_queue_max_priority` (RabbitMQ, `None`), `task_default_priority` (RabbitMQ/Redis; higher is higher on RabbitMQ, `0` is highest on Redis), `task_inherit_parent_priority` (RabbitMQ, `False`). `worker_direct` (disabled) gives each worker a queue named `w1@example.com.dq` on exchange `C.dq2`: `{'exchange': 'C.dq2', 'routing_key': 'w1@example.com'}`.

## Transient queues for speed
Queues are persistent by default; for tasks that may be lost, use `delivery_mode=1` and `durable=False`:
```python
from kombu import Exchange, Queue
task_queues = (
    Queue('celery', routing_key='celery'),
    Queue('transient', Exchange('transient', delivery_mode=1),
          routing_key='transient', durable=False),
)
task_routes = {'proj.tasks.add': {'queue': 'celery', 'delivery_mode': 'transient'}}
```
Delivery mode 1 is not written to disk; 2 (default) can be. Use `task.apply_async(args, queue='transient')` to target it.

## Checked

2026-11-07. Re-read the cited page(s) (configuration, optimizing) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
