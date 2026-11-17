---
id: computing-software.messaging-and-integration.celery.celery-callbacks-and-errbacks
name: celery-callbacks-and-errbacks
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, celery-calling, link, link-error, errback, callback, on-message, allow-join-result]
level: practitioner
status: docs-checked
description: "Attach Celery callbacks and error callbacks with link and link_error, understand when errbacks are called directly vs as tasks, and stream states with on_message."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/calling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run follow-up tasks on success or failure, and watch progress.

## Callback
```python
add.apply_async((2, 2), link=add.s(16))   # (2 + 2) + 16 = 20
```
The callback receives the parent result (4) as a partial argument, so the callback adds 16 to it. `link` and `link_error` both accept lists; callbacks/errbacks are called in order, all with the parent's return value:
```python
add.apply_async((2, 2), link=[add.s(16), other_task.s()])
```

## Errback
```python
@app.task
def error_handler(request, exc, traceback):
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(request.id, exc, traceback))

add.apply_async((2, 2), link_error=error_handler.s())
```
Normally the worker calls the errback function directly so the raw request, exception and traceback can be passed. That direct call happens only when the errback is a registered `@app.task` function, is not `bind=True`, and accepts more than one argument. If it takes a single argument, is `bind=True`, or is not registered in the worker handling the failure, Celery applies it as a task, passing only the failed task id. Use the single-argument form when the failing task was sent with `send_task`, and fetch the result inside with `allow_join_result`:
```python
from celery.result import allow_join_result

@app.task
def on_error(task_id):
    with allow_join_result():
        result = app.AsyncResult(task_id)
        exc = result.get(propagate=False)
        print('Task {0} raised exception: {1!r}'.format(task_id, exc))

app.send_task('proj.tasks.add', (2, 2), link_error=on_error.s())
```
For chords there are separate error handling strategies (see the chord errors guide).

## on_message
Catch every state change while waiting:
```python
@app.task(bind=True)
def hello(self, a, b):
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 50})
    return 'hello world: %i' % (a+b)

def on_raw_message(body):
    print(body)

r = hello.apply_async(args=(1, 1))
print(r.get(on_message=on_raw_message, propagate=False))
```
Each message prints like `{'task_id': ..., 'result': {'progress': 50}, 'children': [], 'status': 'PROGRESS', 'traceback': None}`, ending with `SUCCESS`.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/calling.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Removed or reworded: the claim that link is an internal primitive and chains are preferred.

Method: documentation only; no commands were run.
