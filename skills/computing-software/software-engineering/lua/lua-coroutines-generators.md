---
id: computing-software.software-engineering.lua.lua-coroutines-generators
name: lua-coroutines-generators
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-coroutines, coroutines-generators]
level: advanced
status: docs-checked
description: "Use coroutines for generators, producers and cooperative scheduling, and handle errors and states."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# create, resume, yield, wrap and status
- `local co = coroutine.create(f)`; `coroutine.resume(co, ...)` returns `true` plus yielded or returned values, or `false` plus the error message; `coroutine.yield(...)` suspends and its arguments become extra results of `resume`; the arguments of the next `resume` become the results of `yield`.
- `coroutine.wrap(f)` returns a function that resumes the coroutine; on error it closes the coroutine and propagates the error.
- `coroutine.status(co)` is "running", "suspended" (also before first start), "normal" (active but has resumed another) or "dead" (body finished or stopped by an error).
- `coroutine.close(co)` closes a suspended or dead coroutine and its pending to-be-closed variables (5.4), returning `true` or `false` plus the error object. `coroutine.isyieldable([co])` is true outside the main thread and outside non-yieldable C functions. `coroutine.running()` returns the running coroutine and whether it is the main one.
- Coroutines run cooperatively: only one runs at a time, and Lua threads are not operating-system threads.
Verify: a generator yields a known sequence then returns dead status.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: section 2.6 and section 6.2 (coroutine.create, resume, yield, wrap, status, close, isyieldable, running). Removed: the claims about yielding across `pcall` and C boundaries in Lua 5.1, 5.2 and LuaJIT 2 (the manual covers 5.4 only), and the 'resuming a dead coroutine returns false' wording (resume reports an error as false plus message).
Method: documentation only; no commands were run.
