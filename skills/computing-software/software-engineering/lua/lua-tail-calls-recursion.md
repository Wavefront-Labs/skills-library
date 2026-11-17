---
id: computing-software.software-engineering.lua.lua-tail-calls-recursion
name: lua-tail-calls-recursion
category: computing-software
field: software-engineering
product: lua
tags: [lua, tail-calls-recursion]
level: advanced
status: docs-checked
description: "Write tail-recursive Lua with `return f(x)`, which does not grow the stack, versus non-tail recursion that hits stack overflow."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tail calls
- `return f(args)` outside the scope of any to-be-closed variable is a proper tail call: the called function reuses the caller's stack entry, so the number of nested tail calls is unlimited. `return (f(x))`, `return 2 * f(x)`, `return x, f(x)` and `return x or f(x)` are not tail calls.
- A tail call erases any debug information about the calling function, which can confuse debugging.
Verify: a tail-recursive loop of 1e7 iterations finishes.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 3.4.10 (function calls, tail calls and the non-tail examples). Removed: C-call and stack limit names (LUAI_MAXCCALLS, LUAI_MAXSTACK) and the claim that the non-tail version errors.
Method: documentation only; no commands were run.
