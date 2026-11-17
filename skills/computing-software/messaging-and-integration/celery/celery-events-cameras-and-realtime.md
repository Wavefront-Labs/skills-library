---
id: computing-software.messaging-and-integration.celery.celery-events-cameras-and-realtime
name: celery-events-cameras-and-realtime
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-events, celery, snapshots, camera, receiver, event-state, task-failed, heartbeat]
level: practitioner
status: docs-checked
description: "Consume Celery events: snapshot cameras with celery events -c, real-time Receiver handlers, State, the task and worker event reference, mailbox options."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/monitoring.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consume Celery events with cameras and receivers

Goal: capture worker/task events periodically (camera) or in real time (receiver).

Workers emit events when enabled (`celery -A proj control enable_events`). Even one worker produces many, so snapshot state periodically instead of storing everything. Define a `Polaroid` subclass:

```python
from celery.events.snapshot import Polaroid

class DumpCam(Polaroid):
    clear_after = True  # clear after flush (incl, state.event_count).

    def on_shutter(self, state):
        if not state.event_count:
            return
        print('Total: {0.event_count} events, {0.task_count} tasks'.format(state))
```

Run it: `celery -A proj events -c myapp.DumpCam --frequency=2.0`. Programmatically:

```python
state = app.events.State()
with app.connection() as connection:
    recv = app.events.Receiver(connection, handlers={'*': state.event})
    with DumpCam(state, freq=freq):
        recv.capture(limit=None, timeout=None)
```

Real-time processing needs a Receiver, handlers per event type (or `'*'` catch-all), and optionally `app.events.State()`, which tracks tasks and workers, checks heartbeats, merges event fields and syncs timestamps. The task name is sent only with `task-received`, so call `state.event(event)` then `state.tasks.get(event['uuid'])`:

```python
recv = app.events.Receiver(connection, handlers={
    'task-failed': announce_failed_tasks, '*': state.event})
recv.capture(limit=None, timeout=None, wakeup=True)
```

`wakeup=True` makes all workers send a heartbeat so you see them immediately. `celery -A proj events --dump` prints events to stdout.

Task events: `task-sent` (needs `task_send_sent_event`), `task-received`, `task-started`, `task-succeeded(uuid, result, runtime, hostname, timestamp)`, `task-failed`, `task-rejected(uuid, requeue)`, `task-revoked(uuid, terminated, signum, expired)` (may come from several workers), `task-retried`. Worker events: `worker-online`, `worker-heartbeat` (active, processed; sent every minute, offline if none in 2 minutes), `worker-offline`.

Mailbox (Kombu 5.6.0+): `durable` defaults to False, `exclusive` to True; setting both True raises an error. See `event_queue_durable` and `event_queue_exclusive`.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/monitoring.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Removed or reworded: the worker -E option (not on the monitoring page).

Method: documentation only; no commands were run.
