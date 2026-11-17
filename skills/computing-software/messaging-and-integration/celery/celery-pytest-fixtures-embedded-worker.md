---
id: computing-software.messaging-and-integration.celery.celery-pytest-fixtures-embedded-worker
name: celery-pytest-fixtures-embedded-worker
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-testing, celery, pytest, fixtures, celery-worker, celery-config, conftest, embedded-worker]
level: practitioner
status: docs-checked
description: "Enable the Celery pytest plugin and use celery_app, celery_worker, celery_config, celery_includes and session fixtures to run an embedded worker in tests."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/testing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Celery pytest plugin: fixtures and embedded worker

Goal: run integration tests against an embedded worker with test config.

The plugin ships disabled (since 4.0). Enable by `pip install celery[pytest]`, or env `PYTEST_PLUGINS=celery.contrib.pytest`, or `pytest_plugins = ("celery.contrib.pytest", )` in the root `conftest.py`.

Per-test config with the `celery` mark (function or class):

```python
@pytest.mark.celery(result_backend='redis://')
def test_something(): ...
```

Function-scope fixtures:
- `celery_app`: test app. `celery_worker`: embeds a live worker in a separate thread, shut down when the test returns; it waits up to 10 seconds for outstanding tasks and raises if exceeded (change with `shutdown_timeout` in the dict from `celery_worker_parameters`).

```python
def test_create_task(celery_app, celery_worker):
    @celery_app.task
    def mul(x, y):
        return x * y

    celery_worker.reload()
    assert mul.delay(4, 4).get(timeout=10) == 16
```

The embedded worker only runs tasks registered on the `celery_app` fixture: use `@shared_task`, define on `celery_app`, or register on it before `celery_worker.reload()`. A task on a separately created `Celery()` app is not found.

Heartbeats are off by default (no `worker-online`/`worker-offline`/`worker-heartbeat` events); return `{"without_heartbeat": False}` from `celery_worker_parameters` to enable.

Session-scope override fixtures (define in conftest.py, `scope='session'`):
- `celery_config`: dict for `celery_app` and `celery_session_app`, e.g. `{'broker_url': 'amqp://', 'result_backend': 'rpc'}`.
- `celery_parameters`: `Celery.__init__` arguments, e.g. `{'task_cls': ..., 'strict_typing': False}`.
- `celery_worker_parameters`: passed to `WorkController`, e.g. `{'queues': ('high-prio', 'low-prio'), 'exclude_queues': ('celery')}`.
- `celery_enable_logging`: return True to log in embedded workers.
- `celery_includes`: modules to import at worker start, e.g. `['proj.tests.tasks', 'proj.tests.celery_signal_handlers']`.
- `celery_worker_pool`: e.g. `'prefork'`. You cannot use gevent/eventlet pools unless the whole suite runs monkeypatched.
- `celery_session_worker`: worker living for the whole session (mixing session and ephemeral workers is probably a bad idea); `celery_session_app` is the app for other session-scoped fixtures.
- `use_celery_app_trap`: return True to raise when code falls back to the default or current app; mark tests that need it with `@pytest.mark.usefixtures('depends_on_current_app')`.

## Checked

2026-11-07. Re-read the cited page(s) (testing) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. Code snippet and include files were not opened separately.

Changed: reworded the celery_session_app description.

Method: documentation only; no commands were run.
