---
id: computing-software.messaging-and-integration.celery.canvas-chords-error-handling
name: canvas-chords-error-handling
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, canvas, chord, chorderror, result-backend, ignore-result, celery-canvas-chords]
level: practitioner
status: docs-checked
description: "Build Celery chords, handle ChordError and chord errbacks, avoid ignore_result and result_expires pitfalls, and know how the chord join step works per backend."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/canvas.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run a callback (body) after every task in a header group has finished.

```python
from celery import chord
chord(add.s(i, i) for i in range(100))(tsum.s()).get()   # 9900
# broken down
callback = tsum.s()
header = [add.s(i, i) for i in range(100)]
result = chord(header)(callback)
```

The callback receives the list of header return values. The id returned by the chord is the callback's. The page warns that the sync step is costly (a chord is slower than the Python equivalent), so avoid chords where you can, and never have a task wait on other tasks. Use `.si` on the body when the group results should not be passed: `chord((import_contact.s(c) for c in contacts), notify_complete.si(import_id)).apply_async()`.

`countdown`/`eta` delay the header tasks only, not the body or the `chord_unlock` retry interval.

## Requirements

- A result backend is required; chords are not supported with the RPC backend.
- If `task_ignore_result` is True, define chord tasks with `ignore_result=False` (`@app.task(ignore_result=False)` or `class MyTask(Task): ignore_result = False`).
- Header tasks running longer than `result_expires` can lose bookkeeping so the body never runs; set `result_chord_expires`.
- Redis needs server 2.2 or newer. With Redis, an overridden `Task.after_return` must call `super().after_return(*args, **kwargs)` or the callback is not applied.

## Errors

If a header task raises, the callback result goes to failure with `ChordError` (message includes the failing task id and exception; `result.traceback` has the original). The other header tasks still run, and only the first failure in time is reported.

```python
@app.task
def on_chord_error(request, exc, traceback):
    print('Task {0!r} raised error: {1!r}'.format(request.id, exc))

c = (group(add.s(i, i) for i in range(10)) |
     tsum.s().on_error(on_chord_error.s())).delay()
```

An unbound errback taking `(request, exc, traceback)` gets those three args. A single-argument errback, or one declared `@app.task(bind=True)`, is dispatched as a task and receives the failed chord callback's id.

A linked errback fires once on body failure. Setting `task_allow_error_cb_on_chord_header` also invokes it for failing header tasks. Since 5.7 `chord.apply_async()` accepts `link` and `link_error`; that setting does not apply to `link_error`.

## Join implementation

By default a recurring `unlock_chord` task polls `group.ready()` every second. Redis, Memcached and DynamoDB instead increment a counter per finished header task and apply the callback when it is reached.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/canvas.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
