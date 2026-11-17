---
id: computing-software.messaging-and-integration.celery.celery-define-tasks
name: celery-define-tasks
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, celery-define-tasks, task-decorator, shared-task, bound-tasks, task-names, argument-checking, python]
level: practitioner
status: docs-checked
description: "Define Celery tasks with the app.task and shared_task decorators, bind=True, base classes, explicit or custom-generated names, and argument checking."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/tasks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: turn a callable into a uniquely named Celery task and control how it is named and called.

## Decorators
- `@app.task` on your `Celery` app instance; options go in as arguments, e.g. `@app.task(serializer='json')`.
- Django or library code: `from celery import shared_task`, then `@shared_task`.
- Combined with other decorators the task decorator must be applied last, which means it is first in the list:
```python
@app.task
@decorator2
@decorator1
def add(x, y): return x + y
```

## Bound tasks
`@app.task(bind=True)` makes the first argument `self` (the task instance). Needed for `self.retry()`, `self.request`, and custom base-class functionality.
```python
@app.task(bind=True)
def add(self, x, y):
    logger.info(self.request.id)
```

## Base class
`@app.task(base=MyTask)` where `class MyTask(celery.Task)` can define handlers such as `on_failure(self, exc, task_id, args, kwargs, einfo)`.

## Names
Every task needs a unique name. Default = module name + function name (`tasks.add` for `add` in `tasks.py`). Set explicitly with `@app.task(name='sum-of-two-numbers')`; best practice is to use the module name as a namespace. Read it with `add.name`. Use the `inspect registered` worker command to see registered names.

Change automatic naming (new in 4.0) by overriding `gen_task_name` on a `Celery` subclass:
```python
class MyCelery(Celery):
    def gen_task_name(self, name, module):
        if module.endswith('.tasks'):
            module = module[:-6]
        return super().gen_task_name(name, module)
app = MyCelery('main')
```
Gotcha: `gen_task_name` must be a pure function (same input, same output).

## Argument checking (since 4.0)
Calling `add.delay(8)` with a missing argument raises `TypeError` on the caller, like a normal function call. Disable per task with `@app.task(typing=False)`; then the call is accepted locally but the receiving worker raises an error.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/tasks.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
