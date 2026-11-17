---
id: computing-software.messaging-and-integration.celery.celery-worker-shutdown-and-restart
name: celery-worker-shutdown-and-restart
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-worker-shutdown, celery, worker, signals, sigterm, soft-shutdown, restart, broker-reconnect]
level: practitioner
status: docs-checked
description: "Shut down and restart Celery workers safely: warm, soft, cold and hard stages, signals, REMAP_SIGTERM, HUP, and broker reconnect behaviour."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/workers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shut down and restart Celery workers safely

Goal: stop a worker without losing tasks, and know what each signal does.

Use `TERM` for shutdown. Main process signals: `TERM` warm shutdown (wait for tasks), `QUIT` cold shutdown (terminate ASAP), `USR1` dump tracebacks of all active threads, `USR2` remote debug (`celery.contrib.rdb`). `INT` (Ctrl-C) always advances to the next stage.

Stages:
- Warm: on `TERM` (or first Ctrl-C) the worker finishes executing tasks; extra `TERM` is ignored; the next `INT` moves on. Since 5.6 prefork keeps broker heartbeats during warm shutdown so tasks can complete. Since 5.7 `--pool threads` cancels pending futures (`cancel_futures=True`), so only running tasks finish.
- Soft (since 5.5): a time-limited warm shutdown before cold. Set `worker_soft_shutdown_timeout` to a positive float (disabled by default). It is skipped if no tasks run; also enable `worker_enable_soft_shutdown_on_idle` to force it. With ETA tasks reserved, enable the idle setting or tasks may be lost in the cold shutdown.
- Cold: `QUIT` stops running tasks and terminates. If env `REMAP_SIGTERM=SIGQUIT`, `TERM` does a cold shutdown. In prefork it raises `SystemExit` inside a signal handler, which can interrupt Python at any bytecode, so do not rely on atomicity (the page names Django `on_commit` as a construct to avoid, and suggests a transactional outbox or precondition checks in downstream tasks).
- Hard (since 5.5): repeated Ctrl-C raises `WorkerTerminate`; for local/debug use. The log "Restoring 1 unacknowledged message(s)" is misleading, restoration is not guaranteed.

`KILL` loses running tasks unless `acks_late` is set, and the worker cannot reap children; clean up with `pkill -9 -f 'celery worker'`. Since 5.2 on Linux children get KILL after worker termination via `PR_SET_PDEATHSIG`.

Restart: send `TERM` and start a new instance. For development: `celery multi start 1 -A proj -l INFO -c4 --pidfile=/var/run/celery/%n.pid` then `celery multi restart 1 --pidfile=/var/run/celery/%n.pid`. `kill -HUP $pid` restarts in place but only works when daemonized, is disabled on macOS and is not recommended in production.

Broker loss (since 5.3): the worker retries connecting after the first loss unless `broker_connection_retry_on_startup` is False; `broker_connection_retry` governs later reconnects. `worker_cancel_long_running_tasks_on_connection_loss=True` (since 5.1) also cancels running tasks. Prefetch is reduced by running tasks times `worker_prefetch_multiplier` and restored gradually as pre-loss tasks complete; disable with `worker_enable_prefetch_count_reduction=False`.

## Checked

2026-11-07. Re-read the cited page(s) (workers) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
