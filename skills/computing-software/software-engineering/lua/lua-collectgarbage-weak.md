---
id: computing-software.software-engineering.lua.lua-collectgarbage-weak
name: lua-collectgarbage-weak
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-memory-gc, collectgarbage-weak]
level: advanced
status: docs-checked
description: "Tune and observe the GC with collectgarbage, use weak tables for caches and avoid leaks."
sources: ["https://www.lua.org/manual/5.4/manual.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# collectgarbage, GC modes and weak tables
- `collectgarbage("count")` returns the memory in use in Kbytes (fractional); `"step"` performs a basic step; `"incremental"` and `"generational"` select the collector mode (5.4).
- Weak tables use the `__mode` metafield; only objects with explicit construction are removed from them; numbers and strings behave like values and are not removed.
- To-be-closed variables (`local x <close>`) run `__close` on scope exit by normal exit, `break`, `goto`, `return` or error (5.4).
Verify: allocate in a loop and watch `collectgarbage("count")` plateau.

## Checked

Date: 2026-11-02. Confirmed on Lua 5.4 manual: collectgarbage ('count' in Kbytes, 'step'), section 2.5 (incremental and generational modes), weak tables (strings as values), to-be-closed variables. Removed as not confirmed: the list of common leaks and the `__gc` resurrection remark.

Method: documentation only; no commands were run.
