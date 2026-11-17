---
id: computing-software.messaging-and-integration.celery.celery-worker-limits-and-autoscale
name: celery-worker-limits-and-autoscale
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-worker-limits, celery, time-limit, rate-limit, max-tasks-per-child, max-memory-per-child, autoscale, prefork]
level: practitioner
status: docs-checked
description: "Bound Celery task runtime and worker resources: soft/hard time limits, rate limits, max tasks or memory per child, and autoscaling the prefork pool."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/workers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Limit task time, rate, memory and pool size

Goal: stop runaway tasks, throttle task types, recycle leaky processes, and scale the pool.

Time limits (prefork/gevent). Hard `--time-limit` kills the process and replaces it; soft `--soft-time-limit` raises an exception the task can catch before the hard limit. Settings: `task_time_limit`, `task_soft_time_limit`. Client side use `AsyncResult.get(timeout=...)`.

```python
from celery.exceptions import SoftTimeLimitExceeded

@app.task
def mytask():
    try:
        do_work()
    except SoftTimeLimitExceeded:
        clean_up_in_a_hurry()
```

Gotchas: time limits need platforms that support `SIGUSR1`; the gevent pool has no soft limits and will not enforce the hard limit if the task is blocking.

Change at runtime (amqp, redis); only tasks started after the change are affected:

```pycon
>>> app.control.time_limit('tasks.crawl_the_web', soft=60, hard=120, reply=True)
[{'worker1.example.com': {'ok': 'time limits set successfully'}}]
```

Rate limits at runtime:

```pycon
>>> app.control.rate_limit('myapp.mytask', '200/m')
>>> app.control.rate_limit('myapp.mytask', '200/m', destination=['celery@worker1.example.com'])
```

No destination means all workers. It has no effect on workers with `worker_disable_rate_limits` enabled.

Recycling (prefork), useful for leaks you cannot fix such as closed-source C extensions: `--max-tasks-per-child` or `worker_max_tasks_per_child`; `--max-memory-per-child` (resident memory, since 4.0) or `worker_max_memory_per_child`.

Autoscale (prefork, gevent): `--autoscale=10,3` means max 10, min 3 processes. It grows when there is work and shrinks after a keepalive of 30 seconds since the last task was accepted for immediate execution or the pool grew; ETA/countdown and rate-limited tasks do not reset the timer. Change the period with env `AUTOSCALE_KEEPALIVE`. For custom rules (load average, free memory) subclass `celery.worker.autoscale.Autoscaler` and set `worker_autoscaler`.

## Checked

2026-11-07. Re-read the cited page(s) (workers) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
