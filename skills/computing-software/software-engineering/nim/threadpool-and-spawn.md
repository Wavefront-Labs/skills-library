---
id: computing-software.software-engineering.nim.threadpool-and-spawn
name: threadpool-and-spawn
category: computing-software
field: software-engineering
product: nim
tags: [threadpool-and-spawn, threads-and-parallelism, threadpool, spawn, flowvar, parallel, sync, fork-join, parallel-for, nim]
level: advanced
status: docs-checked
description: "Use std/threadpool spawn and FlowVar for fork-join parallelism, and know that the module is deprecated."
sources:
  - https://nim-lang.org/docs/threadpool.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# threadpool and spawn

Goal: parallelise independent tasks.

```nim
import std/threadpool
proc fib(n: int): int = (if n < 2: n else: fib(n-1) + fib(n-2))
let a = spawn fib(30)
let b = spawn fib(31)
echo ^a + ^b   # ^ blocks on the FlowVar
```
- `spawn f(args)` returns a `FlowVar[T]`; `^fv` waits and reads; `sync()` waits for all tasks; `blockUntilAny(flowVars)` waits for the first ready one; `isReady(fv)` polls.
- The module implements `parallel` and `spawn`; set pool size via `setMaxPoolSize` / `setMinPoolSize` (at most `MaxThreadPoolSize`, 256 by default).
- The page marks the module deprecated and its API unstable, and recommends the nimble packages `malebolgia`, `taskpools` or `weave` instead.

Gotchas:
- `spawn` returns a `FlowVar[T]`; `^` blocks until the value is available.

Verify: the example prints the sum of fib(30) and fib(31).

## Checked

2026-11-03. Confirmed against the threadpool page: spawn, FlowVar, `^`, sync, blockUntilAny, isReady, parallel, setMaxPoolSize/setMinPoolSize, MaxThreadPoolSize = 256, the deprecation note recommending malebolgia, taskpools or weave, unstable API. Real error fixed: `awaitAny` does not exist (the page has `blockUntilAny`). Removed: --threads:on, gcsafe-argument, exception-propagation and task-size claims (not on the page).

Method: documentation only; no commands were run.
