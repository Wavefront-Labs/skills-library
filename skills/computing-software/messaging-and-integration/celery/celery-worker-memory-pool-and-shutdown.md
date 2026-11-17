---
id: computing-software.messaging-and-integration.celery.celery-worker-memory-pool-and-shutdown
name: celery-worker-memory-pool-and-shutdown
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-worker-memory, celery, max-tasks-per-child, max-memory-per-child, spawn, fork, soft-shutdown, worker-pool, memory-leak]
level: practitioner
status: docs-checked
description: "Control Celery prefork memory growth, choose fork or spawn start method, and configure soft shutdown and worker pool settings."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
  - https://docs.celeryq.dev/en/stable/userguide/optimizing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Worker memory, pool start method and shutdown

Goal: keep prefork workers healthy and shut them down gracefully.

## Memory
First check whether the Celery master process keeps growing after start-up; if so it may be a leak to report. If only child processes grow, the issue is in your task. Python memory has a high watermark and is not returned to the OS until the child stops; one big task can raise a child permanently, so chunk work.

- `worker_max_tasks_per_child` (default no limit): replace a pool process after N tasks.
- `worker_max_memory_per_child` (default no limit, int in kilobytes): resident memory limit; if one task exceeds it, the task completes and the worker is replaced afterwards. `worker_max_memory_per_child = 12288  # 12 MB`.
Do not set these too low: with `worker_max_tasks_per_child = 1` and a 1 second child start-up, a child handles at most 60 tasks a minute. The same happens if tasks always exceed the memory limit.

## Fork vs spawn (5.7+)
`worker_pool_start_method` default `"fork"`; only for prefork (ignored by eventlet, gevent and solo). Fork is fast and shares imported modules copy-on-write, but is unsafe when the parent has started threads or uses fork-unsafe C extensions (gRPC, psycopg, CUDA): children can hang, deadlock or corrupt state, especially after a hard `task_time_limit` kill replaces a child. Fix:

```python
worker_pool_start_method = "spawn"
```
Costs: slower start-up, more memory, picklable app and task arguments, entry point guarded by `if __name__ == '__main__':`. A replacement child must finish importing your app within `worker_proc_alive_timeout` (default 4.0 s), so raise it for slow imports.

## Pool settings
- `worker_pool` default `"prefork"`. Never select eventlet or gevent with this setting; use `-P` so monkey patches are applied in time.
- `worker_pool_restarts` (disabled): enables the `pool_restart` remote control command.
- `worker_autoscaler` (`celery.worker.autoscale:Autoscaler`), `worker_consumer`, `worker_timer`.
- `worker_timer_precision` (1.0 s): ETA scheduler max sleep; `0.1` for near-millisecond precision.
- `worker_state_db` (`None`): persistent state file (revoked tasks); suffix `.db` may be appended. `worker_enable_remote_control` default enabled.

## Soft shutdown (5.5+)
`worker_soft_shutdown_timeout` (default 0.0 = effectively disabled): wait this long before cold shutdown begins; also applies to a cold shutdown without a prior warm one. Docs suggest 10, 30 or 60 seconds; too high risks the host sending KILL. It is skipped when no tasks are running unless `worker_enable_soft_shutdown_on_idle` (default False) is on; enable that when ETA tasks are waiting, otherwise they may fail to be re-queued during teardown.

## Checked

2026-11-07. Re-read the cited page(s) (configuration, optimizing) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
