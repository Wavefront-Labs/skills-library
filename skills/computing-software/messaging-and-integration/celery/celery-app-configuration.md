---
id: computing-software.messaging-and-integration.celery.celery-app-configuration
name: celery-app-configuration
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, celery-application, config-from-object, config-from-envvar, main-name, lazy-app, censored-config, abstract-tasks]
level: practitioner
status: docs-checked
description: "Create and configure a Celery app: the main module name, config_from_object and config_from_envvar, censored config output, lazy finalization, and custom base task classes."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/application.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: instantiate and configure the `Celery` application correctly.

## Main name
Messages carry only task names; each worker keeps a task registry mapping names to functions. When Celery cannot detect a function's module (module run as a program, or app made in the REPL) names start with `__main__`. Fix by giving the main name: `app = Celery('tasks')`, then `add.name` is `tasks.add` and `app.main` is `'tasks'`.

## Configuration
Read and write via `app.conf`: `app.conf.enable_utc = True`, or `app.conf.update(enable_utc=True, timezone='Europe/London')`. Lookup order: run-time changes, then the config module, then defaults (`celery.app.defaults`); add sources with `add_defaults`.

`config_from_object` accepts a module name (`'celeryconfig'`, `'myproj.config.celery'`, `'myproj.config:CeleryConfig'`), a module object, or a class/object with attributes:
```python
app.config_from_object('celeryconfig')
class Config:
    enable_utc = True
    timezone = 'Europe/London'
app.config_from_object(Config)
```
Gotcha: it resets previously set configuration, so set extra values after calling it. Prefer the module name: a module object must be serialized when the prefork pool is used (pickle errors).

`config_from_envvar` reads the module name from an environment variable:
```python
os.environ.setdefault('CELERY_CONFIG_MODULE', 'celeryconfig')
app.config_from_envvar('CELERY_CONFIG_MODULE')
```
then `CELERY_CONFIG_MODULE="celeryconfig.prod" celery worker -l INFO`.

## Censored output
`app.conf.humanize(with_defaults=False, censored=True)` returns a tabulated string; `app.conf.table(with_defaults=False, censored=True)` a dict. Censoring is a regular expression: a key is hidden if its name contains `API`, `TOKEN`, `KEY`, `SECRET`, `PASS`, `SIGNATURE` or `DATABASE`. Name custom secret settings accordingly.

## Laziness
Creating `Celery()` only creates a logical clock, the task registry, sets itself current (unless `set_as_current` is disabled), and calls `on_init`. Task decorators are deferred (`type(add)` is `celery.local.PromiseProxy`) until used or the app is finalized (`app.finalize()` or accessing `app.tasks`). Tasks are shared between apps unless `shared` is disabled.

## Pass the app around
Avoid `current_app` inside classes; accept an `app` argument. Set `CELERY_TRACE_APP=1` in development to raise if the app chain breaks.

## Base task class
`@app.task(base=DebugTask)` with `class DebugTask(Task)`; if you override `__call__`, call `self.run(*args, **kwargs)` and not `super().__call__`. The default base for an app can be changed with `app.Task = MyBaseTask`. Inherit from the neutral base class `celery.Task` (`from celery import Task`).

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/application.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Removed or reworded: the unsupported claim about celery.task removal (now: inherit from celery.Task).

Method: documentation only; no commands were run.
