---
id: computing-software.messaging-and-integration.celery.celery-next-steps-calling-canvas-routing
name: celery-next-steps-calling-canvas-routing
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-next-steps, celery, delay, apply-async, signatures, canvas, task-routes, multi]
level: intro
status: docs-checked
description: "Celery next steps: celery multi, --app lookup order, delay vs apply_async, task states and get(propagate), signatures, group chain chord, routing and timezone."
sources:
  - https://docs.celeryq.dev/en/stable/getting-started/next-steps.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Next steps: calling tasks, canvas, routing, multi

Goal: use the core Celery calling and workflow API beyond the first-steps tutorial.

`--app` takes `module.path:attribute`. With a bare package `proj` it tries, in order: `proj.app`, `proj.celery`, any Celery attribute in `proj`, then `proj.celery.app`, `proj.celery.celery`, any Celery attribute in `proj.celery`.

`celery multi start w1 -A proj -l INFO` starts background workers; `restart` and `stop` follow (stop is asynchronous; `stopwait` waits for running tasks). multi stores no worker info, so restart with the same arguments; stopping needs the same pidfile and logfile arguments. Use dedicated directories: `--pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log`. Per-node options: `celery multi start 10 -A proj -l INFO -Q:1-3 images,video -Q:4,5 data -Q default -L:4,5 debug`.

Calling API: `add.delay(2, 2)` is a star-args shortcut for `add.apply_async((2, 2))`, which takes options: `add.apply_async((2, 2), queue='lopri', countdown=10)`. `add(2, 2)` runs locally with no message. Each call has a UUID task id and returns an `AsyncResult`; results are disabled by default, so configure a backend before `res.get(timeout=1)`. `get()` propagates errors; `res.get(propagate=False)` returns the exception instead, then use `res.failed()`, `res.successful()`, `res.state` ('FAILURE'). States: `PENDING -> STARTED -> SUCCESS`; STARTED is recorded only with `task_track_started` or `@task(track_started=True)`; PENDING is the default for any unknown id. Retried twice: `PENDING -> STARTED -> RETRY -> STARTED -> RETRY -> STARTED -> SUCCESS`.

Signatures: `add.signature((2, 2), countdown=10)`. `.s()` takes only task args (`add.s(2, 2, countdown=10)` would pass `countdown` to the task); use `add.s(2, 2).set(countdown=10)`. Partials: `s2 = add.s(2); s2.delay(8)` gives `add(8, 2)`; new kwargs merge over existing ones.

Canvas:
- `group(add.s(i, i) for i in range(10))().get()`; partial `group(add.s(i) ...)(10)`.
- `chain(add.s(4, 4) | mul.s(8))().get()` is 64; same as `(add.s(4, 4) | mul.s(8))()`.
- `chord((add.s(i, i) for i in range(10)), xsum.s())().get()` is 90; a group chained to a task becomes a chord automatically.
Result retrieval needs a result backend.

Routing: `app.conf.update(task_routes={'proj.tasks.add': {'queue': 'hipri'}})` or `queue=` at call time; consume with `celery -A proj worker -Q hipri,celery` (default queue is `celery`; order gives equal weight).

Timezone: internal times and messages are UTC; set `app.conf.timezone = 'Europe/London'` for local conversion. The default config favours fair scheduling over throughput; see the Optimizing guide.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (getting-started/next-steps.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
