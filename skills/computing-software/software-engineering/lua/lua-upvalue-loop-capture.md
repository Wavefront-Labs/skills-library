---
id: computing-software.software-engineering.lua.lua-upvalue-loop-capture
name: lua-upvalue-loop-capture
category: computing-software
field: software-engineering
product: lua
tags: [lua, upvalue-loop-capture]
level: advanced
status: docs-checked
description: "Understand upvalue capture: each loop iteration creates a fresh local, so closures capture per-iteration values."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upvalues in loops
- In `for i=1,3 do fns[i]=function() return i end end` the control variable is a new variable local to the loop body, so each closure sees its own `i`.
- A `while` loop that mutates one outer local shares a single upvalue across closures.
- Each execution of a `local` statement defines new local variables; closures that access the same external local variable share it, and `debug.upvalueid` returns identical ids for shared upvalues.
Verify: call all three closures and print 1, 2, 3.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 3.5 (ten closures each get their own y while sharing x), 3.3.5 (control variable local to the loop body) and 6.10 (debug.upvalueid). Removed: debug.upvaluejoin and the large-object remark.
Method: documentation only; no commands were run.
