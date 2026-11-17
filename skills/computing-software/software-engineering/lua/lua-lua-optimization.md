---
id: computing-software.software-engineering.lua.lua-lua-optimization
name: lua-lua-optimization
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-performance, lua-optimization]
level: advanced
status: docs-checked
description: "Measure with os.clock and profilers and apply table, string and local-variable optimisations."
sources:
  - https://www.lua.org/manual/5.4/manual.html
  - https://luajit.org/extensions.html
  - https://luajit.org/running.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiling and optimising Lua code
- Measure first: `os.clock()` around loops (CPU time), a sampling or counting hook built on `debug.sethook`, or LuaJIT's `-jp` integrated profiler; use many iterations to avoid timer noise.
- Preallocate in LuaJIT with `table.new(narray, nhash)` after `require("table.new")`; the Lua 5.4 table library has no preallocation function.
- Avoid creating closures and tables in hot loops; reuse buffers; cache globals and library functions in locals (`local insert = table.insert`) and time the change.
- Build strings with `table.concat(list, sep)` rather than repeated `..` in a loop.
- Memoise pure functions with weak-table caches (`setmetatable(cache, {__mode = "k"})` or `"v"`; the collector may drop entries).
Verify: before and after timing with the same input.

## Checked
2026-11-08. Confirmed in the Lua 5.4 Reference Manual (`os.clock`, `debug.sethook`, `table.concat`, weak tables in section 2.5.4, via targeted reads), LuaJIT Extensions (`table.new`) and Running LuaJIT (`-jp`). Removed: named third-party profilers, the claims that `ipairs` and numeric `for` beat `pairs` and that `#t` recalculation is slow (not in the docs; measure instead).
Method: documentation only; no commands were run.
