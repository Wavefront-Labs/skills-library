---
id: computing-software.software-engineering.lua.lua-coroutine-close-isyieldable
name: lua-coroutine-close-isyieldable
category: computing-software
field: software-engineering
product: lua
tags: [lua, coroutine-close-isyieldable]
level: advanced
status: docs-checked
description: "Manage coroutine lifetime in Lua 5.4: coroutine.close for cleanup, status values, isyieldable and running."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Coroutine lifetime
- `coroutine.status(co)` is suspended, running, normal (resumed another) or dead.
- `coroutine.close(co)` (5.4) closes a suspended or dead coroutine, running pending to-be-closed variables; returns true, or false plus the error.
- `coroutine.isyieldable()` is false on the main thread and inside a non-yieldable C function.
- `coroutine.running()` returns the thread and a boolean for main.
Verify: close a suspended coroutine that holds a `<close>` variable and see its cleanup run.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 6.2 (coroutine.close, status, isyieldable, running). Fixed: isyieldable description now matches the manual.
Method: documentation only; no commands were run.
