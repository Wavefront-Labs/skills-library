---
id: computing-software.software-engineering.nim.asyncdispatch-basics
name: asyncdispatch-basics
category: computing-software
field: software-engineering
product: nim
tags: [asyncdispatch-basics, async-programming, asyncdispatch, async, await, future, waitfor, event-loop, asyncfutures, sleepasync, nim]
level: practitioner
status: docs-checked
description: "Write async procs with {.async.}, await futures, run the dispatcher with waitFor, and combine futures with all and or."
sources:
  - https://nim-lang.org/docs/asyncdispatch.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# asyncdispatch: async procs, await and the event loop

Goal: do concurrent IO on one thread.

```nim
import std/asyncdispatch
proc work(n: int): Future[int] {.async.} =
  await sleepAsync(100)
  return n * 2
echo waitFor work(21)
```
- `{.async.}` rewrites the proc into a state machine returning `Future[T]`; `await` suspends until the future completes.
- `waitFor fut` runs the event loop until done; `asyncCheck fut` neither waits nor returns the result but raises an exception if the future fails.
- Parallel: `let fs = @[work(1), work(2)]; await all(fs)`; first-wins: `await fs[0] or fs[1]`.
- Timers: `sleepAsync(ms)`; timeouts: `withTimeout(fut, ms)` returns a `Future[bool]`.
- Async IO modules: `asyncnet`, `asynchttpserver`, `asyncfile`, `httpclient`'s `AsyncHttpClient`.

Gotchas:
- Never `waitFor` inside an async proc; use `await`.
- Do not discard futures directly: they may contain errors. `await` checks the future for you and `asyncCheck` raises if it failed.

Verify: two 100 ms sleeps awaited together finish in about 100 ms.

## Checked

2026-11-03. Confirmed against the asyncdispatch page: async pragma, await, waitFor, asyncCheck semantics, the 'never discard futures' note, sleepAsync, withTimeout (Future[bool]), the `all` and `or` future combinators in the exports list. Removed: the blocking-call stall claim as worded and the swallowed-errors wording.

Method: documentation only; no commands were run.
