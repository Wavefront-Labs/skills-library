---
id: computing-software.messaging-and-integration.celery.signals-worker-logging-lifecycle
name: signals-worker-logging-lifecycle
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, signals, worker, logging, celeryd-init, worker-process-init, setup-logging, celery-signals-worker]
level: practitioner
status: docs-checked
description: "Use Celery worker, beat, logging and command signals: celeryd_init, worker_process_init sender and 4 second limit, setup_logging, and user_preload_options."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/signals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure workers and logging at startup and clean up at shutdown.

## Startup order and per-worker config

- `celeryd_init`: first signal when `celery worker` starts. Sender is the worker hostname. Arguments: `sender`, `instance`, `conf`, `options` (CLI options including defaults).

```python
@celeryd_init.connect(sender='worker12@example.com')
def configure_worker12(conf=None, **kwargs):
    conf.task_default_rate_limit = '10/m'
```

Omit the sender to cover several workers and test `sender` inside.
- `celeryd_after_setup`: after setup but before run; `-Q` queues are enabled and logging is set up. Example adds a per-worker direct queue: `instance.app.amqp.queues.select_add('{0}.dq'.format(sender))`. Arguments: `sender`, `instance`, `conf`. Only `app` and `hostname` are set on the instance so far.
- `worker_init` (before start), `worker_ready` (ready for work), `heartbeat_sent` (sender is the `Heart`), `worker_shutting_down` (`sig`, `how` warm or cold, `exitcode`), `worker_shutdown`.
- `import_modules`: sent when a program asks for `include`/`imports` modules; sender is the app.

## Pool processes

- `worker_before_create_process`: parent process, just before a prefork child is created; use it to clean instances that fork badly.
- `worker_process_init`: in each prefork child and once in the main process for a solo pool; threads, gevent and eventlet pools don't send it. Sender is the worker node name (the `-n` value), so `@worker_process_init.connect(sender='db@example.com')` targets one worker. Before 5.7 the sender was always None; a solo pool created outside a worker still sends None. Handlers must not block more than 4 seconds or the process is killed as having failed to start.
- `worker_process_shutdown`: prefork children just before exit; arguments `pid`, `exitcode`. Not guaranteed to run, like a `finally` block.
- Eventlet: `eventlet_pool_started`, `eventlet_pool_preshutdown`, `eventlet_pool_postshutdown`, `eventlet_pool_apply` (`target`, `args`, `kwargs`).

## Beat

`beat_init` fires when beat starts (standalone or embedded); `beat_embedded_init` also fires when embedded. Sender is `celery.beat.Service`.

## Logging

- `setup_logging`: if connected, Celery doesn't configure loggers, so you fully override. Arguments `loglevel`, `logfile`, `format`, `colorize`.
- `after_setup_logger` (global loggers) and `after_setup_task_logger` (each task logger) augment Celery's config; they also get `logger`.

## Command line

`user_preload_options` fires after preload options are parsed (arguments `app`, `options`). Add options via click:

```python
app.user_options['preload'].add(Option(
    ('--monitoring',), is_flag=True, help='Enable our external monitoring utility'))

@signals.user_preload_options.connect
def handle_preload_options(options, **kwargs):
    if options.get('monitoring'):
        enable_monitoring()
```

## Checked

2026-11-07. Re-read the cited page(s) (signals) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
