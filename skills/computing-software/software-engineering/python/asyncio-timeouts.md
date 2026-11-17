---
id: computing-software.software-engineering.python.asyncio-timeouts
name: asyncio-timeouts
category: computing-software
field: software-engineering
product: python
tags: [python, asyncio-timeout, wait-for, deadlines, cancellation, timeout-errors, asyncio]
level: practitioner
status: verified
description: "Put deadlines on async work with asyncio.timeout/timeout_at and wait_for, reschedule deadlines, handle TimeoutError vs CancelledError, and timeouts for whole operations."
sources: ["https://docs.python.org/3/library/asyncio-task.html#timeouts", "https://docs.python.org/3/library/asyncio-task.html#asyncio.wait_for", "https://docs.python.org/3/library/asyncio-task.html#task-cancellation"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# asyncio timeouts

**Goal:** every network-facing await has a deadline, timeouts propagate as clean
errors, and cancellation is not accidentally swallowed.

## asyncio.timeout (3.11+): preferred
```python
import asyncio
try:
    async with asyncio.timeout(5):          # whole block, including several awaits
        user = await repo.get_user(uid)
        prefs = await repo.get_prefs(uid)
except TimeoutError:
    raise ServiceUnavailable("user lookup timed out")
```
- On expiry the current task is cancelled; the context manager converts that
  `CancelledError` into `TimeoutError` at the `async with` boundary.
- `asyncio.timeout(None)` = no timeout; `cm.reschedule(loop.time() + 2)` extends or
  shortens a running deadline; `asyncio.timeout_at(when)` takes an absolute loop time -
  ideal for propagating one request-wide deadline into nested calls.
- Since 3.11 `asyncio.TimeoutError` is an alias of the builtin `TimeoutError`.

## wait_for
```python
result = await asyncio.wait_for(fetch(), timeout=5)
```
Wraps a single awaitable; since 3.12 implemented with `timeout()` internally. Use when you
need the expression form or support older Pythons.

## Don't break cancellation
```python
try:
    await work()
except asyncio.CancelledError:
    await cleanup()
    raise                      # always re-raise; swallowing it breaks timeout() and TaskGroup
```
`except Exception` does not catch `CancelledError` (it is a `BaseException` since 3.8) -
good. A bare `except:` or `except BaseException:` without re-raise will.

Shielding work that must finish (e.g. commit): `await asyncio.shield(commit())` - the
outer await still times out, but the inner task keeps running.

## Layer timeouts
- Client-level: `httpx.AsyncClient(timeout=httpx.Timeout(10, connect=2))`.
- Operation-level: `asyncio.timeout()` around a multi-call operation.
- Request-level: middleware deadline shorter than the load balancer's idle timeout.
Inner timeouts should be shorter than outer ones so the inner error (more specific) wins.

## Gotchas
- A timeout only interrupts at an `await`; a CPU loop or blocking call inside the block
  overruns silently.
- Nested `timeout()` blocks: the innermost expired one raises; outer ones see normal flow.
- Retry loops need a total deadline too, not just per attempt.

## Verify
- [ ] Every outbound network call has an explicit timeout (grep for client constructors).
- [ ] Tests simulate a hanging dependency (`await asyncio.sleep(3600)`) and assert TimeoutError handling.
## Checked
- Python 3.14.0: `asyncio.timeout(0.2)` around several awaits raises `TimeoutError` at the `async with` boundary; `asyncio.TimeoutError is TimeoutError`; `cm.reschedule(...)` shortened a 10 s deadline to 0.2 s; `timeout_at` and `timeout(None).when()` (`None`); `wait_for` raises `TimeoutError`; `CancelledError` is a `BaseException` but not an `Exception`, so `except Exception` let a cancelled task cancel while `except BaseException` swallowed it, and swallowing it inside `timeout()` returned the handler's value instead of `TimeoutError`; `shield` kept the inner commit running after the outer `wait_for` timed out; with nested `timeout()` blocks the expired inner one raised and the outer carried on; a 0.5 s CPU loop inside a 0.1 s timeout ran to completion (the timeout only acts at an `await`). httpx timeouts and the request-deadline layering were not run.
Linux pass (Python 3.14.8 standalone musl build in a WSL2 busybox distro): every check above gave the same result as on Windows.
