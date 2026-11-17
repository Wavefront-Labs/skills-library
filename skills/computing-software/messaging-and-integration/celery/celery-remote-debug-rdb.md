---
id: computing-software.messaging-and-integration.celery.celery-remote-debug-rdb
name: celery-remote-debug-rdb
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-debugging, celery, rdb, pdb, remote-debugging, telnet, sigusr2, breakpoint]
level: practitioner
status: docs-checked
description: "Debug a running Celery task with celery.contrib.rdb: set_trace, telnet to the port, CELERY_RDB_PORT and CELERY_RDB_HOST, and the SIGUSR2 breakpoint signal."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/debugging.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debug Celery tasks remotely with rdb

Goal: step through a task running in a worker that has no terminal.

`celery.contrib.rdb` is an extended `pdb` for remote debugging of processes without terminal access. Put a break-point in the task:

```python
from celery import task
from celery.contrib import rdb

@task()
def add(x, y):
    result = x + y
    rdb.set_trace()  # <- set break-point
    return result
```

`set_trace()` sets a break-point at the current location and opens a socket you can telnet into.

Ports and access:
- The debugger may start in several processes at once, so it searches for a free port starting at the base port, 6900 by default. Change the base with env `CELERY_RDB_PORT`.
- By default it is reachable only from the local host. Set env `CELERY_RDB_HOST` to allow access from outside.

When the worker hits the break-point it logs something like:

```text
[WARNING/PoolWorker-1] Remote Debugger:6900:
    Please telnet 127.0.0.1 6900.  Type `exit` in session to continue.
```

Connect and you get a pdb prompt (the page's session shows the current line and `(Pdb)`):

```console
$ telnet localhost 6900
(Pdb) result
4
(Pdb) result = 'hello from rdb'
(Pdb) continue
Connection closed by foreign host.
```

The worker log then shows the changed value as the task result: `Task tasks.add[d7261c71-4962-47e5-b342-2448bedd20e8] succeeded in 61.481s: 'hello from rdb'`. Type `help` for pdb commands.

Break-point signal: if env `CELERY_RDBSIG` is set, the worker opens an rdb instance whenever it receives `SIGUSR2`, for both the main process and pool processes. Start with `CELERY_RDBSIG=1 celery worker -l INFO`, then `kill -USR2 <pid>` for any worker process.

Gotchas: the worker log shows "Waiting for client..." until you connect. Exiting the session with `exit` or `continue` lets the task continue.

## Checked

2026-11-07. Re-read the cited page(s) (debugging) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. Code snippet and include files were not opened separately.

Changed: removed an unsupported production-code warning.

Method: documentation only; no commands were run.
