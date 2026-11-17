---
id: computing-software.software-engineering.lua.lua-coroutine-scheduler
name: lua-coroutine-scheduler
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-scheduler, coroutine-scheduler]
level: advanced
status: docs-checked
description: "Build a simple round-robin scheduler and async-style wrappers on top of coroutines."
sources:
  - https://www.lua.org/manual/5.4/manual.html
  - https://luajit.org/extensions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task schedulers and async wrappers with coroutines
- Keep a queue of coroutines; the loop resumes each and re-queues it when `coroutine.status` is `"suspended"` (also the state of a coroutine that has not started yet), and drops `"dead"` ones (finished, or stopped with an error).
- Yield a wait request (such as a timestamp or file descriptor); the scheduler resumes when ready, so blocking calls become `yield`s. Values passed to `coroutine.resume` come back as the results of `yield`; values passed to `yield` come back from `resume` after `true`.
- Report errors: `local ok, err = coroutine.resume(co)`; when `ok` is false, `resume` returned `false` plus the error message, and `debug.traceback(co, err)` gives a traceback of that coroutine with `err` prepended.
- `coroutine.isyieldable()` is false on the main thread and inside non-yieldable C functions.
- In the standard Lua 5.1 VM you cannot yield across `pcall`; LuaJIT's fully resumable VM can.
Verify: two tasks that sleep different amounts finish in the expected order.

## Checked
2026-11-08. Confirmed in the Lua 5.4 Reference Manual coroutine library (`resume`, `status`, `isyieldable`) and `debug.traceback` entries, and in the LuaJIT Extensions page ("Fully Resumable VM"), read via targeted reads. Removed: the unverified list of scheduler libraries (copas, luv-based schedulers) and the claim that the traceback is otherwise lost.
Method: documentation only; no commands were run.
