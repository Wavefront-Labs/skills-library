---
id: computing-software.messaging-and-integration.celery.celery-worker-custom-control-commands
name: celery-worker-custom-control-commands
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-worker-queues, celery, control-command, inspect-command, remote-control, imports, prefetch]
level: practitioner
status: docs-checked
description: "Write custom Celery remote control and inspect commands with control_command and inspect_command and call them from celery control or inspect."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/workers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Write your own remote control commands

Goal: add a worker-side command callable with `celery control` or `celery inspect`.

Two kinds:
- Inspect command: no side effects, usually returns a value found in the worker (registered tasks, active tasks).
- Control command: performs side effects, such as adding a new queue to consume from.

Commands register in the control panel and take a `state` object first, then any arguments sent with the command. `state` holds the worker's `app`, `hostname` and `consumer`, so `state.consumer` is the active Consumer.

Control command that raises the prefetch count:

```python
from celery.worker.control import control_command

@control_command(
    args=[('n', int)],
    signature='[N=1]',  # <- used for help on the command-line.
)
def increase_prefetch_count(state, n=1):
    state.consumer.qos.increment_eventually(n)
    return {'ok': 'prefetch count incremented'}
```

Put this code in a module the worker imports: the module where your app is defined, or add the module to the `imports` setting. Restart the worker so the command is registered, then call it:

```console
$ celery -A proj control increase_prefetch_count 3
```

Inspect command reading the current value:

```python
from celery.worker.control import inspect_command

@inspect_command()
def current_prefetch_count(state):
    return {'prefetch_count': state.consumer.qos.value}
```

After restarting the worker:

```console
$ celery -A proj inspect current_prefetch_count
```

Gotchas: the command is unavailable until the worker restarts with the module imported. Remote control needs an amqp or redis broker. Replies must arrive within the client timeout (one second by default; with the solo pool an executing task blocks waiting control commands).

## Checked

2026-11-07. Re-read the cited page(s) (workers) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Changed: reworded the solo pool remark to the page wording.

Method: documentation only; no commands were run.
