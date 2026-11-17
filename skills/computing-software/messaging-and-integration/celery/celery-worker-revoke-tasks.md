---
id: computing-software.messaging-and-integration.celery.celery-worker-revoke-tasks
name: celery-worker-revoke-tasks
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-worker-revoke, celery, revoke, terminate, statedb, stamped-headers, remote-control, broadcast]
level: practitioner
status: docs-checked
description: "Revoke Celery tasks by id or stamped header, terminate stuck processes, and persist revokes across restarts with --statedb; includes broadcast usage."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/workers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Revoke Celery tasks and use broadcast

Goal: stop queued or running tasks cluster-wide, and keep revokes across restarts.

Remote control uses a high-priority broadcast queue; broker support is amqp and redis. Replies are collected within a timeout that defaults to one second (a missing reply may just be latency); with a destination, max replies is the number of destination hosts. The solo pool supports remote control, but an executing task blocks any waiting control command, so raise the client timeout. Raw API:

```pycon
>>> app.control.broadcast('rate_limit', {'task_name': 'myapp.mytask', 'rate_limit': '200/m'},
...                       reply=True, destination=['worker1@example.com'])
```

Without `reply=True` it is fire-and-forget.

Revoke:

```pycon
>>> result.revoke()
>>> app.control.revoke('d9078da5-9915-40a0-bfa1-392c7bde42ed')
>>> app.control.revoke(task_id, terminate=True, signal='SIGKILL')
>>> app.control.revoke([id1, id2, id3])
```

CLI: `celery -A proj control revoke <task_id>`. A revoked task is skipped; a running one is only killed with `terminate`, which kills the pool process (default signal `TERM`, any uppercase name from the `signal` module). `terminate` is a last resort for administrators: that process may already be on another task, so never call it programmatically. Without `task_track_started` a running task shows PENDING, so it is marked REVOKED and still stores its result. Since 5.6 the result backend is updated to REVOKED immediately.

Memory: env `CELERY_WORKER_REVOKES_MAX` (default 50000), after which revokes expire in `CELERY_WORKER_REVOKE_EXPIRES` (10800 s); `CELERY_WORKER_SUCCESSFUL_MAX` (1000) and `CELERY_WORKER_SUCCESSFUL_EXPIRES` (10800) for successful tasks.

Persistence: revokes live in memory and starting workers sync from the cluster; if all workers restart they vanish. Pass `--statedb=/var/run/celery/worker.state`; under multi use `--statedb=/var/run/celery/%n.state` for one file per node.

By stamped header:

```pycon
>>> app.control.revoke_by_stamped_headers({'header_A': 'value_1', 'header_B': ['value_2', 'value_3']})
```

CLI: `celery -A proj control revoke_by_stamped_headers key=value --terminate --signal=SIGKILL`. Revoked headers are not persistent across restarts, and with high concurrency plus terminate it may perform poorly (it iterates the running tasks).

## Checked

2026-11-07. Re-read the cited page(s) (workers) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Changed: reworded the solo pool remark to the page wording (an executing task blocks control commands).

Method: documentation only; no commands were run.
