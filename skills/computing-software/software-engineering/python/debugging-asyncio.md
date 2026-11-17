---
id: computing-software.software-engineering.python.debugging-asyncio
name: debugging-asyncio
category: computing-software
field: software-engineering
product: python
tags: [python, asyncio-debug-mode, never-awaited, task-exception-never-retrieved, slow-callback, asyncio, aiomonitor]
level: advanced
status: verified
description: "Diagnose asyncio bugs: debug mode, 'coroutine was never awaited', 'Task exception was never retrieved', lost tasks from GC, slow callbacks, and dumping all running tasks."
sources: ["https://docs.python.org/3/library/asyncio-dev.html", "https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task", "https://docs.python.org/3/library/asyncio-task.html#asyncio.all_tasks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging asyncio

**Goal:** find the hung, lost or silently failing coroutine in an async application.

## Turn on debug mode
```bash
PYTHONASYNCIODEBUG=1 python -X dev app.py
# or asyncio.run(main(), debug=True)
```
Enables: logging of never-awaited coroutines with the creation traceback, slow callback
warnings (>100 ms, `loop.slow_callback_duration`), non-threadsafe call detection, and
resource warnings for unclosed transports. Development only - it is slow.

## Classic symptoms
**`RuntimeWarning: coroutine 'save' was never awaited`**
You called `save()` without `await`; the body never ran. Debug mode shows where it was created.
Type checkers catch it too (mypy `unused-coroutine`, pyright `reportUnusedCoroutine`). Ruff `RUF006` is a different check: it flags `create_task` results that are not stored.

**`Task exception was never retrieved`**
A task created with `create_task` raised, and nobody awaited it. The error is logged only
when the task is garbage collected - possibly much later. Fix: structure with
`asyncio.TaskGroup` (exceptions propagate), or add
`task.add_done_callback(lambda t: t.cancelled() or t.exception() and log.error(...))`.

**Task vanished mid-way**
The loop keeps only weak references to tasks. A fire-and-forget `asyncio.create_task(x())`
with no saved reference can be garbage collected before finishing.
```python
background = set()
t = asyncio.create_task(job()); background.add(t); t.add_done_callback(background.discard)
```

**Everything slow / timeouts everywhere**
Something blocks the loop. Debug mode prints `Executing <Task ...> took 1.2 seconds`.
Offload with `asyncio.to_thread`.

**Hang**
Dump every task and where it is suspended:
```python
for t in asyncio.all_tasks():
    t.print_stack()           # or t.get_coro().cr_frame
```
Wire it to a signal handler (`loop.add_signal_handler(signal.SIGUSR1, dump)`; POSIX only, Windows loops raise `NotImplementedError` and have no `SIGUSR1`), use
`python -m asyncio ps <pid>` / `pstree <pid>` (3.14+; on Windows 3.14.0 it failed with "Failed to find the PyRuntime section"), or `py-spy dump --pid <pid>` from
outside. aiomonitor gives a telnet console listing tasks in a live app.

## Exception handler for stray errors
```python
def handler(loop, ctx):
    log.error("asyncio: %s", ctx.get("message"), exc_info=ctx.get("exception"))
asyncio.get_running_loop().set_exception_handler(handler)
```

## Gotchas
- Mixing `asyncio.run()` calls or creating loops per request breaks connection pools bound to
  a loop ("attached to a different loop", "Event loop is closed").
- Jupyter already runs a loop: use top-level `await`, not `asyncio.run`.
- `pytest-asyncio` creates loops per test by default; session-scoped async fixtures need
  matching loop scope.

## Verify
- [ ] Test suite runs with `PYTHONASYNCIODEBUG=1 -W error::RuntimeWarning` clean.
- [ ] No bare `create_task` without a stored reference or a TaskGroup.

## Checked
- Python 3.14.0 on Windows: debug mode printed the never-awaited coroutine with its creation traceback and "Executing <Task ...> took 0.205 seconds"; `loop.add_signal_handler` raised `NotImplementedError` and `signal.SIGUSR1` is absent on Windows; an `asyncio.Lock` reused on a second loop raised `RuntimeError ... is bound to a different event loop`; `python -m asyncio ps/pstree <pid>` exists in 3.14 (What's New) but failed here with "Failed to find the PyRuntime section"; ruff `RUF006` is asyncio-dangling-task (ruff rule docs, run locally). `py-spy` and aiomonitor were not run.
