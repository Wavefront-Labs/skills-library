---
id: computing-software.software-engineering.lua.lua-os-clock-vs-time
name: lua-os-clock-vs-time
category: computing-software
field: software-engineering
product: lua
tags: [lua, os-clock-vs-time]
level: practitioner
status: docs-checked
description: "Time Lua code correctly: os.clock measures CPU time, os.time wall seconds, and repeat runs with a warm-up."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timing
- `os.clock()` returns an approximation of the CPU time used by the program, in seconds (the C function `clock`).
- `os.time()` returns the current time as a number whose meaning depends on the system; on POSIX and Windows it counts seconds since the epoch. `os.difftime(t2, t1)` gives the difference in seconds.
- `collectgarbage("collect")` performs a full collection cycle and is the default option, which is useful before timing a run.
Verify: a busy loop shows clock growth; `os.execute("sleep 1")` does not.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 6.9 (os.clock, os.time, os.difftime) and 6.1 (collectgarbage). Removed: LuaSocket gettime and luv.hrtime (third-party, not on the page), 'integer' for os.time, and benchmarking advice.
Method: documentation only; no commands were run.
