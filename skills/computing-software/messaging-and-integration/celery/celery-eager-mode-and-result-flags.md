---
id: computing-software.messaging-and-integration.celery.celery-eager-mode-and-result-flags
name: celery-eager-mode-and-result-flags
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-eager, celery, task-always-eager, testing, ignore-result, track-started, tblib, task-eager-propagates]
level: practitioner
status: docs-checked
description: "Run Celery tasks locally with task_always_eager, propagate exceptions, store eager results, and control which results and errors are stored."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Eager execution and result-storage flags

Goal: run tasks in-process and decide what is stored in the result backend.

## Eager settings
- `task_always_eager` (default disabled): when `True`, all tasks run locally, blocking until the task returns. `apply_async()` and `Task.delay()` return an `EagerResult`, which emulates `AsyncResult` but is already evaluated. Tasks are executed locally instead of being sent to the queue.
- `task_eager_propagates` (default disabled): when `True`, eagerly executed tasks (via `task.apply()` or `task_always_eager`) propagate exceptions. Same as always running `apply()` with `throw=True`.
- `task_store_eager_result` (5.1+, default disabled): saves eager results to the backend only if `task_always_eager` is `True` and `task_ignore_result` is `False`. By default, even with those two conditions, the result is not saved.

```python
task_always_eager = True
task_eager_propagates = True
```

With Django namespace use `CELERY_TASK_ALWAYS_EAGER = True`.

## Result and state flags
- `task_ignore_result` (default disabled): do not store return values (tombstones). To still store errors, set `task_store_errors_even_if_ignored` (default disabled; the worker then stores all task errors even when `Task.ignore_result` is on).
- `task_track_started` (default disabled): report a `started` state when a worker begins executing. Normally a task is only pending, finished or waiting to be retried; `started` helps for long-running tasks.
- `task_remote_tracebacks` (default disabled): results include the worker stack when errors are re-raised. Requires `tblib`: `pip install celery[tblib]`.
- `task_default_rate_limit` (default no limit): global default rate limit for tasks without a custom one. `worker_disable_rate_limits` disables all rate limits even when tasks set explicit ones.
- `task_repr_maxlevels` (5.7+, default 3): maximum nesting depth for `argsrepr`/`kwargsrepr`; deeper containers show as `{...}` / `[...]`; `0` or `None` means no limit.

## task_annotations
Rewrite any task attribute from config, as a dict or list of annotation objects:

```python
task_annotations = {'tasks.add': {'rate_limit': '10/s'}}
task_annotations = {'*': {'rate_limit': '10/s'}}   # all tasks
task_annotations = {'*': {'on_failure': my_on_failure}}
```

An object with an `annotate(self, task)` method can return a dict of attributes for matching tasks.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/configuration.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
