---
id: computing-software.messaging-and-integration.celery.celery-call-tasks-apply-async
name: celery-call-tasks-apply-async
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, celery-calling, apply-async, delay, countdown, eta, expires, routing, ignore-result]
level: practitioner
status: docs-checked
description: "Call Celery tasks with delay and apply_async: countdown, eta, expires, queue routing, priority, ignore_result, and the warnings about distant ETAs and RabbitMQ consumer_timeout."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/calling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: send a task message with the right execution options.

## Three ways to call
- `T.delay(*args, **kwargs)` is a shortcut for `apply_async(args, kwargs)` and takes no execution options.
- `T.apply_async(args=[a, b], kwargs={'k': 'v'}, ...)` takes options.
- `T(2, 2)` (`__call__`) runs in the current process; no message is sent.
- By name: `app.send_task('proj.tasks.add', (2, 2), link_error=on_error.s())` (the page uses it where the task is referenced by name).

## Examples from the page
```python
add.apply_async((2, 2), countdown=3)                 # at least 3 seconds
add.apply_async((2, 2), eta=tomorrow)                # tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
add.apply_async((10, 10), expires=60)                # expires 60 s after publish
add.apply_async((2, 2), retry=False)                 # disable publish retry
```

## ETA and countdown
`countdown` is seconds; `eta` must be a `datetime` (timezone-aware, e.g. `datetime.now(timezone.utc) + timedelta(days=1)`). The task runs some time after the ETA, not exactly at it. Countdown and numeric `expires` use elapsed seconds across DST changes (86400 is 24 hours). A task rate limit applies after the ETA.

Warnings:
- Tasks with `eta`/`countdown` are fetched immediately and held in worker memory, which may grow RAM use. They are not acked until execution starts; with Redis the task is redelivered if the countdown exceeds `visibility_timeout`. Keep values to several minutes; for longer use periodic tasks (for example `django-celery-beat`).
- RabbitMQ 3.8.15+ has a default `consumer_timeout` of 15 minutes (30 minutes since 3.8.17). A longer countdown closes the channel with `PRECONDITION_FAILED` (`consumer ack timed out`). Set `consumer_timeout` in `rabbitmq.conf` at or above the countdown.

## Expiration
`expires` is seconds after publish or a `datetime`. An expired task received by a worker is marked `REVOKED` (`TaskRevokedError`).

## Routing and priority
`add.apply_async(queue='priority.high')`, then run a worker with `celery -A proj worker -l INFO -Q celery,priority.high`. Prefer `task_routes` over hard-coded queue names. Advanced: `exchange`, `routing_key`, and `priority` (0 to 255, 255 highest; supported by RabbitMQ; Redis reversed, 0 highest).

## Results option
`apply_async(..., ignore_result=True)` skips storage; `False` stores. Since 5.7 `send_task` respects the task's `ignore_result` when omitted; pass `ignore_result=False` to fetch a result from such a task, otherwise `get()` waits until its timeout (or forever). To store the periodic task name, pass `headers={"periodic_task_name": "task_name"}`.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/calling.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Removed or reworded: the cheat-sheet block (task_id example, countdown=60/expires=120, eta+10s) and the task_id option, none on the page; replaced by the page examples.

Method: documentation only; no commands were run.
