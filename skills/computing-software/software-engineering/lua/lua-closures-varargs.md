---
id: computing-software.software-engineering.lua.lua-closures-varargs
name: lua-closures-varargs
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-functions, closures-varargs]
level: practitioner
status: docs-checked
description: "Use closures, upvalues, varargs and multiple return values correctly."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Closures, varargs and multiple returns
- Functions are first-class values. A local used by an inner function is an upvalue; variables declared by a `for` statement are locals of the loop body, and a closure sees its upvalue by reference.
- Multiple returns: `return a, b`. A multi-result expression is expanded only as the last element of an expression list; elsewhere it is adjusted to one value, and `(g())` forces exactly one result.
- Varargs `...`: `select("#", ...)` counts all arguments, `select(n, ...)` returns those after position n (negative n counts from the end); `{...}` can lose trailing nils to length ambiguity, while `table.pack(...)` keeps `n`.
- A call of the form `return f(x)` outside the scope of any to-be-closed variable is a proper tail call: the stack entry is reused, so nested tail calls are unlimited, but debug information about the caller is erased.
- `obj:m(x)` is `obj.m(obj, x)`.
Verify: `print((function() return 1, 2 end)())` versus wrapped in parentheses.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: section 3.5 (upvalues), section 3.4.12 (multiple results and adjustment), section 3.4.10 (tail calls), select, table.pack, section 3.4.11 (method call sugar). Removed: the claim that each loop iteration creates a fresh local captured by closures (the manual only says for-variables are local to the loop body).
Method: documentation only; no commands were run.
